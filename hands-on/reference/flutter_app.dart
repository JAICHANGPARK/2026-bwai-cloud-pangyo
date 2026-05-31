import 'package:flutter/material.dart';
import 'package:flutter/scheduler.dart';

void main() {
  runApp(const BreakoutGameApp());
}

class BreakoutGameApp extends StatelessWidget {
  const BreakoutGameApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: '벽돌깨기 게임',
      theme: ThemeData(
        brightness: Brightness.light,
        primarySwatch: Colors.deepPurple,
        useMaterial3: true,
      ),
      home: const GameScreen(),
    );
  }
}

class Brick {
  final Rect rect;
  bool isDestroyed;
  Brick({required this.rect, required this.isDestroyed});
}

class GameScreen extends StatefulWidget {
  const GameScreen({super.key});

  @override
  State<GameScreen> createState() => _GameScreenState();
}

class _GameScreenState extends State<GameScreen> with SingleTickerProviderStateMixin {
  late Ticker _ticker;
  Duration _lastElapsed = Duration.zero;

  static const double boardWidth = 400.0;
  static const double boardHeight = 600.0;
  static const int rows = 5;
  static const int cols = 8;
  static const double paddleWidth = 80.0;
  static const double paddleHeight = 15.0;
  static const double ballRadius = 8.0;

  List<Brick> _bricks = [];
  Offset ballPosition = const Offset(boardWidth / 2, boardHeight - 100);
  Offset ballVelocity = const Offset(200.0, -300.0);
  Offset paddlePosition = const Offset(boardWidth / 2 - 40, boardHeight - 50);

  int score = 0;
  bool isGameOver = false;
  bool isGameWon = false;

  @override
  void initState() {
    super.initState();
    _initializeBricks();
    _ticker = Ticker(_updateGame);
    _ticker.start();
  }

  void _initializeBricks() {
    _bricks.clear();
    final brickWidth = (boardWidth - 20) / cols;
    const brickHeight = 20.0;
    const double startYOffset = 50.0;

    for (int r = 0; r < rows; r++) {
      for (int c = 0; c < cols; c++) {
        _bricks.add(Brick(
          rect: Rect.fromLTWH(c * (brickWidth + 1) + 10, startYOffset + r * 30, brickWidth - 1, brickHeight),
          isDestroyed: false,
        ));
      }
    }
  }

  void _updateGame(Duration elapsed) {
    if (isGameOver || isGameWon) return;

    final double dt = (elapsed - _lastElapsed).inMicroseconds / 1000000.0;
    _lastElapsed = elapsed;

    if (dt > 0.1) return; // Prevent teleportation on lag

    setState(() {
      ballPosition += ballVelocity * dt;

      // Wall collisions
      if (ballPosition.dx <= ballRadius || ballPosition.dx >= boardWidth - ballRadius) {
        ballVelocity = Offset(-ballVelocity.dx, ballVelocity.dy);
      }
      if (ballPosition.dy <= ballRadius) {
        ballVelocity = Offset(ballVelocity.dx, -ballVelocity.dy);
      }

      // Paddle collision
      final paddleRect = Rect.fromLTWH(paddlePosition.dx, paddlePosition.dy, paddleWidth, paddleHeight);
      if (paddleRect.contains(ballPosition)) {
        ballVelocity = Offset(ballVelocity.dx, -ballVelocity.dy.abs() * 1.05);
      }

      // Brick collision
      bool allDestroyed = true;
      for (var brick in _bricks) {
        if (!brick.isDestroyed) {
          allDestroyed = false;
          if (brick.rect.contains(ballPosition)) {
            brick.isDestroyed = true;
            ballVelocity = Offset(ballVelocity.dx, -ballVelocity.dy);
            score += 10;
          }
        }
      }

      if (allDestroyed) isGameWon = true;
      if (ballPosition.dy > boardHeight) isGameOver = true;
    });
  }

  @override
  void dispose() {
    _ticker.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('벽돌깨기 게임'),
        centerTitle: true,
        backgroundColor: Theme.of(context).colorScheme.primaryContainer,
      ),
      body: GestureDetector(
        onPanUpdate: (d) => setState(() {
          paddlePosition = Offset((paddlePosition.dx + d.delta.dx).clamp(0, boardWidth - paddleWidth), paddlePosition.dy);
        }),
        child: Center(
          child: SingleChildScrollView(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const SizedBox(height: 10),
                Text('Score: $score', style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
                const SizedBox(height: 10),
                Container(
                  width: boardWidth,
                  height: boardHeight,
                  decoration: BoxDecoration(
                    color: Colors.grey[100],
                    border: Border.all(color: Colors.grey),
                  ),
                  child: CustomPaint(
                    painter: GamePainter(_bricks, ballPosition, paddlePosition),
                  ),
                ),
                const SizedBox(height: 20),
                if (isGameOver || isGameWon)
                  Column(
                    children: [
                      Text(
                        isGameWon ? 'You Win! 🎉' : 'Game Over 😢',
                        style: TextStyle(
                          fontSize: 28,
                          fontWeight: FontWeight.bold,
                          color: isGameWon ? Colors.green : Colors.red,
                        ),
                      ),
                      const SizedBox(height: 10),
                      ElevatedButton.icon(
                        icon: const Icon(Icons.refresh),
                        onPressed: () {
                          setState(() {
                            _initializeBricks();
                            ballPosition = const Offset(boardWidth / 2, boardHeight - 100);
                            ballVelocity = const Offset(200.0, -300.0);
                            score = 0;
                            isGameOver = false;
                            isGameWon = false;
                          });
                        },
                        label: const Text('다시 시작'),
                      ),
                    ],
                  )
              ],
            ),
          ),
        ),
      ),
    );
  }
}

class GamePainter extends CustomPainter {
  final List<Brick> bricks;
  final Offset ball;
  final Offset paddle;
  GamePainter(this.bricks, this.ball, this.paddle);

  @override
  void paint(Canvas canvas, Size size) {
    for (var b in bricks) {
      if (!b.isDestroyed) {
        canvas.drawRect(
          b.rect,
          Paint()
            ..shader = const LinearGradient(
              colors: [Colors.orange, Colors.red],
            ).createShader(b.rect)
            ..style = PaintingStyle.fill,
        );
        canvas.drawRect(
          b.rect,
          Paint()
            ..color = Colors.white
            ..style = PaintingStyle.stroke
            ..strokeWidth = 1,
        );
      }
    }
    
    // Draw paddle
    final paddleRect = Rect.fromLTWH(paddle.dx, paddle.dy, 80, 15);
    canvas.drawRRect(
      RRect.fromRectAndRadius(paddleRect, const Radius.circular(8)),
      Paint()..color = Colors.blue,
    );
    
    // Draw ball
    canvas.drawCircle(ball, 8, Paint()..color = Colors.black);
  }

  @override
  bool shouldRepaint(covariant CustomPainter oldDelegate) => true;
}
