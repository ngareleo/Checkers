import pygame as py
import pygame.event

game_running = True
S_HEIGHT, S_WIDTH = 600, 700
BOARD_DIM = 8
POSITION_DIM = 60
game_pieces = []
SCREEN_SIZE = [S_HEIGHT, S_WIDTH]
game_board = py.display.set_mode(SCREEN_SIZE)
py.init()

# ///////////////////////////////////////////////////////////////////////////////////////////////

colors = {
    "white": [225, 220, 200],
    "black": [119, 98, 92],
    "red": [73, 57, 44],
    "color_a": [0, 10, 10]
}
images = [
    py.image.load(r"./views/bp.png"),
    py.image.load(r"./views/rp.png"),
    py.image.load(r"./views/bpk.png"),
    py.image.load(r"./views/rpk.png"),
]


def get_relative_position(x, y):
    return [x + 20, y + 20]

# ///////////////////////////////////////////////////////////////////////////////////////////////


class Board:
    def __init__(self):
        self._background = "color_a"
        self.height = BOARD_DIM * POSITION_DIM
        self.width = BOARD_DIM * POSITION_DIM
        self.space_x = 10
        self.space_y = 10
        self.pieces = [Piece(piece_type=(i % 2)) for i in range(16)]
        self.positions = []
        self.init_board()

    def init_board(self):

        # add the positions
        count = 0
        pos_colors = ["white", "black"]
        for i in range(BOARD_DIM):
            self.positions.append([])
            for j in range(BOARD_DIM):
                temp = Position(POSITION_DIM, j * POSITION_DIM, i * POSITION_DIM, pos_colors[count % 2])
                self.positions[i].append(temp)
            count += 1

    def get_background(self):
        return self._background

    def place_board(self):
        offset_x = (S_WIDTH - self.width) / 2
        offset_y = (S_HEIGHT - self.height) / 2
        return [offset_y, offset_x]

    def set_background(self, color: str):
        if color.lower() in colors.keys():
            self._background = color
            return
        return -1

    def get_rect(self, screen=game_board):
        relative_position = self.place_board()
        py.draw.rect(screen,
                     colors[self._background],
                     [relative_position[0], relative_position[1], self.width, self.height])

    def render_board(self):
        for pos in self.positions:
            pos.get_rect()


class Piece:
    def __init__(self, piece_type):
        self.type = piece_type
        self._appearance = images[self.type]
        """
        0 - blue
        1 - red
        2 - blue king
        3 - red king
        """


class Position:

    def __init__(self, h, pos_x, pos_y, color, piece=None):
        self.height = h
        self.color = color
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.has_piece = False
        self.piece = piece

    @staticmethod
    def get_offset():
        offset_x = (S_WIDTH - (BOARD_DIM * POSITION_DIM)) / 2
        offset_y = (S_HEIGHT - (BOARD_DIM * POSITION_DIM)) / 2
        return [offset_y, offset_x]

    def get_rect(self, screen=game_board):
        off_ = self.get_offset()
        relative_position = [self.pos_x + off_[0], self.pos_y + off_[1]]
        py.draw.rect(screen,
                     colors[self.color],
                     [relative_position[0], relative_position[1], self.height, self.height])

    def assign_piece(self, piece: Piece):
        self.has_piece = True
        self.piece = piece
        game_board.blit(self.piece, [self.pos_x, self.pos_y])


# ///////////////////////////////////////////////////////////////////////////////////////////////


main_board = Board()


# ///////////////////////////////////////////////////////////////////////////////////////////////


def pre_checks():
    if S_WIDTH < BOARD_DIM * POSITION_DIM:
        print("Screen Size too small")
        exit(-1)


pre_checks()
while game_running:

    game_board.fill(colors["red"])
    main_board.get_rect()

    main_board.render_board()
    for event in pygame.event.get():
        if event.type == py.QUIT:
            game_running = False

    py.display.flip()

py.quit()

