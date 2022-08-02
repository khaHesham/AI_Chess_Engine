import 'package:flutter/material.dart';
import 'package:flutter_chess_board/flutter_chess_board.dart';
import 'utils.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const MyHomePage(),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({Key? key}) : super(key: key);

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  ChessBoardController controller = ChessBoardController();
  String _fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1';
  List<BoardArrow> arrows = [];

  void possible_moves() {
    controller.getPossibleMoves();
  }

  @override
  void initState() {
    super.initState();
    controller.addListener(() {});
  }

  String possiblemovies = "";
  String src = "b2";
  String dest = "c4";

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        centerTitle: true,
        title: const Text("Chess Game"),
      ),
      body: Column(
        children: [
          SizedBox(height: 120,),
          Center(
            child: ChessBoard(
              onMove: () => {
                print(controller.getFen()),
                print(controller.getBoard()),
                print(controller.game.san_moves().toString()),
              },
              controller: controller,
              boardColor: BoardColor.darkBrown,
              boardOrientation: PlayerColor.white,
              arrows: [
                BoardArrow(
                    from: src, to: dest, color: Colors.red.withOpacity(0.5)),
                BoardArrow(
                    from: "b4", to: "b5", color: Colors.red.withOpacity(0.5))
              ],
            ),
          ),
          Expanded(
            child: ValueListenableBuilder<Chess>(
              valueListenable: controller,
              builder: (context, game, _) {
                return Text(
                  controller.getSan().fold(
                        '',
                        (previousValue, element) =>
                            previousValue + '\n' + (element ?? ''),
                      ),
                );
              },
            ),
          )
        ],
      ),
    );
  }
}
