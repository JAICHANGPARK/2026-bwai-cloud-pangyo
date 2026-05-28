# Google Antigravity (AGY) SDK를 활용한 핸즈온 코드 생성 가이드

이 문서는 Google Antigravity (AGY) SDK 에이전트에 우리가 정의한 **핸즈온 시스템 프롬프트**를 주입하고, 에이전트가 그 규칙에 따라 필요한 파이썬 실습 코드를 자동으로 생성하도록 구현하는 방법을 안내합니다.

---

## 1. 사전 준비

### 라이브러리 설치
가상환경을 활성화한 상태에서 AGY SDK와 환경변수 로더를 설치합니다:
```bash
uv add google-antigravity python-dotenv
```

### API 키 설정
Gemini 모델 호출을 위해 Google AI Studio에서 API 키를 발급받은 뒤 `.env` 파일에 저장합니다.
*   **API 키 발급:** [Google AI Studio API Key](https://aistudio.google.com/app/api-keys)
*   **`.env` 파일 설정:**
    ```env
    GEMINI_API_KEY=your_gemini_api_key_here
    ```

---

## 2. AGY 에이전트 구성 및 코드 생성 방법

AGY SDK에서 시스템 프롬프트(Persona/System Instructions)를 주입할 때는 `LocalAgentConfig` 클래스의 `system_instructions` 인자를 사용합니다.

아래는 시스템 프롬프트를 에이전트에 주입하고, 사용자의 상세 요구사항을 받아 핸즈온 코드를 스트리밍으로 출력받는 완성형 파이썬 스크립트입니다.

### 파일 작성: `generate_hands_on_code.py`
```python
import asyncio
import os
from google.antigravity import Agent, LocalAgentConfig
from google.antigravity.types import TemplatedSystemInstructions
from dotenv import load_dotenv

# 환경변수 로드 (.env의 GEMINI_API_KEY 활성화)
load_dotenv()

# 앞서 정의한 핸즈온 코드 생성 시스템 프롬프트
HANDS_ON_SYSTEM_PROMPT = """역할: 너는 로컬 LLM 통합에 특화된 시니어 파이썬 개발자야.
작성 목표: 로컬에 기동된 Gemma 4 API 서버(Ollama, LM Studio, llama.cpp) 중 선택한 환경에 맞춰 비동기 또는 동기 방식으로 추론하고, 스트리밍 응답과 모델의 생각 과정(Reasoning/Thinking)을 구분해 출력해 주는 파이썬 스크립트를 작성해 줘.

반드시 지켜야 할 제약사항:
1. HTTP 클라이언트 라이브러리로 requests 대신 'httpx'를 사용할 것.
2. 가볍고 빠른 비동기(Async) 또는 동기(Sync) 코드를 선택적으로 제공할 것.
3. 로컬 API 환경 설정을 소스코드 하드코딩이 아닌 '환경변수(os.environ)'를 통해 유연하게 주입할 것:
   - LLM_PROVIDER: 'ollama' | 'lmstudio' | 'llamacpp' (기본값: 'ollama')
   - LLM_API_URL: 해당 서버의 Base URL (기본값은 제공자별 기본 포트 기준 자동 매핑)
   - LLM_MODEL: 호출할 모델 이름 (기본값: 'gemma4:e4b')
4. Gemma 4 모델의 생각 과정(Thinking/Reasoning)을 파싱하여 화면에 시각적으로 구분하여 표시할 것:
   - 일반적으로 생각 과정은 응답 텍스트의 <think>와 </think> 태그 내부에 존재함.
   - 스트리밍 출력 시 <think> 태그가 감지되면 화면에 '[생각 과정 시작]' 문구와 함께 회색이나 다른 텍스트 스타일로 출력하고, </think>를 만나면 일반 답변 출력으로 전환해 줘.
5. 로컬 서버 연결이 끊겼거나 접속이 안 될 때 상세한 에러 핸들링 코드를 포함할 것.
"""

async def main():
    # 1. 에이전트 설정 정의 (시스템 지침 주입)
    config = LocalAgentConfig(
        system_instructions=TemplatedSystemInstructions(
            identity=HANDS_ON_SYSTEM_PROMPT
        )
    )

    # 2. 에이전트 초기화 및 실행
    print("AGY 에이전트를 초기화합니다...")
    async with Agent(config) as agent:
        # 생성할 코드의 구체적인 요구사항 설정
        user_request = (
            "LM Studio에서 gemma-4-e4b-it 모델을 호출하고 생각 과정(thinking)과 "
            "답변을 httpx로 처리하는 동기식(Sync) 파이썬 코드를 작성해줘."
        )
        
        print(f"\n[요청] {user_request}\n")
        print("[응답 스트리밍 시작]\n" + "=" * 50)
        
        # 3. 에이전트 대화 시작
        response = await agent.chat(user_request)
        
        # 4. 생성된 응답 실시간 출력
        async for token in response:
            print(token, end="", flush=True)
            
        print("\n" + "=" * 50 + "\n[코드 생성 완료]")

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 3. 에이전트 실행 및 결과 확인

생성한 파이썬 스크립트를 `uv`를 통해 바로 가동해 봅니다:

```bash
uv run generate_hands_on_code.py
```

### 실행 프로세스 설명
1.  **에이전트 Config 초기화:** `LocalAgentConfig`가 주입된 시스템 지침(`HANDS_ON_SYSTEM_PROMPT`)을 탑재합니다.
2.  **세션 수립:** `Agent(config)` 컨텍스트 매니저를 통해 구글 제미나이(Gemini) 백엔드와 연결을 엽니다.
3.  **코드 추론:** 에이전트가 사용자의 요구사항("LM Studio 연동 동기식 파이썬 코드 작성")을 시스템 지침 조건과 결합하여 코드를 빌드합니다.
4.  **스트리밍 출력:** `async for token in response` 구문이 실시간으로 텍스트 토큰을 받아 터미널에 생성 과정을 뿌려줍니다.

이를 응용하여 다양한 로컬 환경(예: llama.cpp 비동기 API 서버 연동 등)에 대응하는 실습 스크립트를 에이전트가 직접 규격에 맞춰 생성하도록 실습을 진행할 수 있습니다.
[목차로 돌아가기](./README.md)
