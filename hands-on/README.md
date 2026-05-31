# 🚀 Gemma 4 로컬 연동 핸즈온 실습 가이드

이 폴더는 로컬에 기동된 Gemma 4 API 서버(Ollama, LM Studio, llama.cpp)와 연동하여 답변을 실시간으로 스트리밍하고, 생각 과정(Thinking)을 파싱하여 제어하는 실습 자료를 포함하고 있습니다.

---

## 📂 폴더 구조 및 실습 주제

### 0. Warmup: Flutter / DartPad 실습
*   [DartPad 사용 및 설정 가이드](../docs/dartpad_guide.md): 브라우저에서 플러터 앱을 빌드하고 실행하는 방법과 제약사항 설명서입니다.
*   [system_prompt_flutter.txt](./system_prompt_flutter.txt): DartPad에서 단일 파일로 동작하는 플러터 앱 생성을 위한 AI 시스템 프롬프트입니다.
*   [flutter_app.dart](./reference/flutter_app.dart): DartPad([dartpad.dev](https://dartpad.dev))에 복사해 실행해볼 수 있는 플러터 웰컴 앱 레퍼런스 (벽돌깨기 게임) 코드입니다.


### 1. 기본 스트리밍 & 생각 과정 파싱 실습
*   [system_prompt.txt](./system_prompt.txt): 기본 대화 스트리밍 및 생각 과정 분리 출력을 위한 AI 시스템 프롬프트입니다.
*   [main.py](./reference/main.py): 환경변수를 연동해 실시간 스트리밍 답변 및 생각 과정을 파싱하는 파이썬 레퍼런스 코드입니다.

### 2. Function Calling (도구 호출) 실습
*   [system_prompt_fc.txt](./system_prompt_fc.txt): 날씨 조회 도구를 바인딩하고 처리하는 코드를 생성하기 위한 AI 시스템 프롬프트입니다.
*   [function_calling.py](./reference/function_calling.py): 모델의 도구 호출 요청을 받아 로컬 함수를 실행한 후 최종 대답을 출력하는 레퍼런스 코드입니다.

### 3. Structured Output (구조화된 출력) 실습
*   [system_prompt_so.txt](./system_prompt_so.txt): 특정 JSON 스키마 규격으로 출력을 강제하고 파싱하는 코드를 생성하기 위한 AI 시스템 프롬프트입니다.
*   [structured_output.py](./reference/structured_output.py): JSON 모드를 활성화하고 수신된 JSON의 스키마 유효성을 검증하는 레퍼런스 코드입니다.

### 4. Thinking Toggle (생각 토글) 실습
*   [system_prompt_tt.txt](./system_prompt_tt.txt): 생각 과정을 API 레벨 및 클라이언트 필터링으로 켜고 끄며, 인터랙티브 루프를 지원하는 코드를 위한 AI 시스템 프롬프트입니다.
*   [thinking_toggle.py](./reference/thinking_toggle.py): CLI 플래그에 따라 생각 과정 출력을 콘솔에 노출하거나 완전히 가리는 제어 레퍼런스 코드입니다.

---

## 🛠️ 1. 개발 환경 및 환경변수 설정

### 개발 환경 구성
1. [uv 설치 및 가상환경 구성 가이드](../docs/uv_guide.md)에 따라 개발 환경을 구성합니다.
2. 터미널에서 `hands-on` 폴더로 이동하여 의존성 동기화를 진행합니다.
   ```bash
   cd hands-on
   uv sync
   ```

### 환경변수 설정 (`.env`)
`hands-on` 폴더 내에 `.env` 파일을 생성하고 아래 표를 참고하여 자신이 사용하는 로컬 API 서버 유형에 맞는 환경변수를 지정합니다.

| 환경변수 | Ollama 환경 | LM Studio 환경 | llama.cpp 환경 | 기본값 |
| :--- | :--- | :--- | :--- | :--- |
| **`LLM_PROVIDER`** | `ollama` | `lmstudio` | `llamacpp` | `ollama` |
| **`LLM_MODEL`** | `gemma4:e4b` (혹은 로컬 모델명) | 다운로드받은 모델 식별자 (예: `google/gemma-4-e2b`) | 다운로드받은 모델 식별자 | `gemma4:e4b` |
| **`LLM_API_URL`** | `http://localhost:11434` | `http://localhost:1234/v1` | `http://localhost:8080/v1` | 제공자별 기본 URL 자동 매핑 |

#### 예시 `.env` 파일 구성:

**LM Studio를 사용하는 경우:**
```env
LLM_PROVIDER=lmstudio
LLM_MODEL=google/gemma-4-e2b
LLM_API_URL=http://localhost:1234/v1
```

**Ollama를 사용하는 경우:**
```env
LLM_PROVIDER=ollama
LLM_MODEL=gemma4:e4b
LLM_API_URL=http://localhost:11434
```

---

## 🤖 2. 프롬프트를 통한 코드 생성 방법

각 실습 주제에 맞춤 제공되는 **시스템 프롬프트 텍스트 파일**의 내용을 복사하여 AI 어시스턴트(예: Gemini, Cursor, Copilot 등)에 주입하고 코드를 생성하도록 지시합니다.

> [!TIP]
> **AI 어시스턴트에게 코드를 작성해달라고 프롬프트를 입력하는 방법:**
> 1. 사용할 주제의 시스템 프롬프트 내용(예: `system_prompt_tt.txt`)을 전체 복사합니다.
> 2. AI 어시스턴트 대화창에 복사한 내용을 붙여넣으며 아래 명령조를 추가합니다:
>    - *"이 시스템 프롬프트 지침에 맞춰서 로컬 LLM 연동 코드를 구현해줘."*
>    - *"작성된 결과는 지정된 파일 경로(예: `hands-on/thinking_toggle.py`)에 정확히 저장하거나 코드로 제공해줘."*
> 3. AI 어시스턴트가 생성한 완성본 코드를 실습 루트에 해당 파일명으로 저장합니다.

---

## 🏃 3. 생성된 실습 코드 실행 방법

코드가 올바르게 생성되었는지 확인하기 위해 아래 명령어를 입력하여 각 실습을 구동합니다. (작성한 코드 실행 시에는 레퍼런스가 아닌 생성한 코드 파일명으로 바로 실행합니다.)

### 0) Flutter / DartPad 실습
1. [system_prompt_flutter.txt](./system_prompt_flutter.txt) 내용을 복사해 프롬프트로 주입 후 플러터 코드를 요청합니다.
2. 생성된 코드 전체를 복사하여 [dartpad.dev](https://dartpad.dev)에 붙여넣고 **Run** 버튼을 눌러 브라우저에서 실행합니다. (자세한 브라우저 실행 가이드 및 주의사항은 [DartPad 사용 및 설정 가이드](../docs/dartpad_guide.md)를 참고해 주세요.)

### 1) 기본 대화 스트리밍 & 생각 파싱 실습 (`main.py`)
사용자와 터미널 상에서 주고받는 인터랙티브 대화 루프로 실행됩니다.
```bash
# 대화 루프 실행
uv run main.py

# CLI 인자로 즉시 1회성 질문 실행
uv run main.py "지구에서 가장 높은 산은 어디인가요?"
```

### 2) Function Calling 실습 (`function_calling.py`)
로컬 날씨 조회 API 도구가 정상적으로 바인딩 및 매핑되는지 확인합니다.
```bash
# 날씨 질문을 하여 내부 함수 호출 작동 검증
uv run function_calling.py "오늘 서울과 부산의 날씨가 어때?"
```

### 3) Structured Output 실습 (`structured_output.py`)
정해진 JSON 형식(Schema)으로 모델이 결과값을 강제 출력하고 검증하는지 확인합니다.
```bash
# 구조화된 출력 테스트 실행
uv run structured_output.py "대한민국의 수도, 인구수, 대표 명소 3곳을 알려줘."
```

### 4) Thinking Toggle (생각 과정 켜기/끄기) 실습 (`thinking_toggle.py`)
생각 과정을 콘솔에 회색 텍스트로 노출하거나 완전히 보이지 않게 클라이언트 필터링을 조절할 수 있습니다.

*   **생각 기능 켜기 (ON 모드 - 기본값)**:
    인터랙티브 루프나 CLI 1회 질문 시 생각 과정을 구분하여 시각적으로 보여줍니다.
    ```bash
    # 대화형 대화 루프 실행 (생각 노출)
    uv run thinking_toggle.py
    
    # CLI 모드로 즉시 실행
    uv run thinking_toggle.py "17 * 39 + 128 / 4 - 83은 무엇인가요?"
    ```

*   **생각 기능 끄기 (OFF 모드 - 필터링)**:
    `--no-think` 플래그를 추가하면 생각 과정을 생략하고 핵심 답변만 출력합니다.
    ```bash
    # 대화형 대화 루프 실행 (생각 가림)
    uv run thinking_toggle.py --no-think
    
    # CLI 모드로 즉시 실행
    uv run thinking_toggle.py --no-think "17 * 39 + 128 / 4 - 83은 무엇인가요?"
    ```

---

## 💡 참고 사항 (정답 코드 확인)
스스로 프롬프트를 통해 코드를 작성하다가 막히는 경우, [reference](./reference/) 폴더 안에 사전 제공된 정답 코드를 실행하여 비교 대조해볼 수 있습니다.
```bash
# 예시: 레퍼런스 생각 토글 코드 실행
uv run reference/thinking_toggle.py --no-think "15 * 15는?"
```
