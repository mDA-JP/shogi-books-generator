from dataclasses import dataclass
from copy import deepcopy


PROMOTION = 8
EMP = -1
FU = 0
KY = 1
KE = 2
GI = 3
KI = 4
KA = 5
HI = 6
OU = 7
TO = FU + PROMOTION
NY = KY + PROMOTION
NK = KE + PROMOTION
NG = GI + PROMOTION
UM = KA + PROMOTION
RY = HI + PROMOTION

BLACK = 20
WHITE = 40

PIECE_KANJI_MAP = {
    EMP: '・',
    FU : '歩',
    KY : '香',
    KE : '桂',
    GI : '銀',
    KI : '金',
    KA : '角',
    HI : '飛',
    OU : '玉',
    TO : 'と',
    NY : '杏',
    NK : '圭',
    NG : '全',
    UM : '馬',
    RY : '竜',
}

KANJI_PIECE_MAP = {value: key for key, value in PIECE_KANJI_MAP.items()}

KANSUJI_INT_MAP = {
    '一': 1,
    '二': 2,
    '三': 3,
    '四': 4,
    '五': 5,
    '六': 6,
    '七': 7,
    '八': 8,
    '九': 9,
}


@dataclass
class Piece:
    type_: int
    camp: int
    is_promoted: bool = False
    
    def to_int(self):
        return self.type_ + (BLACK if self.camp == 0 else WHITE) + (PROMOTION if self.is_promoted else 0)

    def promotion(self):
        self.is_promoted = True
        self.type_ = self.type_ + PROMOTION

    @property
    def raw_type(self):
        return self.type_ - (PROMOTION if self.is_promoted else 0)

    def to_str(self):
        return ('v' if self.camp == 1 else ' ') + PIECE_KANJI_MAP[self.type_]


INITIAL_BOARD = [
    Piece(KY, 1), Piece(KE, 1), Piece(GI, 1), Piece(KI, 1), Piece(OU, 1), Piece(KI, 1), Piece(GI, 1), Piece(KE, 1), Piece(KY, 1),
    Piece(EMP, -1), Piece(HI, 1), Piece(EMP, -1), Piece(EMP, -1), Piece(EMP, -1), Piece(EMP, -1), Piece(EMP, -1), Piece(KA, 1), Piece(EMP, -1),
    Piece(FU, 1), Piece(FU, 1), Piece(FU, 1), Piece(FU, 1), Piece(FU, 1), Piece(FU, 1), Piece(FU, 1), Piece(FU, 1), Piece(FU, 1),
    Piece(EMP, -1), Piece(EMP, -1), Piece(EMP, -1), Piece(EMP, -1), Piece(EMP, -1), Piece(EMP, -1), Piece(EMP, -1), Piece(EMP, -1), Piece(EMP, -1),
    Piece(EMP, -1), Piece(EMP, -1), Piece(EMP, -1), Piece(EMP, -1), Piece(EMP, -1), Piece(EMP, -1), Piece(EMP, -1), Piece(EMP, -1), Piece(EMP, -1),
    Piece(EMP, -1), Piece(EMP, -1), Piece(EMP, -1), Piece(EMP, -1), Piece(EMP, -1), Piece(EMP, -1), Piece(EMP, -1), Piece(EMP, -1), Piece(EMP, -1),
    Piece(FU, 0), Piece(FU, 0), Piece(FU, 0), Piece(FU, 0), Piece(FU, 0), Piece(FU, 0), Piece(FU, 0), Piece(FU, 0), Piece(FU, 0),
    Piece(EMP, -1), Piece(KA, 0), Piece(EMP, -1), Piece(EMP, -1), Piece(EMP, -1), Piece(EMP, -1), Piece(EMP, -1), Piece(HI, 0), Piece(EMP, -1),
    Piece(KY, 0), Piece(KE, 0), Piece(GI, 0), Piece(KI, 0), Piece(OU, 0), Piece(KI, 0), Piece(GI, 0), Piece(KE, 0), Piece(KY, 0),
]


@dataclass
class Square:
    x: int
    y: int

    def __str__(self):
        return f'{self.x}{self.y}'

    def __repr__(self):
        return f'{self.x}{self.y}'

    def to_int(self):
        return 9 - self.x + (self.y - 1) * 9

    def is_hand(self):
        return self.x == 0 and self.y == 0


class Board:
    def __init__(self, board=None):
        if board is None:
            self.board = board if board else INITIAL_BOARD
            self.b_hand = [0] * 7
            self.w_hand = [0] * 7

    def move(self, move):
        if move.from_.is_hand():
            self.board[move.to.to_int()] = move.piece
            hand = self.b_hand if move.phase else self.w_hand
            hand[move.piece.raw_type] -= 1
        else:
            self.board[move.from_.to_int()] = Piece(EMP, -1)
            if self.board[move.to.to_int()].type_ != EMP:
                hand = self.b_hand if move.phase else self.w_hand
                hand[self.board[move.to.to_int()].raw_type] += 1
            self.board[move.to.to_int()] = move.piece
            if move.promotion:
                self.board[move.to.to_int()].promotion()

    def _to_str_hand(self, b=True):
        hand = self.b_hand  if b else self.w_hand
        s = ''
        for i in reversed(range(7)):
            v = hand[i]
            if v >= 1:
                s += PIECE_KANJI_MAP[i]
            if v > 1:
                s += str(v)

        return s

    def _to_str_board(self):
        s = ''
        for i in range(9):
            for j in range(9):
                s += self.board[9 * i + j].to_str()
            if i < 8:
                s += '\n'
        return s

    def print(self):
        print('持ち駒:' + self._to_str_hand(False))
        print(self._to_str_board())
        print('持ち駒:' + self._to_str_hand())


@dataclass
class Move:
    phase: bool
    piece: Piece
    from_: Square
    to: Square
    promotion: bool
    comment: str = ''


class KifParser:
    @classmethod
    def parse(cls, f):
        flag = False
        init_flag = False
        zenkaku_flag = False
        board = Board() 
        moves = []
        for l in f:
            if '後手の持駒' in l:
                init_flag = True
                zenkaku_flag = '　' in l
                l.split('：')
            elif '先手の持駒':
                pass

            ll = l.split()
            if ll[0] == '1':
                flag = True

            if flag and ll[0].isdigit():
                move_str = ll[1]
                if move_str == '投了':
                    break
                x = int(move_str[0])
                y = KANSUJI_INT_MAP[move_str[1]]
                phase = int(ll[0]) % 2 == 1
                piece_type = KANJI_PIECE_MAP[move_str[2]]
                move = Move(
                    phase,
                    Piece(piece_type, 0 if phase else 1, piece_type >= TO),
                    Square(0, 0),
                    Square(x, y),
                    '成' in move_str
                )
                if '打' not in move_str:
                    move.from_ = Square(int(move_str[-3]), int(move_str[-2]))
                moves.append(move)
            elif l[0] == '*':
                moves[-1].comment += l[1:]
        return board, moves


class Kif:
    def __init__(self, path):
        self.path = path
        if '.kif' in path:
            parser = KifParser
        self.start_board, self.moves = parser.parse(open(self.path, 'r'))

    def index(self, index=None):
        board = deepcopy(self.start_board)
        if index == None:
            index = len(self.moves)
        for i in range(index):
            board.move(self.moves[i])
        return board


if __name__ == '__main__':
    kif = Kif('test.kif')
    board = kif.index()
    board.print()
