# Generate Flutter Dashboard Code

Write or update the Flutter single-file Dart script at `hands-on/flutter_app.dart`.

## Guidelines & Requirements:
1. **Workspace Rules:** Strictly follow the rules defined in [gemma4_flutter.md](file:///Users/jaichang/Documents/GitHub/2026-bwai-cloud-pangyo/.agents/rules/gemma4_flutter.md).
2. **Library Restrictions:** Only import allowed DartPad-supported libraries (`dart:async`, `dart:math`, `dart:convert`, etc.) and packages (`flutter_riverpod`, `provider`, `fl_chart`, `google_fonts`, `animations`, etc.).
3. **Single File Structure:** Combine all widgets, models, states, and the `main()` function in a single file. Do not use relative imports.
4. **No Local Assets:** Use `Image.network` for images with fallback widgets, and load fonts via the `google_fonts` package.
5. **Resource Lifecycle:** Correctly call `dispose()` to clean up resources like controllers or timers in `StatefulWidget` states.
6. **Null Safety:** Strictly adhere to modern Dart syntax and Null Safety.
7. **Target File:** Save the generated code strictly to `hands-on/flutter_app.dart`.
