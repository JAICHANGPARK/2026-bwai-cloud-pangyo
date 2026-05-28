# llama.cpp 빌드 및 Gemma 4 실행 가이드

[llama.cpp](https://github.com/ggerganov/llama.cpp)는 C/C++로 구현된 초경량 LLM 추론 엔진입니다. 종속성이 거의 없고 리소스 오버헤드가 극도로 적어 로컬 하드웨어(CPU 및 GPU)의 성능을 한계까지 끌어올릴 수 있습니다. 실행 속도를 최대로 높이고 싶거나 컴파일 환경 제어가 익숙한 개발자에게 추천하는 방식입니다.

---

## llama.cpp 다운로드 및 빌드 방법

### 1. macOS (Apple Silicon & Intel Mac)
macOS에서는 Xcode 명령줄 도구를 활용해 소스코드를 클론하고 직접 빌드하는 것이 가장 확실하고 권장되는 방법입니다.

#### 사전 준비
터미널을 열고 컴파일러(`clang` / `make` 등)가 설치되어 있는지 확인합니다. 설치되어 있지 않다면 설치 팝업을 수락하여 설치합니다:
```bash
xcode-select --install
```

#### 소스코드 다운로드 및 컴파일
1. 저장소를 클론하고 폴더로 진입합니다:
   ```bash
   git clone https://github.com/ggerganov/llama.cpp
   cd llama.cpp
   ```
2. CMake를 사용해 빌드 디렉토리를 만들고 컴파일을 수행합니다:
   ```bash
   cmake -B build -DCMAKE_BUILD_TYPE=Release
   cmake --build build --config Release
   ```

> [!NOTE]
> *   **Apple Silicon (M 시리즈):** CMake 빌드 과정에서 macOS의 **Metal (MPS)** 하드웨어 가속 성능이 자동으로 탑재되도록 빌드됩니다.
> *   **Intel Mac:** CPU 코어 연산 및 벡터 연산 명령어(AVX2 등)를 컴파일러가 자동 탐지하여 최적화 빌드합니다.

---

### 2. Windows
Windows 환경의 경우, 컴파일 없이 사전에 빌드된 바이너리 패키지(Pre-built binaries)를 다운로드해 바로 실행하는 방식을 권장합니다.

#### 사전 빌드 파일 다운로드
1. [llama.cpp GitHub Releases 페이지](https://github.com/ggerganov/llama.cpp/releases)에 접속합니다.
2. 최신 릴리스 버전 하단의 **Assets** 목록에서 본인의 그래픽 카드 사양에 맞는 `.zip` 파일을 다운로드합니다:
   *   **NVIDIA 그래픽 카드 소유자 (권장):** `llama-bXXXX-bin-win-cuda-cuXX.X-x64.zip` (CUDA 가속 지원)
   *   **AMD 그래픽 카드 소유자:** `llama-bXXXX-bin-win-vulkan-x64.zip` (Vulkan 가속 지원)
   *   **외장 그래픽 카드가 없는 경우 (CPU 전용):** `llama-bXXXX-bin-win-llvm-x64.zip`
3. 다운로드한 `.zip` 파일의 압축을 로컬 폴더(예: `C:\llamacpp`)에 해제합니다.

---

## Gemma 4 GGUF 모델 다운로드

llama.cpp는 단일 파일로 구성된 **GGUF** 포맷의 모델 파일을 사용합니다. 터미널(또는 PowerShell)에서 `curl` 명령어를 이용해 허깅페이스 저장소에서 모델을 직접 다운로드할 수 있습니다.

먼저 모델을 저장할 디렉토리를 생성하고 다운로드를 진행합니다:

### macOS / Linux (터미널)
```bash
mkdir -p models

# Gemma 4 E4B (16GB RAM 이상 권장 - Q4_K_M 양자화 버전)
curl -L -o models/gemma-4-e4b-it-Q4_K_M.gguf https://huggingface.co/bartowski/gemma-4-E4B-it-GGUF/resolve/main/gemma-4-E4B-it-Q4_K_M.gguf

# Gemma 4 E2B (8GB RAM 노트북 권장 - Q4_K_M 양자화 버전)
# curl -L -o models/gemma-4-e2b-it-Q4_K_M.gguf https://huggingface.co/bartowski/gemma-4-E2B-it-GGUF/resolve/main/gemma-4-E2B-it-Q4_K_M.gguf
```

### Windows (PowerShell)
```powershell
New-Item -ItemType Directory -Force -Path .\models

# Gemma 4 E4B (16GB RAM 이상 권장)
Invoke-WebRequest -Uri "https://huggingface.co/bartowski/gemma-4-E4B-it-GGUF/resolve/main/gemma-4-E4B-it-Q4_K_M.gguf" -OutFile ".\models\gemma-4-e4b-it-Q4_K_M.gguf"

# Gemma 4 E2B (8GB RAM 권장)
# Invoke-WebRequest -Uri "https://huggingface.co/bartowski/gemma-4-E2B-it-GGUF/resolve/main/gemma-4-E2B-it-Q4_K_M.gguf" -OutFile ".\models\gemma-4-e2b-it-Q4_K_M.gguf"
```

---

## Gemma 4 로컬 실행 방법

최신 llama.cpp는 대화형 인터페이스를 제공하는 `llama-cli`와 로컬 웹 데모/API 서버를 구동하는 `llama-server` 바이너리를 포함하고 있습니다. (과거 버전의 `main`, `server` 명령어가 통합 및 변경되었습니다.)

### 1. 터미널 인터랙티브 대화 (CLI)

*   **macOS (컴파일 완료 후 `llama.cpp` 폴더 안에서 실행):**
    ```bash
    ./build/bin/llama-cli -m models/gemma-4-e4b-it-Q4_K_M.gguf -cnv -p "너는 친절한 AI 어시스턴트야. 사용자의 질문에 답해줘."
    ```
*   **Windows (압축 해제한 폴더 안에서 실행):**
    ```cmd
    llama-cli.exe -m models\gemma-4-e4b-it-Q4_K_M.gguf -cnv -p "너는 친절한 AI 어시스턴트야. 사용자의 질문에 답해줘."
    ```
    *   `-cnv` 옵션은 챗봇 형태의 대화형 세션(Conversation Mode)을 켭니다. 대화 모드에서 탈출하려면 `Ctrl + C`를 누르세요.

---

### 2. 로컬 웹 서버 및 API 서버 구동 (Web UI)

Gemma 4 모델을 서버 모드로 로드하여 브라우저 환경에서 대화하거나 타 서비스와 연동합니다.

*   **macOS:**
    ```bash
    ./build/bin/llama-server -m models/gemma-4-e4b-it-Q4_K_M.gguf -c 4096 --port 8080
    ```
*   **Windows:**
    ```cmd
    llama-server.exe -m models\gemma-4-e4b-it-Q4_K_M.gguf -c 4096 --port 8080
    ```

**실행 확인:**
1. 브라우저를 열고 `http://localhost:8080`에 접속합니다.
2. llama.cpp가 자체 제공하는 완성도 높은 웹 인터페이스를 통해 시스템 프롬프트 제어, 매개변수 조절, 채팅 테스트가 가능합니다.
3. 이 서버는 OpenAI 규격 API 호환 엔드포인트(`http://localhost:8080/v1`)도 자동으로 오픈합니다.

이제 llama.cpp를 활용한 로컬 고성능 Gemma 4 실습 준비가 모두 완료되었습니다!
[목차로 돌아가기](./README.md)
