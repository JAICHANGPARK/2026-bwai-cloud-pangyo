# LM Studio 설치 및 Gemma 4 모델 준비 가이드

[LM Studio](https://lmstudio.ai/)는 로컬 환경에서 GGUF 포맷의 LLM을 탐색, 다운로드, 실행할 수 있는 완성도 높은 GUI 데스크톱 애플리케이션입니다. 터미널 조작 없이 깔끔한 그래픽 사용자 인터페이스(GUI)를 통해 모델과 채팅하거나, 로컬 OpenAI 호환 API 서버를 마우스 클릭만으로 열고 싶으신 분들께 적극 권장합니다.

> [!WARNING]
> **인텔 맥(Intel Mac) 미지원 안내:**
> LM Studio 최신 버전은 인텔 맥(Intel CPU 탑재 macOS 기기)을 공식적으로 지원하지 않거나 실행 시 정상 작동하지 않을 수 있습니다. 인텔 맥 사용자는 LM Studio 대신 [**Ollama 설치 가이드**](./ollama_guide.md) 혹은 [**llama.cpp 빌드 가이드**](./llamacpp_guide.md)를 사용하여 Gemma 4 모델을 구동하는 것을 강력히 권장합니다.

---

## LM Studio 설치 방법

### 1. 다운로드 및 설치
1. [LM Studio 공식 웹사이트](https://lmstudio.ai/)에 접속합니다.
2. 사용 중인 운영체제(OS)에 맞는 설치 파일을 선택해 다운로드합니다:
   *   **macOS (Apple Silicon):** Apple Silicon Mac 전용 (M 시리즈, Metal 하드웨어 가속 지원)
   *   **macOS (Intel CPU):** (지원 제한) 인텔 칩셋 탑재 맥은 공식 실행이 지원되지 않거나 성능이 원활하지 않습니다. (Ollama/llama.cpp 권장)
   *   **Windows:** Windows 10/11 전용 (Nvidia CUDA / AMD ROCm 가속 지원)
3. 다운로드 완료 후 설치 프로그램을 실행합니다:
   *   **macOS:** DMG 파일을 더블 클릭하여 `LM Studio.app`을 **응용 프로그램(Applications)** 폴더로 드래그합니다.
   *   **Windows:** 다운로드된 `.exe` 파일을 실행하여 가이드에 따라 설치합니다.

---

## Gemma 4 GGUF 모델 검색 및 다운로드

LM Studio를 실행한 후 앱 내에서 직접 허깅페이스(Hugging Face)에 등록된 Gemma 4 GGUF 파일을 검색하고 내려받을 수 있습니다.

1. **모델 검색 창으로 이동:** LM Studio 좌측 메뉴 바의 **돋보기 아이콘(Search)을** 클릭합니다.
2. **모델 검색:** 상단 검색창에 `gemma-4`를 입력하고 엔터를 누릅니다.
3. **업로더/레포지토리 선택:** 검색 결과 목록에서 신뢰도 높은 업로더(예: `bartowski`, `unsloth` 또는 공식 Google 저장소)의 저장소를 선택합니다.
   *   **Gemma 4 E4B (16GB RAM 이상 권장):** `gemma-4-E4B-it-GGUF` 또는 `gemma-4-E4B-it`가 포함된 결과를 선택합니다.
   *   **Gemma 4 E2B (8GB RAM 이하 권장):** `gemma-4-E2B-it-GGUF` 또는 `gemma-4-E2B-it`가 포함된 결과를 선택합니다.
4. **양자화 버전(Quantization) 선택 및 다운로드:** 우측 파일 목록에서 원하는 양자화 크기 옆의 **Download** 버튼을 누릅니다.
   *   **추천 파일:** `Q4_K_M` (속도와 정밀도의 밸런스가 가장 좋습니다) 또는 `Q8_0` (고화질 모델이지만 용량이 조금 더 큽니다).
   *   *예: `bartowski/gemma-4-E4B-it-GGUF`에서 `gemma-4-e4b-it-Q4_K_M.gguf`를 다운로드.*

---

## 로컬 채팅 테스트

다운로드가 완료되면 LM Studio 내에서 바로 대화를 시작할 수 있습니다.

1. 좌측 메뉴에서 **말풍선 아이콘(AI Chat)을** 클릭하여 채팅 화면으로 이동합니다.
2. 화면 상단 중앙의 **Select a model to load** 드롭다운 메뉴를 클릭합니다.
3. 방금 다운로드한 `gemma-4-e4b-it` (혹은 `e2b`) 모델을 클릭하여 메모리에 로드합니다.
   *   오른쪽 사이드바의 **Hardware Settings**에서 GPU 가속(GPU Offload)이 켜져 있는지 확인하세요. Apple Silicon Mac의 경우 `Metal`이 자동으로 활성화되어 하드웨어 가속이 진행됩니다.
4. 하단 채팅 입력창에 한국어로 질문을 해보고 답변 속도와 작동 여부를 테스트합니다.
   *   *예: "오늘 서울 판교 날씨가 어때? (예상 시나리오 질문)" 또는 "파이썬으로 퀵 정렬 코드를 짜줘"*

---

## 로컬 API 서버 활성화 (OpenAI 호환)

LM Studio는 로컬에서 작동하는 Gemma 4 모델을 외부 애플리케이션이나 코드(예: Python SDK, Web UI 등)에서 호출할 수 있도록 OpenAI 규격과 100% 호환되는 API 서버 기능을 제공합니다.

1. 좌측 메뉴에서 **이중 플러그 아이콘(Local Server)을** 클릭합니다.
2. 상단 드롭다운에서 Gemma 4 모델이 선택되어 있는지 확인합니다.
3. 우측 설정 창에서 포트 번호(기본값: `1234`)를 확인하고, **Start Server** 버튼을 누릅니다.
4. 서버가 켜지면 아래와 같이 `http://localhost:1234/v1` 경로로 OpenAI SDK 스타일의 요청을 수신할 수 있게 됩니다.

### Python 연동 예시 코드:
```python
from openai import OpenAI

# 로컬 LM Studio 서버 주소로 클라이언트 설정
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

completion = client.chat.completions.create(
    model="gemma-4-e4b-it", # 로드된 모델명
    messages=[
        {"role": "system", "content": "너는 판교 AI 행사 가이드야."},
        {"role": "user", "content": "Gemma 4의 주요 장점을 알려줘."}
    ],
    temperature=0.7,
)

print(completion.choices[0].message.content)
```

이제 LM Studio를 사용한 Gemma 4 개발 준비가 완료되었습니다!
[목차로 돌아가기](./README.md)
