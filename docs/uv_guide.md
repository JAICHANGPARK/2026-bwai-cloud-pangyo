# uv 설치 및 개발 환경 구성 가이드

[uv](https://github.com/astral-sh/uv)는 Rust로 작성된 초고속 파이썬 패키지 인스톨러이자 프로젝트 매니저입니다. 기존 `pip`나 `pip-tools` 대비 10~100배 빠른 속도로 패키지를 설치하고 가상환경을 관리해 줍니다. 이번 Gemma 4 실습 코드 구동을 위해 uv를 사용해 가볍고 빠르게 환경을 구성해 보겠습니다.

---

## OS별 uv 설치 방법

### 1. macOS (Apple Silicon & Intel Mac)
터미널을 열고 아래 명령어 중 하나를 실행합니다.

#### 방법 A: 공식 스크립트 실행 (권장)
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
*   설치가 끝나면 터미널을 재시작하거나 `source ~/.zshrc`를 실행해 변경 사항을 반영합니다.

#### 방법 B: Homebrew 사용하기
```bash
brew install uv
```

---

### 2. Windows
PowerShell을 열고 아래 명령어 중 하나를 실행합니다.

#### 방법 A: 공식 스크립트 실행 (권장)
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

#### 방법 B: winget 사용하기
```powershell
winget install --id=astral-sh.uv -e
```

---

### 3. 공통: pip 설치 (위의 방법들이 실패할 경우)
이미 파이썬이 설치되어 있고 환경변수 설정이 복잡할 경우, 기존 pip를 이용해 설치할 수도 있습니다.
```bash
pip install uv
```

설치가 완료되었는지 확인하려면 터미널에 아래 명령어를 입력해 버전을 출력해 봅니다:
```bash
uv --version
```

---

## uv를 이용한 가상환경 구축 및 패키지 설치

실습을 진행하기 위해 **`hands-on` 폴더로 이동**한 뒤 가상환경을 구성하고 필요한 라이브러리를 동기화합니다.

### 1. hands-on 폴더로 이동 및 가상환경 생성
터미널에서 `hands-on` 폴더로 이동한 후 가상환경(`.venv`)을 생성합니다:
```bash
cd hands-on
uv venv
```
*   uv는 순식간에 가상환경을 생성합니다.

### 2. 가상환경 활성화

*   **macOS / Linux:**
    ```bash
    source .venv/bin/activate
    ```
*   **Windows (PowerShell):**
    ```powershell
    .venv\Scripts\Activate.ps1
    ```
*   **Windows (CMD):**
    ```cmd
    .venv\Scripts\activate.bat
    ```

활성화되면 터미널 창 맨 앞에 `(.venv)` 표시가 나타납니다.

### 3. 실습 필수 라이브러리 설치 및 동기화
`hands-on` 폴더 내에 이미 제공된 `pyproject.toml`과 `uv.lock` 설정을 가상환경에 동기화합니다:
```bash
uv sync
```
*   (참고) 만약 직접 개별 라이브러리를 추가하고 싶다면 `uv add httpx openai python-dotenv` 명령어를 실행할 수도 있습니다. `uv sync`를 실행하면 실습에 필요한 모든 패키지가 초고속으로 자동 설치됩니다.

이제 파이썬 실습을 위한 모든 개발 환경 준비가 끝났습니다!
[목차로 돌아가기](./README.md)
