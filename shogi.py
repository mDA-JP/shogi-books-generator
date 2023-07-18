import os

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
    '十': 10,
    '十一': 11,
    '十二': 12,
    '十三': 13,
    '十四': 14,
    '十五': 15,
    '十六': 16,
    '十七': 17,
    '十八': 18,
    '十九': 19,
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

EMPTY_BOARD = [Piece(EMP, -1) for i in range(81)]
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
    def __init__(self, board=INITIAL_BOARD, b_hand=[0] * 7, w_hand=[0] * 7):
        self.board = board
        self.b_hand = b_hand
        self.w_hand = w_hand

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
    phase: bool = None
    piece: Piece = None
    from_: Square = None
    to: Square = None
    promotion: bool = None
    comment: str = ''


class Node:
    def __init__(self, move: Move=Move(), parent=None):
        self.move = move
        self.parent = parent
        self.children = []

    def append_child(self, child):
        self.children.append(child)


class KifTree:
    def __init__(self, init_board: Board, root: Node):
        self.init_board = init_board
        self.root = root

    def create_specified_board(self, branch=0, index=None):
        node = self.root
        board = deepcopy(self.init_board)
        i = 0
        current_branch = 0
        while True:
            if index is not None and index <= i:
                break
            if len(node.children) == 0:
                break
            elif len(node.children) == 1 or branch <= current_branch:
                node = node.children[0]
            elif len(node.children) == 2 and branch > current_branch:
                node = node.children[1]
                current_branch += 1
            board.move(node.move)
            i += 1
        return board

    def extract_subtree(self, branch=0):
        pass


class KifParser:
    @classmethod
    def parse(cls, f):
        flag = False
        board = Board() 
        root = Node()
        current_node = root
        for l in f:
            l = l.strip()
            ll = l.split()
            if '後手の持駒' in l:
                board = cls._generate_init_board(f, l)
            elif l == '手数----指手---------消費時間--':
                root = cls._generate_move_tree(f)
        return KifTree(board, root)

    @classmethod
    def _generate_init_board(cls, f, s):
        b_hand = [0] * 7
        w_hand = [0] * 7
        board = EMPTY_BOARD

        def _hand(s):
            space = ' ' if ' ' in s else '　'
            hand = b_hand if '先手' in s else w_hand
            for p in s.split('：')[1].split(space):
                piece = KANJI_PIECE_MAP[p[0]]
                num = KANSUJI_INT_MAP[p[1:]]
                hand[piece] = num

        _hand(s)

        for l in f:
            l = l.strip()
            if len(l) == 0:
                continue
            if '持駒' in l:
                _hand(l)
            elif l[-1] in KANSUJI_INT_MAP.keys():
                y = KANSUJI_INT_MAP[l[-1]]
                index = 1
                x = 9
                while x > 0:
                    if l[index+1] != '・':
                        piece = Piece(
                            KANJI_PIECE_MAP[l[index+1]],
                            1 if l[index] == 'v' else 0
                        )
                        board[Square(x, y).to_int()] = piece
                    index += 2
                    x -= 1
            if '先手の持駒' in l:
                break

        return Board(board, b_hand, w_hand)

    @classmethod
    def _generate_move_tree(clss, f):
        root = Node()
        current_node = root
        for l in f:
            l = l.strip()
            if len(l) == 0:
                continue
            ll = l.split()
            if ll[0].isdigit():
                move_str = ll[1]
                if move_str[:2] in ('投了', '中断'):
                    continue
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
                node = Node(
                    move,
                    current_node
                )
                current_node.append_child(node)
                current_node = node
            elif l[0] == '*':
                current_node.move.comment += l[1:]
            elif '変化' in l:
                n = int(l.split('：')[1][:-1])
                current_node = root
                for i in range(n-1):
                    current_node = current_node.children[0]
        return root


class Kif:
    def __init__(self, path):
        self.path = path
        if '.kif' in path or '.kifu' in path:
            parser = KifParser
        self.tree = parser.parse(open(self.path, 'r'))

    def create_specified_board(self, branch=0, index=None):
        self.tree.create_specified_board(branch, index)


if __name__ == '__main__':
    kif = Kif('test.kifu')
    board = kif.tree.create_specified_board(branch=1, index=None)
    board.print()
