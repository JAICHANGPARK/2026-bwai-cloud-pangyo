# Gemma 4 로컬 연동 핸즈온 실습 가이드

이 폴더는 로컬에 기동된 Gemma 4 API 서버(Ollama, LM Studio, llama.cpp)와 연동하여 답변을 스트리밍하고 생각 과정을 파싱하는 실습 자료를 담고 있습니다.

---

## 폴더 구조 및 파일 설명

### 0. Warmup: Flutter / DartPad 실습
*   [system_prompt_flutter.txt](./system_prompt_flutter.txt): DartPad에서 단일 파일로 동작하는 플러터 앱 생성을 위한 AI 시스템 프롬프트입니다.
*   [flutter_app.dart](./reference/flutter_app.dart): DartPad(dartpad.dev)에 복사해 실행할 수 있는 플러터 웰컴 앱 레퍼런스 코드입니다.

### 1. 기본 스트리밍 & 생각 과정 파싱 실습
*   [system_prompt.txt](./system_prompt.txt): 기본 스트리밍 및 생각 과정 분리 출력을 위한 AI 시스템 프롬프트입니다.
*   [main.py](./reference/main.py): 환경변수를 연동해 실시간 스트리밍 답변 및 생각 과정을 파싱하는 파이썬 레퍼런스 코드입니다.

### 2. Function Calling (도구 호출) 실습
*   [system_prompt_fc.txt](./system_prompt_fc.txt): 날씨 조회 도구를 바인딩하고 처리하는 코드를 생성하기 위한 AI 시스템 프롬프트입니다.
*   [function_calling.py](./reference/function_calling.py): 모델의 도구 호출 요청을 받아 로컬 함수를 실행한 후 최종 대답을 출력하는 레퍼런스 코드입니다.

### 3. Structured Output (구조화된 출력) 실습
*   [system_prompt_so.txt](./system_prompt_so.txt): 특정 JSON 스키마 규격으로 출력을 강제하고 파싱하는 코드를 생성하기 위한 AI 시스템 프롬프트입니다.
*   [structured_output.py](./reference/structured_output.py): JSON 모드를 활성화하고 수신된 JSON의 스키마 유효성을 검증하는 레퍼런스 코드입니다.

### 4. Thinking Toggle (생각 토글) 실습
*   [system_prompt_tt.txt](./system_prompt_tt.txt): 생각 과정을 API 레벨 및 클라이언트 필터링으로 켜고 끄는 코드를 생성하기 위한 AI 시스템 프롬프트입니다.
*   [thinking_toggle.py](./reference/thinking_toggle.py): CLI 플래그에 따라 생각 과정 출력을 콘솔에 노출하거나 완전히 가리는 제어 레퍼런스 코드입니다.

---

## 실습 진행 절차

### 1. 개발 환경 구성
[uv 설치 및 가상환경 구성 가이드](../docs/uv_guide.md)에 따라 개발 환경 구성을 완료해 주세요. (가상환경 활성화 후 `uv sync`를 실행해 실습에 필요한 패키지 동기화를 완료합니다.)

### 2. 환경변수 설정 파일 생성 (`.env`)
`hands-on` 폴더 내에 `.env` 파일을 새로 생성하고 본인이 사용 중인 로컬 API 서버와 다운로드받은 모델 크기에 맞춰 아래 양식 중 하나를 복사하여 설정합니다.

#### Ollama 사용 시:
```env
LLM_PROVIDER=ollama
LLM_MODEL=gemma4:e4b
```

#### LM Studio 사용 시:
```env
LLM_PROVIDER=lmstudio
LLM_MODEL=gemma-4-e4b-it
```

#### llama.cpp 사용 시:
```env
LLM_PROVIDER=llamacpp
LLM_MODEL=gemma-4-e4b-it
```

### 3. 실습 코드 실행 (레퍼런스 코드)
터미널에서 `hands-on` 폴더로 이동한 후 각 실습 주제별 레퍼런스(정답) 코드를 아래 명령어로 구동할 수 있습니다.

```bash
# hands-on 폴더로 이동 (이미 이동했다면 생략 가능)
cd hands-on

# 1. 기본 스트리밍 + 생각 파싱 레퍼런스 실행
uv run reference/main.py

# 2. Function Calling 레퍼런스 실행
uv run reference/function_calling.py

# 3. Structured Output 레퍼런스 실행
uv run reference/structured_output.py

# 4. 생각 과정 토글 레퍼런스 실행 (ON 모드)
uv run reference/thinking_toggle.py

# 4. 생각 과정 토글 레퍼런스 실행 (OFF 모드 - 생각 출력 안 함)
uv run reference/thinking_toggle.py --no-think "17 * 39 + 128 / 4 - 83은 무엇인가요?"
```

---

## 4. 시스템 프롬프트 활용하여 코드 생성 및 실행하기
본인의 선호하는 AI 어시스턴트(예: Gemini, Cursor, 또는 `agy` 에이전트 CLI)의 지침 또는 프롬프트에 실습용 시스템 프롬프트 파일들의 내용을 입력하여 각 실습별 코드를 직접 생성해 봅니다.

### (0) Warmup: Flutter / DartPad 실습
1. [system_prompt_flutter.txt](./system_prompt_flutter.txt)의 내용을 복사해 프롬프트로 주입합니다.
2. AI 도구에 "구글 폰트를 사용한 깔끔한 할 일 관리(Todo) 앱을 만들어줘" 또는 "fl_chart를 활용한 개인 자산 대시보드 앱을 작성해줘"와 같이 원하는 Flutter 앱 코드를 요청합니다.
3. AI 에이전트(`agy` 등)를 사용하는 경우 `hands-on/flutter_app.dart`에 코드가 자동 생성됩니다.
4. 실행 방법: 생성된 코드 전체를 복사하여 [dartpad.dev](https://dartpad.dev)에 붙여넣고 우상단의 **Run** 버튼을 눌러 브라우저에서 실행합니다.

### (1) 기본 대화 스트리밍 & 생각 과정 분리 실습
1. [system_prompt.txt](./system_prompt.txt)의 내용을 복사해 프롬프트로 주입합니다.
2. AI 도구에 "로컬 연동 실습 코드를 작성해줘"라고 요청하면 `hands-on/main.py`에 코드가 생성됩니다.
3. 실행 방법: `uv run main.py`

### (2) Function Calling (도구 호출) 실습
1. [system_prompt_fc.txt](./system_prompt_fc.txt)의 내용을 복사해 프롬프트로 주입합니다.
2. AI 도구에 "Function Calling 실습 코드를 작성해줘"라고 요청하면 `hands-on/function_calling.py`에 코드가 생성됩니다.
3. 실행 방법: `uv run function_calling.py`

### (3) Structured Output (구조화된 출력) 실습
1. [system_prompt_so.txt](./system_prompt_so.txt)의 내용을 복사해 프롬프트로 주입합니다.
2. AI 도구에 "Structured Output 실습 코드를 작성해줘"라고 요청하면 `hands-on/structured_output.py`에 코드가 생성됩니다.
3. 실행 방법: `uv run structured_output.py`

### (4) Thinking Toggle (생각 과정 켜기/끄기) 실습
1. [system_prompt_tt.txt](./system_prompt_tt.txt)의 내용을 복사해 프롬프트로 주입합니다.
2. AI 도구에 "생각 기능 토글 실습 코드를 작성해줘"라고 요청하면 `hands-on/thinking_toggle.py`에 코드가 생성됩니다.
3. 실행 방법 (ON): `uv run thinking_toggle.py`
4. 실행 방법 (OFF): `uv run thinking_toggle.py --no-think`

[메인 목차로 돌아가기](../docs/README.md)
