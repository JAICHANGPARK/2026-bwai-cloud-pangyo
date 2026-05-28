# Ollama 설치 및 Gemma 4 모델 준비 가이드

[Ollama](https://ollama.com/)는 로컬 환경에서 대형 언어 모델(LLM)을 아주 쉽고 간편하게 실행할 수 있도록 돕는 오픈소스 도구입니다. 명령어 단 한 줄로 Gemma 4 모델을 다운로드하고 API 서버를 띄울 수 있어 개발자들에게 가장 권장되는 방식 중 하나입니다.

---

## OS별 Ollama 설치 방법

### 1. macOS (Apple Silicon & Intel Mac)
macOS 환경에서는 네이티브 애플리케이션 설치 또는 패키지 매니저(Homebrew)를 통해 설치할 수 있습니다.

#### 방법 A: 네이티브 앱 다운로드 (권장)
1. [Ollama macOS 다운로드 페이지](https://ollama.com/download/mac)에 접속합니다.
2. **Download for Mac** 버튼을 클릭하여 `Ollama-darwin.zip` 파일을 다운로드합니다.
3. 압축을 해제한 후 `Ollama.app`을 **응용 프로그램(Applications)** 폴더로 드래그하여 이동시킵니다.
4. `Ollama` 앱을 더블 클릭해 실행합니다. 상단 메뉴 바에 Ollama 아이콘(라마 모양)이 생기면 실행 완료입니다.

#### 방법 B: Homebrew 사용하기
터미널을 열고 아래 명령어를 입력합니다.
```bash
brew install ollama
```

> [!NOTE]
> *   **Apple Silicon Mac (M 시리즈):** 별도 설정 없이 Apple GPU(Unified Memory)와 Metal API 가속이 100% 자동 활성화되어 매우 빠른 속도로 동작합니다.
> *   **Intel Mac:** CPU 연산으로 동작하므로 Apple Silicon에 비해 답변 속도가 느릴 수 있습니다. 인텔 맥 사용자라면 가급적 가벼운 `gemma4:e2b` 모델을 사용하는 것을 권장합니다.

---

### 2. Windows
Windows 10/11 환경을 지원하며 외장 GPU(Nvidia, AMD) 가속을 자동으로 탐지하여 적용합니다.

1. [Ollama Windows 다운로드 페이지](https://ollama.com/download/windows)에 접속합니다.
2. **Download for Windows** 버튼을 클릭하여 `OllamaSetup.exe` 파일을 다운로드합니다.
3. 다운로드한 설치 파일을 실행하고 가이드에 따라 설치를 완료합니다.
4. 설치가 끝나면 윈도우 작업 표시줄 오른쪽 아래(시스템 트레이)에 Ollama 아이콘이 나타나며 백그라운드 서비스가 시작됩니다.

> [!TIP]
> Windows 환경에 NVIDIA 외장 그래픽 카드가 탑재되어 있다면 Ollama가 자동으로 CUDA 드라이버를 감지하여 GPU 하드웨어 가속을 수행하므로 매우 쾌적한 속도를 보장합니다.

---

## Gemma 4 모델 다운로드 및 실행

Ollama 설치를 마쳤다면 터미널(macOS는 Terminal 또는 Warp, Windows는 Powershell 또는 CMD)을 열고 본인의 노트북 사양에 맞는 명령어를 입력해 주세요.

### 1. 내 컴퓨터 사양에 맞는 모델 받기

*   **메모리 8GB 이하 노트북 (Intel Mac, 보급형 Windows 등):**
    ```bash
    ollama run gemma4:e2b
    ```
*   **메모리 16GB 이상 노트북 (Apple Silicon Mac, GPU 탑재 Windows 등 - 권장):**
    ```bash
    ollama run gemma4:e4b
    ```

명령어를 실행하면 자동으로 모델 파일 다운로드가 시작되고, 다운로드가 끝나면 터미널 프롬프트(`>>>`)가 열려 대화가 가능해집니다.

---

## 정상 설치 여부 확인 및 테스트

### 1. 설치된 모델 목록 확인
터미널에 다음 명령어를 입력하여 Gemma 4 모델이 정상적으로 로컬 디스크에 다운로드되었는지 확인합니다.
```bash
ollama list
```
**출력 예시:**
```text
NAME          ID            SIZE      MODIFIED
gemma4:e4b    xxxxxxxxx     2.8 GB    Just now
```

### 2. 로컬 채팅 테스트
모델을 실행하고 프롬프트에 한국어로 질문을 입력해 정상 작동 여부를 테스트합니다.
```bash
ollama run gemma4:e4b
```
```text
>>> 안녕하세요! 자기소개 한번 해주세요.
안녕하세요! 저는 구글이 개발한 오픈 가중치 인공지능 모델인 Gemma 4 (E4B)입니다...
>>> /bye
```
*   채팅 창을 종료하려면 `/bye`를 입력하거나 `Ctrl + D`를 누릅니다.

### 3. 로컬 API 서버 정상 작동 확인
Ollama는 설치와 동시에 백그라운드에서 로컬 API 서버(`http://localhost:11434`)를 자동으로 열어줍니다. 터미널에서 다음 curl 명령을 실행해 정상 응답이 오는지 확인합니다.

*   **macOS / Linux:**
    ```bash
    curl http://localhost:11434/api/tags
    ```
*   **Windows (PowerShell):**
    ```powershell
    Invoke-RestMethod -Uri http://localhost:11434/api/tags
    ```

**정상 응답 예시:**
```json
{
  "models": [
    {
      "name": "gemma4:e4b",
      "model": "gemma4:e4b",
      "modified_at": "2026-05-28T19:50:00.000000+09:00",
      "size": 2800000000,
      "digest": "..."
    }
  ]
}
```

이제 Ollama와 Gemma 4 모델 준비가 완료되었습니다!
[목차로 돌아가기](./README.md)
