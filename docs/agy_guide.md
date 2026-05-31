# agy CLI를 활용한 핸즈온 코드 생성 가이드

[Antigravity CLI](https://antigravity.google) (명령어: `agy`)는 터미널 및 콘솔 환경에서 복잡한 코딩 지시, 파일 생성/편집, 에이전트 자율 수행 작업을 수행하는 Google의 에이전트 개발 도구입니다.

이 문서는 `agy` CLI 환경에서 우리가 정의한 **핸즈온 시스템 프롬프트**를 연동하여 실습 코드를 자동으로 생성하도록 요청하는 두 가지 구체적인 방법을 안내합니다.

---

## 1. 방법 A: 작업 공간 규칙 (Workspace Rules) 활용하기 (권장)

`agy` CLI는 실행되는 디렉토리(작업 공간)의 `.agents/rules/` 하위에 위치한 Markdown 문서를 컨텍스트(작업 규칙)로 자동 로드합니다. 가장 간편하고 일관된 코드 생성 방법입니다.

> [!NOTE]
> **준비 완료 안내**: 본 실습용 리포지토리에는 아래 규칙 파일(`.agents/rules/gemma4_hands_on.md`)이 이미 기본으로 생성되어 제공됩니다. 따라서 파일 생성 단계를 건너뛰고 바로 `step 2` 명령어 실행 단계로 넘어가시면 됩니다.

### step 1. 규칙 파일 생성 (리포지토리에 기본 포함됨)
프로젝트 루트 폴더에 `.agents/rules/` 디렉토리를 만들고, 실습용 규칙 파일(예: `gemma4_hands_on.md`)을 작성합니다.

*   **파일 경로:** `.agents/rules/gemma4_hands_on.md`
*   **파일 내용:** (앞서 정의한 시스템 프롬프트를 규칙 문서화합니다)
    ```markdown
    # Gemma 4 핸즈온 코드 생성 규칙
    
    이 작업 공간에서 파이썬 LLM 연동 코드를 생성할 때는 반드시 다음 규칙을 준수해야 합니다:
    
    1. HTTP 클라이언트 라이브러리로 requests 대신 `httpx`를 사용할 것.
    2. 가볍고 빠른 비동기(Async) 또는 동기(Sync) 코드를 선택적으로 제공할 것.
    3. 로컬 API 환경 설정을 소스코드 하드코딩이 아닌 환경변수(`os.getenv`)를 통해 유연하게 주입할 것:
       - `LLM_PROVIDER`: 'ollama' | 'lmstudio' | 'llamacpp' (기본값: 'ollama')
       - `LLM_API_URL`: 서버 Base URL (기본값은 제공자별 기본 포트 기준 자동 매핑)
       - `LLM_MODEL`: 호출할 모델 이름 (기본값: 'gemma4:e4b')
    4. Gemma 4 모델의 생각 과정(Thinking/Reasoning)을 파싱하여 화면에 시각적으로 구분하여 표시할 것:
       - 스트리밍 출력 시 `<think>` 태그가 감지되면 화면에 `[생각 과정 시작...]` 문구와 함께 회색 색상 코드로 출력하고, `</think>`를 만나면 일반 답변 출력으로 복귀할 것.
    5. 로컬 서버 연결이 끊겼거나 접속이 안 될 때 상세한 에러 핸들링 코드를 포함할 것.
    6. 파일 저장 위치 제약사항:
       - 작성된 코드는 반드시 이 워크스페이스 내의 `hands-on/main.py` 파일 경로에 생성하거나 기존 내용을 완전히 덮어써서 업데이트해야 합니다. 다른 임시 파일이나 루트 경로에 생성해서는 안 됩니다.
    7. 환경변수 파일 자동 로드:
       - 실습 폴더의 환경변수 설정 파일(`.env`)을 정상적으로 읽어올 수 있도록, 소스코드 시작 부분에 `python-dotenv` 라이브러리의 `load_dotenv()` 호출을 반드시 포함시켜야 합니다.
    ```

### step 2. agy CLI로 코드 생성 명령 실행
터미널을 열고 프로젝트 루트에서 `agy` 명령어를 직접 호출하여 필요한 코드를 파일로 생성하도록 요청합니다. `agy`는 에이전트이므로 파일을 직접 쓰고 수정할 수 있습니다.

```bash
agy "Ollama에서 gemma4:e4b 모델을 호출하고 생각 과정(thinking)과 답변을 httpx로 처리하는 파이썬 코드를 hands-on/main.py에 생성해줘"
```

*   **동작 원리:** `agy` CLI가 가동되면서 `.agents/rules/gemma4_hands_on.md`에 설정된 제약조건을 자동으로 읽어들이고, 이에 맞춰 `hands-on/main.py` 파일을 자동으로 생성해 줍니다.

---

## 2. 방법 B: 커스텀 에이전트 (Custom Agent) 정의하기

특정 역할만을 담당하는 전용 에이전트 가상 구성을 사용하고 싶다면, 프로젝트 내에 `agent.json` 파일을 작성하여 시스템 프롬프트를 고정할 수 있습니다.

> [!NOTE]
> **준비 완료 안내**: 본 실습용 리포지토리에는 아래 에이전트 정의 파일(`.agents/agents/gemma-coder/agent.json`)이 이미 기본으로 생성되어 제공됩니다. 따라서 파일 생성 단계를 건너뛰고 바로 `step 2` 명령어 실행 단계로 넘어가시면 됩니다.

### step 1. 에이전트 정의 파일 생성 (리포지토리에 기본 포함됨)
프로젝트 폴더 내에 에이전트 설정 디렉토리를 생성하고 `agent.json` 파일을 설정합니다.

*   **파일 경로:** `.agents/agents/gemma-coder/agent.json`
*   **파일 내용:**
    ```json
    {
      "name": "gemma-coder",
      "description": "Gemma 4 로컬 개발용 httpx 실습 코드를 규칙에 맞춰 전문적으로 빌드하는 에이전트",
      "systemPromptSections": [
        "역할: 너는 로컬 LLM 통합에 특화된 시니어 파이썬 개발자야.",
        "작성 목표: 로컬에 기동된 Gemma 4 API 서버(Ollama, LM Studio, llama.cpp)에 맞춰 비동기 또는 동기 방식으로 추론하고, 스트리밍 응답과 모델의 생각 과정(Reasoning/Thinking)을 구분해 출력해 주는 파이썬 스크립트를 작성해 줘.",
        "반드시 지켜야 할 제약사항:",
        "1. HTTP 클라이언트 라이브러리로 requests 대신 'httpx'를 사용할 것.",
        "2. 가볍고 빠른 비동기(Async) 또는 동기(Sync) 코드를 선택적으로 제공할 것.",
        "3. 로컬 API 환경 설정을 소스코드 하드코딩이 아닌 '환경변수(os.environ)'를 통해 유연하게 주입할 것: (LLM_PROVIDER, LLM_API_URL, LLM_MODEL)",
        "4. Gemma 4 모델의 생각 과정(Thinking/Reasoning)을 파싱하여 화면에 시각적으로 구분하여 표시할 것: 스트리밍 출력 시 <think> 태그가 감지되면 화면에 '[생각 과정 시작]' 문구와 함께 회색이나 다른 텍스트 스타일로 출력하고, </think>를 만나면 일반 답변 출력으로 전환해 줄 것.",
        "5. 로컬 서버 연결이 끊겼거나 접속이 안 될 때 상세한 에러 핸들링 코드를 포함할 것.",
        "6. 파일 저장 위치 제약사항: 이 코드는 반드시 이 워크스페이스 내의 'hands-on/main.py' 파일로 작성(또는 덮어쓰기)해야 해. 다른 경로에 생성하면 안 돼.",
        "7. 환경변수 파일 자동 로드: 실습 폴더의 환경변수 설정 파일('.env')을 정상적으로 읽어올 수 있도록, 소스코드 시작 부분에 `python-dotenv` 라이브러리의 `load_dotenv()` 호출을 반드시 포함시켜 줘."
      ]
    }
    ```

### step 2. 커스텀 에이전트 지정 호출
`--agent` 플래그를 사용하여 생성해 둔 에이전트를 지정하고 질문을 전달합니다. 본 실습 공간에는 아래와 같이 총 5가지 에이전트가 사전 구성되어 있습니다:

#### 0) Flutter/DartPad 웜업 에이전트 (`flutter-coder`)
```bash
agy --agent flutter-coder "google_fonts와 fl_chart를 이용한 개인 자산 대시보드 앱을 작성해줘"
```

#### 1) 기본 대화 스트리밍 에이전트 (`gemma-coder`)
```bash
agy --agent gemma-coder "비동기 대화 스트리밍 및 생각 과정 파싱 실습 코드를 작성해줘"
```

#### 2) Function Calling 에이전트 (`gemma-fc`)
```bash
agy --agent gemma-fc "날씨 조회 도구 호출을 수행하는 Function Calling 비동기 실습 코드를 작성해줘"
```

#### 3) Structured Output 에이전트 (`gemma-so`)
```bash
agy --agent gemma-so "특정 개발자 프로필 규격에 맞게 JSON을 스트리밍 출력하고 검증하는 비동기 실습 코드를 작성해줘"
```

#### 4) 생각 과정 토글 에이전트 (`gemma-tt`)
```bash
agy --agent gemma-tt "CLI 플래그에 따라 생각 과정 출력을 필터링하여 노출을 켜고 끄는 비동기 실습 코드를 작성해줘"
```

---

## 3. 설정 확인 및 디버깅

내가 작성한 작업 공간 규칙과 커스텀 에이전트가 `agy` CLI에 정상적으로 로드되었는지 확인하려면 다음 명령을 실행합니다:

```bash
agy inspect
```

*   **확인 사항:** 
    *   `Workspace Rules` 항목에 `gemma4_hands_on.md`, `gemma4_fc.md`, `gemma4_so.md`, `gemma4_tt.md`, `gemma4_flutter.md` 규칙 파일들이 정상 등록되어 있는지 확인합니다.
    *   `Custom Agents`에 `gemma-coder`, `gemma-fc`, `gemma-so`, `gemma-tt`, `flutter-coder` 에이전트가 목록에 노출되는지 확인합니다.

이제 `agy` CLI의 강력한 자율 에이전트 기능을 활용해 Gemma 4 핸즈온 준비를 쉽고 빠르게 수행할 수 있습니다!
[목차로 돌아가기](../docs/README.md)
