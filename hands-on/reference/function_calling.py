import os
import sys
import json
import asyncio
import httpx
from dotenv import load_dotenv

# .env 파일이 존재할 경우 환경변수 자동 로드
load_dotenv()

# 환경변수 로드 및 기본 설정
PROVIDER = os.getenv("LLM_PROVIDER", "ollama").lower()
MODEL = os.getenv("LLM_MODEL", "gemma4:e4b")

DEFAULT_URLS = {
    "ollama": "http://localhost:11434",
    "lmstudio": "http://localhost:1234/v1",
    "llamacpp": "http://localhost:8080/v1"
}
API_URL = os.getenv("LLM_API_URL", DEFAULT_URLS.get(PROVIDER, "http://localhost:11434"))

# 실습에 사용할 가상의 날씨 조회 도구(Tool/Function)
def get_current_weather(location: str):
    """지정된 도시의 현재 날씨를 가져옵니다."""
    weather_db = {
        "seoul": {"temp": "22°C", "condition": "맑음", "humidity": "45%"},
        "tokyo": {"temp": "25°C", "condition": "흐림", "humidity": "60%"},
        "new york": {"temp": "18°C", "condition": "비", "humidity": "80%"}
    }
    loc_clean = location.lower().split(",")[0].strip()
    return weather_db.get(loc_clean, {"temp": "20°C", "condition": "맑음", "humidity": "50%"})

# 모델에 주입할 도구의 스키마 정의
TOOLS_DEFINITION = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "특정 위치의 현재 날씨 정보를 조회합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "날씨를 조회할 도시 이름 (예: Seoul, Tokyo, New York)"
                    }
                },
                "required": ["location"]
            }
        }
    }
]

async def run_function_calling(prompt: str):
    headers = {"Content-Type": "application/json"}
    messages = [{"role": "user", "content": prompt}]
    
    # 1. API 주소 및 페이로드 구성
    if PROVIDER == "ollama":
        url = f"{API_URL}/api/chat"
        payload = {
            "model": MODEL,
            "messages": messages,
            "tools": TOOLS_DEFINITION,
            "stream": False # 첫 번째 턴(도구 호출 판단)은 비스트리밍으로 처리
        }
    else:
        url = f"{API_URL}/chat/completions"
        payload = {
            "model": MODEL,
            "messages": messages,
            "tools": TOOLS_DEFINITION,
            "stream": False
        }

    print(f"[설정 정보] 제공자: {PROVIDER.upper()} | 주소: {url} | 모델: {MODEL}")
    print(f"[사용자 입력]: {prompt}")
    print("-" * 50)

    try:
        # 1단계: 모델에 질의하여 도구 호출 여부 확인
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            if response.status_code != 200:
                print(f"오류 발생: 서버 응답 코드 {response.status_code}")
                print(f"상세 내용: {response.text}")
                return

            res_data = response.json()
            tool_calls = []

            # 제공자별 응답 구조 파싱
            if PROVIDER == "ollama":
                assistant_message = res_data.get("message", {})
                tool_calls = assistant_message.get("tool_calls", [])
            else:
                assistant_message = res_data.get("choices", [{}])[0].get("message", {})
                tool_calls = assistant_message.get("tool_calls", [])

            # 도구 호출이 없는 경우 일반 대답 출력
            if not tool_calls:
                content = assistant_message.get("content", "")
                print(f"[모델 대답 - 도구 사용 안 함]: {content}")
                return

            # 도구 호출이 감지된 경우
            print(f"[도구 호출 감지!]")
            messages.append(assistant_message) # 대화 이력에 어시스턴트 메시지 추가

            for tool_call in tool_calls:
                # 함수 정보 추출
                func_info = tool_call.get("function", {})
                func_name = func_info.get("name")
                
                # 인자 값 파싱 (문자열인 경우와 객체인 경우 구분)
                args = func_info.get("arguments", {})
                if isinstance(args, str):
                    try:
                        args = json.loads(args)
                    except json.JSONDecodeError:
                        args = {}
                
                location = args.get("location", "")
                
                print(f" -> 호출할 함수: {func_name} | 인자: {args}")
                
                # 실제 로컬 함수 실행
                if func_name == "get_current_weather":
                    result = get_current_weather(location)
                else:
                    result = {"error": f"지원하지 않는 도구입니다: {func_name}"}

                print(f" -> 함수 실행 결과: {result}")

                # 2단계: 함수 실행 결과를 메시지 이력에 추가하여 다시 모델 호출
                if PROVIDER == "ollama":
                    messages.append({
                        "role": "tool",
                        "content": json.dumps(result, ensure_ascii=False)
                    })
                else:
                    # OpenAI 호환 규격의 경우 tool_call_id가 매칭되어야 함
                    tool_call_id = tool_call.get("id", "call_default")
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call_id,
                        "name": func_name,
                        "content": json.dumps(result, ensure_ascii=False)
                    })

            # 3단계: 도구 실행 결과를 보강하여 최종 대답 생성 (스트리밍 출력)
            print("-" * 50)
            print("[최종 대답 생성 시작 - 스트리밍]")
            
            if PROVIDER == "ollama":
                payload = {
                    "model": MODEL,
                    "messages": messages,
                    "stream": True
                }
            else:
                payload = {
                    "model": MODEL,
                    "messages": messages,
                    "stream": True
                }

            async with client.stream("POST", url, json=payload, headers=headers) as stream_response:
                if stream_response.status_code != 200:
                    print(f"최종 응답 오류: {stream_response.status_code}")
                    return

                async for line in stream_response.aiter_lines():
                    if not line:
                        continue
                    
                    token = ""
                    if PROVIDER == "ollama":
                        try:
                            data = json.loads(line)
                            token = data.get("message", {}).get("content", "")
                        except json.JSONDecodeError:
                            continue
                    else:
                        if line.startswith("data: "):
                            data_str = line[6:].strip()
                            if data_str == "[DONE]":
                                break
                            try:
                                data = json.loads(data_str)
                                token = data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                            except json.JSONDecodeError:
                                continue
                    
                    print(token, end="", flush=True)
            print("\n" + "-" * 50)

    except httpx.ConnectError:
        print(f"\n[연결 실패] '{PROVIDER}' 로컬 서버가 작동 중인지 확인해 주세요.")
        print(f"접속 시도 주소: {API_URL}")
    except Exception as e:
        print(f"\n[오류 발생] 예외 정보: {e}")

async def main():
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = "오늘 서울 날씨는 어떤지 확인해서 한국어로 친절하게 말해줘."
        
    await run_function_calling(prompt)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n[실행 중단] 사용자에 의해 프로그램이 종료되었습니다.")
        sys.exit(0)
