# Gemma 4 핸즈온 - Flutter/DartPad 코드 생성 규칙

이 작업 공간에서 Flutter/DartPad용 실습 코드를 생성할 때는 반드시 다음 규칙을 준수해야 합니다:

1. **허용된 라이브러리 및 패키지 사용**:
   - Dart 코어 라이브러리: `dart:async`, `dart:math`, `dart:convert`, `dart:collection`, `dart:developer`, `dart:typed_data`, `dart:ui`
   - Flutter 패키지: `animations`, `flame`, `fl_chart`, `flutter_bloc`, `flutter_riverpod`, `provider`, `flutter_hooks`, `flutter_map`, `flutter_svg`, `go_router`, `google_fonts`, `google_generative_ai`, `url_launcher` 등 DartPad에서 허용된 패키지만 사용. 그 외 패키지는 수입하지 말 것.

2. **단일 파일 출력 (Single-File Output)**:
   - 모든 클래스, 헬퍼 메소드, 데이터 모델 및 `main()` 함수는 단일 코드 파일 내에 작성되어야 합니다. 상대 경로 임포트(`import 'utils.dart';` 등)는 금지됩니다.

3. **로컬 에셋 로드 금지 (No Local Assets)**:
   - 로컬 이미지, 오디오 또는 커스텀 로컬 폰트를 사용하지 마십시오.
   - 이미지는 `Image.network`를 사용하고 네트워크 에러 처리를 수반해야 합니다.
   - 아이콘은 standard Flutter `Icons`를 사용하거나 `CustomPainter`로 그리십시오.
   - 폰트는 `google_fonts` 패키지를 이용해 주입하십시오.

4. **자원 정리 (Resource Lifecycle Management)**:
   - 메모리 누수를 방지하기 위해 `Timer`, `AnimationController`, `StreamController` 등의 무거운 리소스는 반드시 `StatefulWidget`의 `dispose()` 메소드에서 정리(`dispose`)해 주어야 합니다.

5. **현대식 Dart 및 Null Safety**:
   - 엄격한 Null Safety와 타입 명시, 올바른 `const` 생성자 사용 등 모던 Dart 규칙을 준수하십시오.

6. **파일 저장 위치 제약사항 (Workspace Agents)**:
   - 작성된 코드는 반드시 이 워크스페이스 내의 `hands-on/flutter_app.dart` 파일 경로에 생성하거나 기존 내용을 완전히 덮어써서 업데이트해야 합니다. 다른 파일에 덮어쓰거나 루트에 생성하지 마십시오.
