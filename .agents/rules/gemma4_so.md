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
7. 터미널 인터랙티브 대화 루프 구현:
   - 일회성 실행이 아닌, 터미널에서 사용자 입력을 대기하고 입력이 들어오면 API를 호출해 스트리밍으로 결과를 출력하는 반복 루프(Interactive Loop)로 설계할 것.
   - 프롬프트 입력 대기 시 "User (프로필을 생성할 인물 이름): "와 같이 명확히 대기 상태를 보여줄 것.
   - 사용자가 'exit' 또는 'quit'을 입력하면 대화 루프를 종료하고 프로그램을 끝낼 것.
8. 로컬 서버 연결이 끊겼거나 접속이 안 될 때 상세한 에러 핸들링 코드를 포함할 것. 또한 키보드 종료(Ctrl+C, KeyboardInterrupt) 발생 시 트레이스백 없이 깔끔한 안내 메시지('[실행 중단] 사용자에 의해 프로그램이 종료되었습니다.')를 출력하고 정상 종료(sys.exit(0))되도록 예외 처리를 포함할 것.
9. 파일 저장 위치 제약사항:
   - 작성된 코드는 반드시 이 워크스페이스 내의 `hands-on/structured_output.py` 파일 경로에 생성하거나 기존 내용을 완전히 덮어써서 업데이트해야 합니다. 다른 임시 파일이나 루트 경로에 생성해서는 안 됩니다.
10. 환경변수 파일 자동 로드:
    - 실습 폴더의 환경변수 설정 파일(`.env`)을 정상적으로 읽어올 수 있도록, 소스코드 시작 부분에 `python-dotenv` 라이브러리의 `load_dotenv()` 호출을 반드시 포함시켜야 합니다.

