# Gemma 4 로컬 연동 핸즈온 실습 가이드

이 폴더는 로컬에 기동된 Gemma 4 API 서버(Ollama, LM Studio, llama.cpp)와 연동하여 답변을 스트리밍하고 생각 과정을 파싱하는 실습 자료를 담고 있습니다.

---

## 폴더 구조 및 파일 설명

*   [system_prompt.txt](./system_prompt.txt): 다른 AI 모델(예: Gemini 등)에 입력하여 제약 조건에 맞는 코드를 자동 생성하기 위한 시스템 프롬프트 텍스트 파일입니다.
*   [main.py](./main.py): 환경변수를 읽고 로컬 서버(Ollama, LM Studio, llama.cpp)를 호출해 대화를 진행하는 비동기 파이썬 레퍼런스 코드입니다.

---

## 실습 진행 절차

### 1. 개발 환경 구성
[uv 설치 및 가상환경 구성 가이드](../docs/uv_guide.md)에 따라 개발 환경 및 패키지 설치(`uv add httpx openai python-dotenv`)를 완료해 주세요.

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

### 3. 실습 코드 실행
uv 가상환경이 활성화된 상태에서 아래 명령어를 실행하여 코드를 구동합니다.

```bash
# 기본 질문으로 실행
uv run main.py

# 질문을 변경하여 실행
uv run main.py "로컬 LLM을 연동할 때 HTTPX가 Requests 라이브러리보다 유리한 점은 무엇인가요?"
```

---

## 4. 시스템 프롬프트 활용하기
[system_prompt.txt](./system_prompt.txt)의 내용을 복사하여 생성형 AI(Gemini 등)의 시스템 지침 또는 프롬프트 입력창에 붙여넣은 뒤, "동기 방식으로 동작하는 Ollama용 실습 코드를 작성해 줘"와 같이 요구사항을 물어보면 제약 조건(`httpx` 사용, 생각 과정 파싱, 환경변수 연동 등)을 충족하는 최적의 코드를 얻을 수 있습니다.
[메인 목차로 돌아가기](../docs/README.md)
