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

# 제공자별 기본 API URL 매핑
DEFAULT_URLS = {
    "ollama": "http://localhost:11434",
    "lmstudio": "http://localhost:1234/v1",
    "llamacpp": "http://localhost:8080/v1"
}
API_URL = os.getenv("LLM_API_URL", DEFAULT_URLS.get(PROVIDER, "http://localhost:11434"))

async def call_gemma4_stream(prompt: str):
    headers = {"Content-Type": "application/json"}
    
    # 1. API 주소 및 페이로드 구성
    if PROVIDER == "ollama":
        # Ollama 네이티브 API 엔드포인트
        url = f"{API_URL}/api/chat"
        payload = {
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": True
        }
    else:
        # LM Studio & llama.cpp (OpenAI 규격 호환 엔드포인트)
        url = f"{API_URL}/chat/completions"
        payload = {
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": True
        }
        
    print(f"[설정 정보] 제공자: {PROVIDER.upper()} | 주소: {url} | 모델: {MODEL}")
    print("-" * 50)

    # 2. HTTPX 비동기 클라이언트로 연결 수립 및 스트리밍 처리
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", url, json=payload, headers=headers) as response:
                if response.status_code != 200:
                    print(f"오류 발생: 서버 응답 코드 {response.status_code}")
                    error_body = await response.aread()
                    print(f"상세 내용: {error_body.decode('utf-8')}")
                    return

                in_thinking = False
                
                # 라인별 스트림 파싱
                async for line in response.iter_lines():
                    if not line:
                        continue
                    
                    token = ""
                    
                    # Ollama 포맷 처리
                    if PROVIDER == "ollama":
                        try:
                            data = json.loads(line)
                            token = data.get("message", {}).get("content", "")
                        except json.JSONDecodeError:
                            continue
                            
                    # OpenAI 호환 포맷 처리 (LM Studio, llama.cpp)
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

                    # 3. 생각 과정(Thinking) 태그 파싱 및 스트리밍 출력
                    if "<think>" in token:
                        print("\n\n[생각 과정 시작...]\n" + "\033[90m", end="", flush=True) # 회색 텍스트 전환
                        in_thinking = True
                        token = token.replace("<think>", "")
                        
                    if in_thinking and "</think>" in token:
                        token = token.replace("</think>", "")
                        print(token + "\033[0m" + "\n\n[생각 과정 완료 - 답변 생성 시작]\n", end="", flush=True) # 색상 초기화
                        in_thinking = False
                        continue
                    
                    # 스트리밍 출력
                    print(token, end="", flush=True)
                    
            print("\n" + "-" * 50)
            
    except httpx.ConnectError:
        print(f"\n[연결 실패] '{PROVIDER}' 로컬 서버가 작동 중인지 확인해 주세요.")
        print(f"접속 시도 주소: {API_URL}")
        print("서버 실행 상태(Ollama App 실행 또는 llama-server 구동 여부)를 재확인하세요.")
    except Exception as e:
        print(f"\n[오류 발생] 예외 정보: {e}")

async def main():
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        prompt = "파이썬 비동기 라이브러리인 httpx의 장점 3가지를 설명해줘."
        
    await call_gemma4_stream(prompt)

if __name__ == "__main__":
    asyncio.run(main())
