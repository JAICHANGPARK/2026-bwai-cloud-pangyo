# Build with AI Cloud x Pangyo 2026
## Gemma 4 Hands-on Session 사전 준비 가이드

본 가이드는 **Build with AI Cloud x Pangyo 2026** 행사의 **Gemma 4 핸즈온 세션**에 참석하시는 분들이 개인 노트북에 필요한 도구와 AI 모델을 미리 설치하여 원활하게 세션에 참여하실 수 있도록 돕기 위해 작성되었습니다.

> [!IMPORTANT]
> 원활한 핸즈온 진행을 위해 **행사 참석 전(5월 31일 이전)에** 본 가이드를 따라 설치와 모델 다운로드를 완료해 주시기 바랍니다. 온라인 세션 진행 중 실시간으로 다운로드할 경우 시간이 오래 걸리거나 연결이 불안정할 수 있습니다.

---

## 행사 정보
*   **일시:** 2026년 5월 31일 (일요일) 오후 2:00 ~ 오후 4:00 (GMT+9)
*   **장소:** 온라인 (접속 링크는 신청 페이지 및 등록 이메일 참고)
*   **행사 신청 및 상세 안내 링크:**
    *   [GDG Cloud Korea 공식 커뮤니티 페이지](https://gdg.community.dev/events/details/google-gdg-cloud-korea-presents-build-with-ai-cloud-x-pangyo-2026/cohost-gdg-cloud-korea/)
    *   [Luma 신청 페이지](https://luma.com/65d0o32r)

---

## 내 컴퓨터에 맞는 Gemma 4 모델 추천
Gemma 4는 구글 딥마인드에서 2026년 4월에 출시한 모바일/온디바이스 최적화 경량 멀티모달 모델 패밀리입니다. 사용하시는 컴퓨터의 메모리(RAM) 용량에 맞춰 적절한 모델을 사전에 다운로드해 주세요.

| 시스템 메모리 (RAM) | 권장 Gemma 4 모델 크기 | 모델 식별자 (Ollama / GGUF) | 비고 |
| :--- | :--- | :--- | :--- |
| **8 GB** | **Gemma 4 E2B** (Effective 2B) | `gemma4:e2b` / `gemma-4-E2B-it-GGUF` | 메모리가 제한적인 PC/랩톱 최적화 |
| **16 GB 이상** | **Gemma 4 E4B** (Effective 4B) | `gemma4:e4b` / `gemma-4-E4B-it-GGUF` | 권장 스펙, 균형 잡힌 코딩/Reasoning 성능 |

> [!TIP]
> *   **E2B (Effective 2B):** 20억 매개변수 모델로, 속도가 매우 빠르며 메모리가 부족한 인텔 맥북이나 8GB 램 윈도우 노트북에 권장됩니다.
> *   **E4B (Effective 4B):** 40억 매개변수 모델로, Apple Silicon Mac (M 시리즈) 16GB 이상이나 외장 GPU가 탑재된 윈도우 PC에서 쾌적하게 동작하며 더 높은 답변 퀄리티를 제공합니다.

---

## 도구별 사전 준비 가이드
사용 환경이나 선호하는 도구에 맞춰 아래 세 가지 설치 가이드 중 하나를 선택해 진행해 주세요. (가장 대중적이고 쉬운 방법은 **Ollama** 또는 **LM Studio**입니다.)

### 1. [Ollama 설치 및 설정 가이드](./ollama_guide.md)
*   **추천 대상:** 개발 생산성을 높이고 싶고, CLI(터미널) 환경이 익숙하며, Docker 스타일로 가볍게 로컬 LLM을 띄우고 싶으신 분.
*   **특징:** 가장 단순한 명령어 한 줄로 모델 다운로드 및 API 서버 실행 가능.

### 2. [LM Studio 설치 및 설정 가이드](./lmstudio_guide.md)
*   **추천 대상:** 터미널 사용이 어색하고, 코드로 연동하기 전에 ChatGPT 같은 깔끔한 GUI 채팅 UI와 마우스 클릭만으로 편리하게 허깅페이스(Hugging Face) 모델을 다운로드하고 싶으신 분. **(※ 인텔 맥 사용자는 설치가 원활하지 않을 수 있으므로 Ollama 또는 llama.cpp를 권장합니다.)**
*   **특징:** 원클릭 로컬 추론 API 서버 활성화 및 미려한 챗 UI 제공.

### 3. [llama.cpp 빌드 및 실행 가이드](./llamacpp_guide.md)
*   **추천 대상:** 로컬 리소스를 극대화하여 성능(토큰 생성 속도)을 가장 높이고 싶거나, low-level 컴파일 옵션을 제어하고 싶으신 고급 개발자.
*   **특징:** C/C++ 기반 초경량 실행 엔진, Apple Silicon(Metal) 및 GPU 가속 직접 제어 가능.

---

## 추가 참고 자료
*   [Gemma 4 모델 상세 사양 안내](./gemma4_guide.md): Gemma 4의 특징(텍스트/이미지/오디오 멀티모달, 함수 호출 등)과 아키텍처에 대한 상세 정보입니다.
