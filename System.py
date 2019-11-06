from Checkers_UI import *

class player:

    def __init__(self,player_name = None , checker_pieces = None):
        self.player_name = str(player_name)
        self.checkers_pieces = checker_pieces

class player_handling:

    def __init__(self ,player_one = None ,player_two = None):

        self.player_one = player_one
        self.player_two = player_two

    def create_teams(self):

        team_one = self.player_one
        team_two = self.player_two
        team_one.checkers_pieces = create_pieces()
        team_two.checkers_pieces = create_pieces()
        for piece in team_one.checkers_pieces:
            piece.team = 'team one'
        for piece in team_two.checkers_pieces:
            piece.team = 'team two'

class game_master:

    def __init__(self, players_mechanism):
        self.player_mechanism = players_mechanism

    def start_game(self):
        player_mech = self.player_mechanism
        name_one = input("Enter name : ")
        name_two = input("Enter name : ")
        names_valid = name_one.capitalize() != name_two.capitalize()
        if names_valid == True:
            print("Names created successfully")
        else:
            print("Pick different names\n")
            names_valid = False
            while names_valid == False:
                name_one = input("Enter Another name : ")
                name_two = input("Enter Another name : ")
                names_valid = name_one.capitalize() != name_two.capitalize()
                if names_valid == False:
                    print("Pick different names\n")
        NPO = player(player_name=name_one)
        NPT = player(player_name=name_two)
        player_mech.player_one = NPO
        player_mech.player_two = NPT
        print("Players created successfully")

    def setup_pieces(self,board_layout):

        PM = self.player_mechanism
        team_one = PM.player_one
        team_two = PM.player_two

############################### TEAM ONE ##########################################
        right = True
        np_one = 0  # Number of pieces
        cr_one, cc_one = 0, 0

        while np_one <= 15:
            while right:
                board_layout[cr_one][cc_one].occupied = True
                board_layout[cr_one][cc_one].current_pieces = team_one.checkers_pieces[np_one]
                team_one.checkers_pieces[np_one].current_position = [cr_one,cc_one]
                np_one += 1
                cc_one += 1
                if cc_one == 8:
                    right = False
                    cr_one += 1
                    cc_one = 7

            while not right:
                board_layout[cr_one][cc_one].occupied = True
                board_layout[cr_one][cc_one].current_pieces = team_one.checkers_pieces[np_one]
                team_one.checkers_pieces[np_one].current_position = [cr_one,cc_one]
                np_one += 1
                cc_one -= 1
                if cc_one == -1:

                    right = True
                    cr_one += 1
                    cc_one = 0
######################################  TEAM TWO #######################################

            right = False
            np_two = 0  # Number of pieces
            cr_two, cc_two = 7, 7

            while np_two <= 15:
                while not right:
                    #print(f"Np two is {np_two}\tcc_two is {cc_two}\tcr_two is {cr_two}\n")
                    board_layout[cr_two][cc_two].occupied = True
                    board_layout[cr_two][cc_two].current_pieces = team_two.checkers_pieces[np_two]
                    team_two.checkers_pieces[np_two].current_position = [cr_two,cc_two]
                    np_two += 1
                    cc_two -= 1
                    if cc_two == -1:
                        right = True
                        cr_two -= 1
                        cc_two = 0
                while right:
                    #print(f"Np two is {np_two}\tcc_two is {cc_two}\tcr_two is {cr_two}\n")
                    board_layout[cr_two][cc_two].occupied = True
                    board_layout[cr_two][cc_two].current_pieces = team_two.checkers_pieces[np_two]
                    team_two.checkers_pieces[np_two].current_position = [cr_two,cc_two]
                    cc_two += 1
                    np_two += 1
                    if cc_two == 8:
                        right = False
                        cr_two -= 1
                        cc_two = 7

    def draw_pieces(self):

        pass
##################################################################################################################################
def process_name(name_one ,name_two):
    valid = False
    if name_one != name_two:
        valid = True
    try:
        if (name_one * 0 == 0 and name_two * 0 == 0) == True:
            print("Name Invalid")
        else:
            valid = True
    except:
       print("err")
    return valid

def create_pieces():
    alphabet = [chr(a) for a in range (65,83)]
    numbers = [i for i in range(1,20)]
    team_pieces = []
    for j in range(16):
        new_piece = checker_piece(piece_ID = str(alphabet[j]+str(numbers[j])))
        team_pieces.append(new_piece)
    return team_pieces


