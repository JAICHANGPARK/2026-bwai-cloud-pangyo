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

async def get_structured_developer_profile(prompt: str):
    headers = {"Content-Type": "application/json"}
    
    # JSON 출력을 유도하는 시스템 지침 설정
    system_instruction = (
        "너는 개발자 프로필 생성기야. 사용자가 입력한 인물에 대한 정보를 반드시 다음 JSON 스키마 규격에 맞춰 단 하나의 JSON 객체로만 응답해줘. "
        "다른 추가 텍스트(마크다운 코드 블록 등)는 절대 포함하지 말고 순수 JSON만 출력해야 해.\n"
        "JSON 스키마:\n"
        "{\n"
        "  \"name\": \"이름 (문자열)\",\n"
        "  \"role\": \"주요 역할/직무 (문자열)\",\n"
        "  \"skills\": [\"기술 스택 배열 (문자열 목록)\"],\n"
        "  \"experience_years\": 경력 년수 (숫자)\n"
        "}"
    )

    messages = [
        {"role": "system", "content": system_instruction},
        {"role": "user", "content": prompt}
    ]

    # 1. API 주소 및 페이로드 구성 (Ollama와 OpenAI 호환 규격의 JSON 모드 설정 적용)
    if PROVIDER == "ollama":
        url = f"{API_URL}/api/chat"
        payload = {
            "model": MODEL,
            "messages": messages,
            "format": "json", # Ollama의 JSON 모드 설정
            "stream": True
        }
    else:
        url = f"{API_URL}/chat/completions"
        payload = {
            "model": MODEL,
            "messages": messages,
            "response_format": {"type": "json_object"}, # OpenAI 규격의 JSON 모드 설정
            "stream": True
        }

    print(f"[설정 정보] 제공자: {PROVIDER.upper()} | 주소: {url} | 모델: {MODEL}")
    print(f"[인물 대상]: {prompt}")
    print("-" * 50)
    print("[스트리밍 출력 시작]")

    accumulated_content = ""

    try:
        # 2. HTTPX 비동기 스트리밍 클라이언트로 연결 및 수신
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", url, json=payload, headers=headers) as response:
                if response.status_code != 200:
                    print(f"오류 발생: 서버 응답 코드 {response.status_code}")
                    error_body = await response.aread()
                    print(f"상세 내용: {error_body.decode('utf-8')}")
                    return

                async for line in response.aiter_lines():
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
                    
                    # 콘솔에 토큰 스트리밍 출력
                    print(token, end="", flush=True)
                    accumulated_content += token

        print("\n" + "-" * 50)
        
        # 3. 수신 완료 후 JSON 파싱 및 최종 검증
        print("[JSON 파싱 및 검증 수행]")
        try:
            parsed_json = json.loads(accumulated_content.strip())
            print(" 파싱 결과: 성공 ✅")
            print(json.dumps(parsed_json, indent=2, ensure_ascii=False))
        except json.JSONDecodeError as je:
            print(f" 파싱 결과: 실패 ❌ (올바른 JSON 형식이 아닙니다.)")
            print(f" 에러 원인: {je}")
            print(f" 수신된 원본 데이터: {accumulated_content}")

    except httpx.ConnectError:
        print(f"\n[연결 실패] '{PROVIDER}' 로컬 서버가 작동 중인지 확인해 주세요.")
        print(f"접속 시도 주소: {API_URL}")
    except Exception as e:
        print(f"\n[오류 발생] 예외 정보: {e}")

async def main():
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = "파이썬 크리에이터 Guido van Rossum에 대한 프로필을 JSON 형태로 생성해줘."
        
    await get_structured_developer_profile(prompt)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n[실행 중단] 사용자에 의해 프로그램이 종료되었습니다.")
        sys.exit(0)
