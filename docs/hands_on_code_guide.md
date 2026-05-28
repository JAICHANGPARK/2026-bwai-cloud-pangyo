# 핸즈온 코드 개발 가이드 및 시스템 프롬프트

이 문서는 Gemma 4 로컬 모델 연동 코드를 자동으로 생성해 주는 **시스템 프롬프트**와 이를 바탕으로 작성된 **레퍼런스 파이썬 코드**를 포함하고 있습니다.

---

## 1. 코드 생성을 위한 시스템 프롬프트
이 프롬프트는 다른 대형 언어 모델(예: Gemini 등)에 입력하여 실습 코드를 생성할 때 사용할 수 있습니다. 아래 텍스트를 복사하여 사용하세요.

```text
역할: 너는 로컬 LLM 통합에 특화된 시니어 파이썬 개발자야.
작성 목표: 로컬에 기동된 Gemma 4 API 서버(Ollama, LM Studio, llama.cpp) 중 선택한 환경에 맞춰 비동기 또는 동기 방식으로 추론하고, 스트리밍 응답과 모델의 생각 과정(Reasoning/Thinking)을 구분해 출력해 주는 파이썬 스크립트를 작성해 줘.

반드시 지켜야 할 제약사항:
1. HTTP 클라이언트 라이브러리로 requests 대신 'httpx'를 사용할 것.
2. 가볍고 빠른 비동기(Async) 또는 동기(Sync) 코드를 선택적으로 제공할 것.
3. 로컬 API 환경 설정을 소스코드 하드코딩이 아닌 '환경변수(os.environ)'를 통해 유연하게 주입할 것:
   - LLM_PROVIDER: 'ollama' | 'lmstudio' | 'llamacpp' (기본값: 'ollama')
   - LLM_API_URL: 해당 서버의 Base URL (기본값은 제공자별 기본 포트 기준 자동 매핑)
     * Ollama: http://localhost:11434 (OpenAI 규격 시 http://localhost:11434/v1)
     * LM Studio: http://localhost:1234/v1
     * llama.cpp: http://localhost:8080/v1
   - LLM_MODEL: 호출할 모델 이름 (기본값: 'gemma4:e4b' 또는 다운로드받은 모델 식별자)
4. Gemma 4 모델의 생각 과정(Thinking/Reasoning)을 파싱하여 화면에 시각적으로 구분하여 표시할 것:
   - 일반적으로 생각 과정은 응답 텍스트의 <think>와 </think> 태그 내부에 존재함.
   - 스트리밍 출력 시 <think> 태그가 감지되면 화면에 '[생각 과정 시작]' 문구와 함께 회색이나 다른 텍스트 스타일로 출력하고, </think>를 만나면 일반 답변 출력으로 전환해 줘.
5. 로컬 서버 연결이 끊겼거나 접속이 안 될 때 상세한 에러 핸들링 코드를 포함할 것.
```

---

## 2. 레퍼런스 파이썬 실습 코드
위의 프롬프트 제약조건을 충족하도록 구성된 실제 동작 코드입니다. 이 코드를 `main.py` 파일로 저장하고 실행해 볼 수 있습니다.

### 파일 작성: `main.py`
```python
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
```

---

## 3. 코드 실행 방법

### step 1. 환경변수 설정 파일 생성 (`.env`)
프로젝트 루트 폴더에 `.env` 파일을 만들고 본인이 실습할 API 제공자 정보를 설정합니다.

*   **Ollama 사용 시:**
    ```env
    LLM_PROVIDER=ollama
    LLM_MODEL=gemma4:e4b
    ```
*   **LM Studio 사용 시:**
    ```env
    LLM_PROVIDER=lmstudio
    LLM_MODEL=gemma-4-e4b-it
    ```
*   **llama.cpp 사용 시:**
    ```env
    LLM_PROVIDER=llamacpp
    LLM_MODEL=gemma-4-e4b-it
    ```

### step 2. uv 가상환경에서 실행
uv 개발 환경 설정이 완료된 상태에서 아래 명령어를 실행하여 코드를 구동합니다.
```bash
# 기본 질문 실행
uv run main.py

# 커스텀 질문 실행
uv run main.py "Gemma 4 모델의 네이티브 멀티모달 능력이란?"
```

이 가이드를 활용해 Gemma 4 API 연동 실습을 원활히 마쳐보세요!
[목차로 돌아가기](./README.md)
