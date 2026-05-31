# Gemma 4 핸즈온 - Structured Output 코드 생성 규칙

이 작업 공간에서 파이썬 LLM Structured Output 코드를 생성할 때는 반드시 다음 규칙을 준수해야 합니다:

1. HTTP 클라이언트 라이브러리로 requests 대신 `httpx`를 사용할 것.
2. 비동기(Async) 코드로 작성하고, 실시간 토큰 출력을 보장하기 위해 스트리밍(stream=True) 방식으로 답변을 가져올 것.
3. 시스템 메시지를 구성할 때 JSON 스키마 제약 조건을 포함할 것. (필드: `name`, `role`, `skills`, `experience_years`)
4. 로컬 API 환경 설정을 소스코드 하드코딩이 아닌 환경변수(`os.getenv`)를 통해 유연하게 주입할 것:
   - `LLM_PROVIDER`: 'ollama' | 'lmstudio' | 'llamacpp' (기본값: 'ollama')
   - `LLM_API_URL`: 서버 Base URL (기본값은 제공자별 기본 포트 기준 자동 매핑)
   - `LLM_MODEL`: 호출할 모델 이름 (기본값: 'gemma4:e4b')
5. 제공자별 JSON 모드 설정 매핑:
   - Ollama: API 요청 페이로드에 `"format": "json"` 옵션 추가
   - LM Studio, llama.cpp: API 요청 페이로드에 `"response_format": {"type": "json_object"}` 옵션 추가
6. 데이터 수신 완료 후, 누적된 텍스트를 `json.loads`를 사용해 파싱 검증하고 정상 구조로 파싱되는지 검증 결과를 화면에 출력할 것.
7. 파일 저장 위치 제약사항:
   - 작성된 코드는 반드시 이 워크스페이스 내의 `hands-on/structured_output.py` 파일 경로에 생성하거나 기존 내용을 완전히 덮어써서 업데이트해야 합니다. 다른 임시 파일이나 루트 경로에 생성해서는 안 됩니다.
8. 환경변수 파일 자동 로드:
   - 실습 폴더의 환경변수 설정 파일(`.env`)을 정상적으로 읽어올 수 있도록, 소스코드 시작 부분에 `python-dotenv` 라이브러리의 `load_dotenv()` 호출을 반드시 포함시켜야 합니다.
