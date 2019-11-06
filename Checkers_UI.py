"""""""""
MY  VERSION OF CHECKERS GAME PURELY IN PYTHON 3.7 USING PYGAME
        AUTHOR : lEO MWENDA NGARI
        GITHUB : NGAREOEL

    The game view user interface 
    Game board view 
    Checkers move UI 
"""""
from System import *
import pygame

################################ THE GAME CONTENTS #########################
class board:
    def __init__(self, board_layout):
        self.board_layout = board_layout

    def make_board(self):
        pygame.draw.rect(main_game_window, Variables.board_color,
                         [Variables.corners, Variables.corners, Variables.piece_size * 8,
                          Variables.piece_size * 8])  ##The actual game board

class board_piece:
    def __init__(self, piece_ID, occupied , position_x = None, position_y = None, current_piece = None, color = None , default_color = None ,):
        self.piece_ID = piece_ID
        self.position_x = position_x
        self.position_y = position_y
        self.current_piece = current_piece
        self.color = color
        self.default_color = default_color
        self.occupied = occupied

class checker_piece:
    def __init__(self ,piece_ID, current_position = None, team = None):
        self.current_position = current_position
        self.piece_ID = piece_ID
        self.team = team

""""
GAME VARIABLES 
"""

class Variables:
    ######################################  RGB values  ##################
    white = [225, 225, 225]
    black = [0, 0, 0]
    board_color = [234, 255, 0]
    background_color = [133, 143, 122]
    team_one_color = []
    team_two_color = []
    color_one = [151, 69, 64]
    color_two = [192, 168, 140]
    corners = 50  # Bars around the board for apperance purposes
    piece_size = 80  # the board piece width and height
    window_height, window_width = piece_size * 8 + 2 * corners, piece_size * 8 + 2 * corners
    checker_piece_radius = 30

    game_end = False
    ###### For board ID
    letters = [chr(a) for a in range(97,105)]
    numbers = [str(a) for a in range(9)]
    ####### For Checkers pieces ID
    c_letters = [chr(a) for a in range(65,79)]
    c_numbers = [str(a) for a in range(17)]
"""
Static Methods
"""


def add_pieces(board_layout):
    right = True
    np = 0  # Number of pieces
    cr, cc = 0, 0
    while np <= 48 and cr <= 7:
        while right:
            if np % 2 == 0:
                piece_color = Variables.color_one
            else:
                piece_color = Variables.color_two
            board_layout[cr][cc].color = piece_color
            board_layout[cr][cc].default_color = piece_color
            board_layout[cr][cc].position_x = Variables.corners + cc * Variables.piece_size
            board_layout[cr][cc].position_y = Variables.corners + cr * Variables.piece_size
            cc += 1
            np += 1
            if cc == 8:
                right = False
                cr += 1
                cc = 7

        while not right:
            if np % 2 == 0:
                piece_color = Variables.color_one
            else:
                piece_color = Variables.color_two
            board_layout[cr][cc].color = piece_color
            board_layout[cr][cc].default_color = piece_color
            board_layout[cr][cc].position_x = Variables.corners + cc * Variables.piece_size
            board_layout[cr][cc].position_y = Variables.corners + cr * Variables.piece_size
            cc -= 1
            np += 1
            if cc == -1:
                right = True
                cr += 1
                cc = 0


def make_layout():
    """"
    Make the board abd load the board squares/Pieces

    """""
    total_layout = [[], [], [], [], [], [], [], []]
    for row in range(8):
        for el in range(8):
            piece_name = Variables.letters[row] + Variables.numbers[el]
            the_game_piece = board_piece(piece_ID=piece_name,occupied=False)
            total_layout[row].append(the_game_piece)
    return total_layout


def draw_board_pieces(game_layout):
    for row in game_layout:
        for piece in row:
            pygame.draw.rect(main_game_window, piece.color,
                             (piece.position_x,
                              piece.position_y,
                              Variables.piece_size,
                              Variables.piece_size)
                             )

def draw_checkers_pieces(game_layout):

    for row in game_layout:
        for piece in row:
            if piece.occupied:
                if piece.current_pieces.team == 'team one':
                    piece_color = Variables.black
                else:
                    piece_color = Variables.white
                pygame.draw.circle(main_game_window,
                                   piece_color,
                                   [piece.position_x + Variables.piece_size //2 ,piece.position_y + Variables.piece_size // 2],
                                   Variables.checker_piece_radius)

def listen_for_mouse_event(game_board):
    for row in game_board:
        for piece in row:
            cp = pygame.mouse.get_pos()
            if (cp[0] < piece.position_x + Variables.piece_size and cp[0] >= piece.position_x) and (cp[1] < piece.position_y + Variables.piece_size and cp[1] > piece.position_y ):
                piece.color = Variables.color_one
            else:
                piece.color = piece.default_color


def setup():

    """
    To set up the board
    Draw the checker pieces
    To place the pieces at the current positions
    To add attributes  to the objects
    """""
    global main_game_window
    global game_clock
    global game_board_layout
    global game_board

    global our_game_master
    global our_mechanism

    # Setup PYGAME
    pygame.init()
    main_game_window = pygame.display.set_mode([Variables.window_height, Variables.window_width])
    pygame.display.set_caption("Checkers")
    ##################### Layout the game
    game_board_layout = make_layout()
    game_board = board(game_board_layout)
    game_clock = pygame.time
    add_pieces(game_board.board_layout)
    our_mechanism = player_handling()
    our_game_master = game_master( players_mechanism=our_mechanism)
    our_game_master.start_game()
    our_mechanism.create_teams()
    our_game_master.setup_pieces(game_board.board_layout)


    """"
    print("TEAM ONE\n\n")
    for piece in our_mechanism.player_one.checkers_pieces:
        print(f"Piece ID : {piece.piece_ID}\t Current Position : {piece.current_position}\n")
    print("TEAM TWO\n\n")
    for piece in our_mechanism.player_two.checkers_pieces:
        print(f"Piece ID :{piece.piece_ID}\t Current Position :{piece.current_position}")
        
        for row in game_board_layout:
        for piece in row:
            print(f"\nPosition X : {piece.position_x}\tPosition Y :{piece.position_y} \t Color is {piece.color}")
        print("Another row\t\t\t\t\t\n")
    """""


"""

"""
########################################### GAME LOOP ###############
if __name__ == '__main__':

    setup()

    while not Variables.game_end:
        main_game_window.fill(Variables.background_color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Variables.game_end = True
        game_board.make_board()
        draw_board_pieces(game_board.board_layout)
        draw_checkers_pieces(game_board.board_layout)
        listen_for_mouse_event(game_board.board_layout)
        pygame.display.update()
    """
   
        
    """
