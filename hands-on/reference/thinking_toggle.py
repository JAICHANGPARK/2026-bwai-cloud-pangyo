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

async def call_gemma4_with_thinking_toggle(prompt: str, thinking_enabled: bool):
    headers = {"Content-Type": "application/json"}
    
    # 1. API 주소 및 페이로드 구성
    if PROVIDER == "ollama":
        url = f"{API_URL}/api/chat"
        # Ollama API 레벨에서 생각 과정 제어 옵션 추가 ("think" 매개변수 사용)
        payload = {
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": True,
            "think": thinking_enabled, # Ollama API 단의 thinking toggle
            "options": {
                "think": thinking_enabled
            }
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
    print(f"[생각 기능 설정]: {'활성화 (ON)' if thinking_enabled else '비활성화 (OFF)'}")
    print("-" * 50)

    try:
        # 2. HTTPX 비동기 클라이언트로 연결 수립 및 스트리밍 처리
        async with httpx.AsyncClient(timeout=60.0) as client:
            async with client.stream("POST", url, json=payload, headers=headers) as response:
                if response.status_code != 200:
                    print(f"오류 발생: 서버 응답 코드 {response.status_code}")
                    error_body = await response.aread()
                    print(f"상세 내용: {error_body.decode('utf-8')}")
                    return

                in_thinking = False
                
                # 라인별 스트림 파싱 및 클라이언트 단의 생각 필터링 적용
                async for line in response.aiter_lines():
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

                    # 3. 생각 과정(Thinking) 태그 파싱 및 필터링 제어
                    if "<think>" in token:
                        in_thinking = True
                        if thinking_enabled:
                            print("\n\n[생각 과정 시작...]\n" + "\033[90m", end="", flush=True) # 회색 텍스트 전환
                        token = token.replace("<think>", "")
                        
                    if in_thinking and "</think>" in token:
                        token = token.replace("</think>", "")
                        if thinking_enabled:
                            print(token + "\033[0m" + "\n\n[생각 과정 완료 - 답변 생성 시작]\n", end="", flush=True) # 색상 초기화
                        in_thinking = False
                        continue
                    
                    # 생각 과정(Thinking) 상태일 때 처리
                    if in_thinking:
                        if thinking_enabled:
                            # 켜져 있을 때만 화면에 출력
                            print(token, end="", flush=True)
                        else:
                            # 꺼져 있을 때는 출력 생략 (화면에 표시하지 않음)
                            pass
                    else:
                        # 일반 답변 상태일 때는 항상 출력
                        print(token, end="", flush=True)
                        
            print("\n" + "-" * 50)
            
    except httpx.ConnectError:
        print(f"\n[연결 실패] '{PROVIDER}' 로컬 서버가 작동 중인지 확인해 주세요.")
        print(f"접속 시도 주소: {API_URL}")
    except Exception as e:
        print(f"\n[오류 발생] 예외 정보: {e}")

async def main():
    thinking_enabled = True
    
    # CLI 인자에 --no-think 플래그가 포함되어 있는지 판별
    args = sys.argv[1:]
    if "--no-think" in args:
        thinking_enabled = False
        args.remove("--no-think")
        
    if args:
        prompt = " ".join(args)
    else:
        prompt = "생각 과정이 필요한 어려운 수학 문제: 17 * 39 + 128 / 4 - 83은 무엇인가요?"
        
    await call_gemma4_with_thinking_toggle(prompt, thinking_enabled)

if __name__ == "__main__":
    asyncio.run(main())
