import pygame as py
import numpy as np

# ///////////////////////////////////////////////////////////////////////////////////


"""
    @Author: Leo Mwenda Ngari
    @name: Checkers game

    @version control: v0.0.1
    
"""
game_running = True
S_HEIGHT, S_WIDTH = 700, 700
BOARD_DIM = 8
POSITION_DIM = 60
PIECE_DIM = 48
game_pieces = []
SCREEN_SIZE = [S_WIDTH, S_HEIGHT]
game_board = py.display.set_mode(SCREEN_SIZE)
py.init()

# ///////////////////////////////////////////////////////////////////////////////////////////////

colors = {
    "white": [225, 220, 200],
    "white_hover": [61, 46, 22],
    "black": [90, 98, 92],
    "black_hover": [61, 46, 22],
    "red": [73, 57, 44],
    "color_a": [0, 10, 10],
    "threat": [218, 31, 30],
    "text_color": [152, 201, 235]
}
images = [
    py.image.load(r"./views/bp.png"),
    py.image.load(r"./views/rp.png"),
    py.image.load(r"./views/bpk.png"),
    py.image.load(r"./views/rpk.png"),
]


# ///////////////////////////////////////////////////////////////////////////////////////////////
class ScoreBoard:

    font = py.font.Font('freesansbold.ttf', 16)
    large_font = py.font.Font('freesansbold.ttf', 32)

    def __init__(self):
        self._background_color = "white"
        self._text_color = "white"
        self.width = S_WIDTH
        self.height = (S_HEIGHT - (BOARD_DIM * POSITION_DIM)) / 2 - 50
        self.pos_x = 0
        self.pos_y = 0
        self.text = "Hello Players"

    def get_rect(self, score_one, score_two):

        offset_x = (S_WIDTH - (BOARD_DIM * POSITION_DIM)) / 2
        p_one_text = self.font.render('Player One', True, colors[self._text_color])
        p_two_text = self.font.render('Player Two', True, colors[self._text_color])
        s_one = self.large_font.render(str(score_one), True, colors[self._text_color])
        s_two = self.large_font.render(str(score_two), True, colors[self._text_color])
        space_x = 300
        # player one
        game_board.blit(p_one_text, [offset_x, 10])
        game_board.blit(s_one, [offset_x, 55])
        game_board.blit(images[0], [offset_x + 50, 40])

        game_board.blit(p_two_text, [offset_x + space_x, 10])
        game_board.blit(s_two, [offset_x + space_x, 55])
        game_board.blit(images[1], [offset_x + space_x + 50, 40])


class Board:
    def __init__(self):

        self._background = "color_a"
        self.height = BOARD_DIM * POSITION_DIM
        self.width = BOARD_DIM * POSITION_DIM
        self.space_x = 10
        self.space_y = 10
        self.display_board = ScoreBoard()
        self.isPlayerOne = False  # Player one -> Blue :::  Player Two -> Red
        self.blue_pieces = [Piece(piece_type=0) for i in range(12)]
        self.red_pieces = [Piece(piece_type=1) for i in range(12)]
        self.red_victims = 0
        self.blue_victims = 0
        self.offset_x = (S_WIDTH - (BOARD_DIM * POSITION_DIM)) / 2
        self.offset_y = (S_HEIGHT - (BOARD_DIM * POSITION_DIM)) / 2
        self.positions = np.array(self.set_pieces(), dtype=Position)
        self.clicked_position = None
        self.init_board()

    def render_display(self):
        self.display_board.get_rect(self.red_victims, self.blue_victims)

    def change_turn(self):
        self.isPlayerOne = not self.isPlayerOne

    def init_board(self):

        # assign the first chips to default positions
        player_one = [0, 1, 2]
        player_two = [-1, -2, -3]
        players = [player_one, player_two]
        pieces = [self.red_pieces, self.blue_pieces]
        player_row_structure = [
            [0, 2, 4, 6],
            [1, 3, 5, 7]
        ]
        a = 1
        for player in range(1, len(players) + 1):
            c = 0
            for row in players[player - 1]:
                a = 1 if a == 0 else 0
                for i in player_row_structure[a]:
                    cp = self.positions[i, row]
                    cp.assign_piece(pieces[player - 1][c])
                    c += 1

    @staticmethod
    def set_pieces():
        count = 0
        positions = []
        pos_colors = ["white", "black"]
        for i in range(BOARD_DIM):
            positions.append([])
            for j in range(BOARD_DIM):
                temp = Position(POSITION_DIM, j * POSITION_DIM, i * POSITION_DIM, pos_colors[count % 2])
                positions[i].append(temp)
                count += 1
            count += 1
        return positions

    def get_background(self):
        return self._background

    def place_board(self):
        offset_x = (S_WIDTH - self.width) / 2
        offset_y = (S_HEIGHT - self.height) / 2
        return [offset_x, offset_y]

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
        for row in self.positions:
            for pos in row:
                pos.get_rect()
                pos.show_piece()

    def listen_for_hover(self):
        mouse_pos = self.get_mouse_position()
        if mouse_pos:
            self.positions[mouse_pos[0], mouse_pos[1]].hovered(self.isPlayerOne)

    def listen_for_click(self, py_events):
        for py_event in py_events:
            if py_event.type == py.MOUSEBUTTONDOWN:
                mouse_pos = self.get_mouse_position()
                if not mouse_pos:
                    return
                possible_position = self.positions[mouse_pos[0], mouse_pos[1]]

                if self.clicked_position \
                        and self.clicked_position.is_clicked \
                        and possible_position in self.clicked_position.highlighted_partners:
                    # make move
                    self.move_piece(self.clicked_position, possible_position)
                    return

                if self.positions[mouse_pos[0], mouse_pos[1]].has_piece:
                    clicked_pos = self.positions[mouse_pos[0], mouse_pos[1]]
                    if self.clicked_position and self.clicked_position.is_clicked:
                        self.clicked_position.un_clicked()
                        self.clicked_position.de_threaten()
                    if self.clicked_position != clicked_pos:
                        if clicked_pos.clicked(self.isPlayerOne):
                            self.clicked_position = clicked_pos
                            self.look_for_possibilities()
                    else:
                        self.clicked_position.clicked(self.isPlayerOne)
                        self.look_for_possibilities()
                    return

    def get_mouse_position(self):
        max_d = BOARD_DIM - 1
        mouse_position = py.mouse.get_pos()
        pos_x = int((mouse_position[0] - self.offset_x) // POSITION_DIM)
        pos_y = int((mouse_position[1] - self.offset_y) // POSITION_DIM)
        if pos_y < 0 or pos_y > max_d or pos_x > max_d or pos_x < 0:
            return None
        # Make sure the player hovers over the right pieces
        return [pos_y, pos_x]

    def look_for_possibilities(self):
        if self.clicked_position.is_clicked:
            args = [self.clicked_position.off_[0], self.clicked_position.off_[1]]
            piece_on_current_type = self.clicked_position.piece.type
            current_position = self.locate_on_grid(args)
            # print(f" Current position : {current_position}")
            poss_landings = self.possible_landings(current_position)

            """
            for row in self.positions:
                for el in row:
                    pass
                    # print(el.has_piece, end = " ")
                # print()
            """
            # we look at the direction
            verified = []
            victim = []
            for poss_landing in poss_landings:

                # remove occupied landings

                if not self.get_position_at(poss_landing).has_piece:
                    if piece_on_current_type < 2:
                        if self.isPlayerOne:
                            # left to right
                            if poss_landing[0] < current_position[0]:
                                verified.append(poss_landing)
                        else:
                            if poss_landing[0] > current_position[0]:
                                verified.append(poss_landing)
                    else:

                        verified.append(poss_landing)

                else:
                    is_opponent = (self.isPlayerOne and self.get_position_at(poss_landing).piece.type % 2 == 1) or \
                                  (not self.isPlayerOne and self.get_position_at(poss_landing).piece.type % 2 == 0)
                    if is_opponent:
                        # we get opponent position
                        gap_to_opponent = [current_position[0] - poss_landing[0],
                                           current_position[1] - poss_landing[1]]
                        intended_landing_point = [poss_landing[0] - gap_to_opponent[0],
                                                  poss_landing[1] - gap_to_opponent[1]]

                        if not self.get_position_at(intended_landing_point) or \
                                self.get_position_at(intended_landing_point).has_piece:
                            continue
                        if piece_on_current_type < 2:
                            if (self.isPlayerOne and poss_landing[0] < current_position[0]) or \
                                    (not self.isPlayerOne and poss_landing[0] > current_position[0]):
                                # left to right
                                victim.append(poss_landing)
                                verified.append(intended_landing_point)
                        else:
                            victim.append(poss_landing)
                            verified.append(intended_landing_point)

            self.clicked_position.threaten([self.get_position_at(v) for v in victim])
            self.clicked_position.highlight_master([self.get_position_at(v) for v in verified])

    @staticmethod
    def possible_landings(coordinates):
        locations = [
            [coordinates[0] + 1, coordinates[1] - 1],
            [coordinates[0] + 1, coordinates[1] + 1],
            [coordinates[0] - 1, coordinates[1] + 1],
            [coordinates[0] - 1, coordinates[1] - 1],
        ]

        true_locations = []
        for location in locations:
            if not (location[0] < 0 or location[0] > BOARD_DIM - 1 or location[1] < 0 or location[1] > BOARD_DIM - 1):
                true_locations.append(location)
        return true_locations

    @staticmethod
    def locate_on_grid(position: list):
        return [int(position[0] // POSITION_DIM) - 1, int(position[1] // POSITION_DIM) - 1]

    def get_position_at(self, coordinates):
        if coordinates[0] >= BOARD_DIM or coordinates[0] <= -1 or coordinates[1] <= -1 or coordinates[1] >= BOARD_DIM:
            return None
        return self.positions[coordinates[1], coordinates[0]]

    def move_piece(self, fro, to):
        fro_grid_pos = [int(fro.pos_x // POSITION_DIM), int(fro.pos_y // POSITION_DIM)]
        to_grid_pos = [int(to.pos_x // POSITION_DIM), int(to.pos_y // POSITION_DIM)]
        gap = [fro_grid_pos[0] - to_grid_pos[0], fro_grid_pos[1] - to_grid_pos[1]]
        if abs(gap[0]) > 1 and abs(gap[1]) > 1:
            skipped_pos = [to_grid_pos[0] + int(gap[0] // 2), to_grid_pos[1] + int(gap[1] // 2)]
            jumped = self.get_position_at(skipped_pos)
            if jumped in fro.victim_list:
                # kill the piece
                if jumped.piece.type % 2 == 0:
                    self.blue_victims += 1
                else:
                    self.red_victims += 1
                jumped.kill_piece()

        moving_piece = fro.get_piece()
        fro.remove_piece()
        to.assign_piece(moving_piece)

        # check if we've skipped over a chip in the victim list

        # check if the piece should be promoted
        if self.isPlayerOne and to_grid_pos[0] == 0:
            to.promote_piece()
        elif not self.isPlayerOne and to_grid_pos[0] == (BOARD_DIM - 1):
            to.promote_piece()

        self.change_turn()
        self.clicked_position.un_clicked()

    def game_is_over(self):
        if self.red_victims == 12 or self.blue_victims == 12:
            return True
        return False


class Piece:
    def __init__(self, piece_type):
        self.type = piece_type
        self._appearance = images[self.type]
        self.dead = False
        """
        0 - blue
        1 - red
        2 - blue king
        3 - red king
        """

    def __repr__(self):
        return f"Piece type: {self.type}"

    def __str__(self):
        return f"Piece type: {self.type}"

    def get_appearance(self):
        return self._appearance

    def killed(self):
        self.dead = True

    def promoted(self):
        self.type += 2
        self._appearance = images[self.type]


class Position:

    def __init__(self, h, pos_x, pos_y, color, piece=None):
        self.height = h
        self.color = color
        self.default_color = self.color
        self.hover_color = f"{self.color}_hover"
        self.threat_color = "threat"
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.is_hovered = False
        self.is_clicked = False
        self.offset_x = (S_WIDTH - (BOARD_DIM * POSITION_DIM)) / 2
        self.offset_y = (S_HEIGHT - (BOARD_DIM * POSITION_DIM)) / 2
        self.off_ = [self.offset_x + self.pos_x, self.offset_y + self.pos_y]
        self.has_piece = False
        self.is_highlighted = False
        self.im_a_victim = False
        self.highlighted_partners = []
        self.victim_list = []
        self.piece = piece

    def __repr__(self):
        return f"Position @ [{self.pos_x}, {self.pos_y}]"

    def __str__(self):
        return f"Position @ [{self.pos_x}, {self.pos_y}]"

    def get_piece(self):
        return self.piece

    def get_rect(self, screen=game_board):
        if not self.is_hovered and not self.is_clicked and not self.is_highlighted and not self.im_a_victim:
            self.color = self.default_color
        py.draw.rect(screen,
                     colors[self.color],
                     [self.off_[0], self.off_[1], self.height, self.height])

        if not self.is_clicked:
            self.is_hovered = False

    def assign_piece(self, piece: Piece):
        self.has_piece = True
        self.piece = piece

    def show_piece(self):
        # center the piece
        piece_offset = (POSITION_DIM - PIECE_DIM) / 2
        if self.has_piece and self.piece:
            game_board.blit(self.piece.get_appearance(), [self.off_[0] + piece_offset, self.off_[1] + piece_offset])

    def hovered(self, is_player_one):
        if self.has_piece and self.piece and (
                (self.piece.type % 2 == 0 and is_player_one) or (self.piece.type % 2 != 0 and not is_player_one)):
            self.color = self.hover_color
            self.is_hovered = True

    def clicked(self, is_player_one):
        if not self.has_piece:
            return False
        if (self.piece.type % 2 == 0 and is_player_one) or (self.piece.type % 2 != 0 and not is_player_one):
            self.color = self.hover_color
            self.is_clicked = True
            return True

    def un_clicked(self):
        self.color = self.default_color
        self.is_clicked = False
        self.remove_highlight_master()
        self.de_threaten()

    def highlight_master(self, partners: list):
        self.highlighted_partners = partners
        for partner in partners:
            # print(partner)
            if partner:
                partner.highlight_partner()

    def highlight_partner(self):
        self.color = self.hover_color
        self.is_highlighted = True

    def remove_highlight_master(self):

        self.color = self.default_color
        for partner in self.highlighted_partners:
            if partner:
                partner.is_highlighted = False

    def remove_piece(self):
        self.piece = None
        self.has_piece = False

    def marked(self):
        self.im_a_victim = True
        self.color = self.threat_color

    def de_marked(self):
        self.im_a_victim = False
        self.color = self.default_color

    def threaten(self, positions):
        self.victim_list = positions
        for victim in positions:
            victim.marked()

    def de_threaten(self):
        for victim in self.victim_list:
            victim.de_marked()
        self.victim_list = []

    def kill_piece(self):
        if self.has_piece and self.piece:
            self.piece.killed()
        self.has_piece = False
        self.piece = None

    def promote_piece(self):
        if self.has_piece and self.piece and not self.piece_is_king():
            self.piece.promoted()

    def piece_is_king(self):
        if self.has_piece and self.piece:
            if self.piece.type >= 2:
                return True
        return False


class Game:

    def __init__(self):
        self._board = Board()
        self.game_is_done = False
        self.game_running = True

    def play_game(self):
        global game_board
        while self.game_running:

            game_events = py.event.get()
            game_board.fill(colors["red"])
            self._board.render_display()
            self._board.get_rect()
            self._board.listen_for_hover()
            self._board.render_board()
            self._board.listen_for_click(game_events)

            for event in game_events:
                if event.type == py.QUIT:
                    self.game_running = False
                    self.game_is_done = True
            if self._board.game_is_over():
                self.game_running = False
            py.display.flip()
        if not self.game_is_done:
            self.__init__()
            self.game_running = True
            self.play_game()


# ///////////////////////////////////////////////////////////////////////////////////////////////


game = Game()


def pre_checks():
    if S_WIDTH < BOARD_DIM * POSITION_DIM:
        print("Screen Size too small")
        exit(-1)


pre_checks()

# ///////////////////////////////////////////////////////////////////////////////////////////////


if __name__ == '__main__':
    game.play_game()