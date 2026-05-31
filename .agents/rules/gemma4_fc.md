# Gemma 4 핸즈온 - Function Calling 코드 생성 규칙

이 작업 공간에서 파이썬 LLM Function Calling 코드를 생성할 때는 반드시 다음 규칙을 준수해야 합니다:

1. HTTP 클라이언트 라이브러리로 requests 대신 `httpx`를 사용할 것.
2. 비동기(Async) 코드로 작성하고, 1단계(도구 판단 및 실행)는 비스트리밍(stream=False), 2단계(최종 답변 생성)는 스트리밍(stream=True)으로 동작하도록 구성할 것.
3. 실습용 도구로 `get_current_weather(location)` 함수를 정의하고, 도구 메타데이터 정의(`tools`) 및 바인딩을 포함할 것. 이 함수는 무료 날씨 API 서비스인 `wttr.in`을 호출(`https://wttr.in/{location}?format=j1`)하여 실시간 온도(`temp_C`), 날씨 상태(`weatherDesc`), 습도(`humidity`) 정보를 딕셔너리로 반환하도록 구현할 것.
4. 로컬 API 환경 설정을 소스코드 하드코딩이 아닌 환경변수(`os.getenv`)를 통해 유연하게 주입할 것:
   - `LLM_PROVIDER`: 'ollama' | 'lmstudio' | 'llamacpp' (기본값: 'ollama')
   - `LLM_API_URL`: 서버 Base URL (기본값은 제공자별 기본 포트 기준 자동 매핑)
   - `LLM_MODEL`: 호출할 모델 이름 (기본값: 'gemma4:e4b')
5. Ollama의 네이티브 도구 호출 응답 구조와 OpenAI 호환 규격(LM Studio, llama.cpp)의 응답 구조를 각각 분기 처리하여 완벽히 대응할 것.
6. 로컬 서버 연결이 끊겼거나 접속이 안 될 때 상세한 에러 핸들링 코드를 포함할 것. 또한 키보드 종료(Ctrl+C, KeyboardInterrupt) 발생 시 트레이스백 없이 깔끔한 안내 메시지('[실행 중단] 사용자에 의해 프로그램이 종료되었습니다.')를 출력하고 정상 종료(sys.exit(0))되도록 예외 처리를 포함할 것.
7. 파일 저장 위치 제약사항:
   - 작성된 코드는 반드시 이 워크스페이스 내의 `hands-on/function_calling.py` 파일 경로에 생성하거나 기존 내용을 완전히 덮어써서 업데이트해야 합니다. 다른 임시 파일이나 루트 경로에 생성해서는 안 됩니다.
8. 환경변수 파일 자동 로드:
   - 실습 폴더의 환경변수 설정 파일(`.env`)을 정상적으로 읽어올 수 있도록, 소스코드 시작 부분에 `python-dotenv` 라이브러리의 `load_dotenv()` 호출을 반드시 포함시켜야 합니다.
