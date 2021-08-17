# Author: Satyam Patel
# Date: 12:53 PM 6/02/2021
# Description: Implements the Kuba game.

class Player:
    """ 
    Holds all data for a player object.
    """
    def __init__(self, player_info):
        """
        initializes the name, color and captured marbles for the player
        """
        self._name = player_info[0]
        self._color = player_info[1]
        self._captured = []

    def get_name(self):
        """ 
        returns player name
        """
        return self._name

    def get_color(self):
        """
        returns marble color of player
        """
        return self._color

    def get_captured(self):
        """
        returns captured marbles of player
        """
        return self._captured

    def capture(self, marble):
        """
        captures marble
        """
        self._captured.append(marble)
    
    def get_captured_count(self, color):
        """
        returns the number of input color marbles captured
        """
        count = 0
        for marble in self._captured:
            if marble == color:
                count += 1
        return count

    def get_captured_counts(self):
        """
        returns a dict of the marble counts captured
        """
        counts = {"W":0, "B":0, "R":0}
        for marble in self.get_captured():    
            if marble in counts:
                counts[marble] += 1
        return counts


class KubaGame:
    """ 
    Main class for the game. 
    """

    def __init__(self, player_a_info, player_b_info):
        """ 
        Initializes the game board and also maps players to their color. 
        Initializes current player turn as well
        Initializes game win state.
        Initializes the board history list.
        player_x_info needs to be passed in as a tuple: ("Name", "W") or ("Name", "B")
        """
        self._board = [['W','W','X','X','X','B','B'],
                       ['W','W','X','R','X','B','B'],
                       ['X','X','R','R','R','X','X'],
                       ['X','R','R','R','R','R','X'],
                       ['X','X','R','R','R','X','X'],
                       ['B','B','X','R','X','W','W'],
                       ['B','B','X','X','X','W','W']]

        self._board_history = []
        self._current_turn = None
        self._winner = None

        self._player_a = Player(player_a_info)
        self._player_b = Player(player_b_info)

        self._players = {self._player_a.get_name() : self._player_a, 
                         self._player_b.get_name() : self._player_b}

        self._error_messages = []

    def get_board(self):
        """ 
        returns the board
        """
        return self._board

    def _set_board(self, board):
        """
        sets the board to the passed in one
        """
        self._board = board

    def get_board_history(self):
        """
        returns the board history
        """
        return self._board_history

    def get_current_turn(self):
        """
        returns the name of the player whose turn it is. Returns None if no player has started yet
        """
        if self._current_turn is not None:
            return self._current_turn.get_name()
        else:
            return None

    def _set_current_turn(self, player):
        """
        sets the current turn of the game
        """
        self._current_turn = player

    def get_player(self, playername):
        """
        returns player object from player name
        """
        return self._players[playername]

    def get_players(self):
        """
        returns the entire player dict
        """
        return self._players

    def get_player_a(self):
        """
        returns the player_a object
        """
        return self._player_a

    def get_player_b(self):
        """
        returns the player_b object
        """
        return self._player_b

    def get_winner(self):
        """
        Returns the name of the winner of the game.
        Returns None if no winner yet.
        """
        if self._winner is not None:
            return self._winner.get_name()
        return None

    def _set_winner(self, player):
        """
        sets the winner of the game
        """
        self._winner = player

    def get_captured(self, playername):
        """
        Returns the number of red marbles captured by this player.
        """

        return self.get_player(playername).get_captured_count("R")

    def get_marble(self, coordinates):
        """
        Returns the marble at this coordinate
        Returns X if no marble is present.
        """
        return self.get_board()[coordinates[0]][coordinates[1]]

    def get_marble_count(self):
        """
        returns the number of white, black, and red marbles in a tuple.
        (W,B,R)
        """
        counts = {"W":0, "B":0, "R":0}

        for row in self.get_board():
            for marble in row:
                if marble in counts:
                    counts[marble] += 1

        return (counts["W"], counts["B"], counts["R"])

    def print_board(self):
        """
        Prints out the board to the console.
        """
        print("      0  1  2  3  4  5  6")
        row_num = 0
        for row in self.get_board():
            print("   ", row_num, "", end="")
            row_num += 1
            for marble in row:
                char = marble
                if marble == "X":
                    char = "■"
                print(char, end="  ")
            print()
    
    def _document_error(self, message):
        """
        pushes message to the error stack
        """
        self._error_messages.append(message)

    def pop_error(self):
        """
        pops the last error message
        """
        return self._error_messages.pop()

    def _is_valid_push(self, coordinates, direction, player_marble):
        """ 
        checks if we can move in this direction at the given coordinates
        Note this function is called in a larger validation function: _move_is_valid()
        """
        # coordinates of interest
        right      = (coordinates[0], coordinates[1]+1) # immediately right
        left       = (coordinates[0], coordinates[1]-1) # immediately left
        above      = (coordinates[0]-1, coordinates[1]) # immediately above
        below      = (coordinates[0]+1, coordinates[1]) # immediately below
        leftmost   = (coordinates[0], 0) # the leftmost extreme of this row
        rightmost  = (coordinates[0], 6) # the rightmost extreme of row
        topmost    = (0, coordinates[1]) # the topmost extreme of column
        bottommost = (6, coordinates[1]) # the bottommost extreme of column

        def helper(coord_index, extreme_index, immediate, extreme):
            """
            helper that consolidates the checks into one function
            """
            row_or_col = []
            slice = []

            if coord_index == 0:
                row_or_col = self._get_column(coordinates[1])
            else:
                row_or_col = self._get_row(coordinates[0])

            if (extreme_index < coordinates[coord_index]):
                slice = row_or_col[coordinates[coord_index]:]
            else:
                slice = row_or_col[:coordinates[coord_index]]

            if player_marble == self.get_marble(extreme) and "X" not in slice:
                self._document_error("You cannot capture your own marble!")
                return False
            if coordinates[coord_index] == extreme_index:
                return True
            if self.get_marble(immediate) == "X":
                return True
            else:
                self._document_error("Cant push from this direction!")
                return False

        if direction == "L":
            return helper(1, 6, right, leftmost)

        if direction == "R":
            return helper(1, 0, left, rightmost)

        if direction == "B":
            return helper(0, 0, above, bottommost)

        if direction == "F":
            return helper(0, 6, below, topmost)

    def _move_is_valid(self, playername, coordinates, direction):
        """
        Validates move by checking:
        if game is already won,
        if it is the players turn or first move,
        if coordinates has current players marble color,
        if move can be made at all in given direction,
        """
        invalid_direction = direction not in "FBLR"
        if invalid_direction:
            self._document_error("Not a valid direction: F,B,L,R")
            return False

        invalid_player = playername not in self.get_players()
        if invalid_player:
            self._document_error("Player doesn't exist!")
            return False

        already_won = self.get_winner() != None
        if already_won:
            self._document_error("A player has already won: " + self.get_winner())
            return False

        coords_in_range = 0 <= coordinates[0] <= 6 and 0 <= coordinates[1] <= 6
        if not coords_in_range:
            self._document_error("Coordinates are not in range!")
            return False

        not_player_turn = False
        if self.get_current_turn() != None:
            not_player_turn = playername != self.get_current_turn()
        if not_player_turn:
            self._document_error("Not your turn. Current turn: " + self.get_current_turn())
            return False

        not_player_marble = self.get_marble(coordinates) != self.get_player(playername).get_color()
        if not_player_marble:
            self._document_error("Not your marble!")
            return False        

        cant_push = not self._is_valid_push(coordinates, direction, self.get_player(playername).get_color())
        if cant_push:
            self._document_error("Cant push because: " + self.pop_error())
            return False

        return True

    def _check_win_conditions(self):
        """
        Checks to see if any of the players have 7 reds or 8 of the opponents marbles.
        """
        for playername, player in self.get_players().items():            
            red_count   = player.get_captured_count("R")
            black_count = player.get_captured_count("B")
            white_count = player.get_captured_count("W")
            if red_count == 7:
                self._set_winner(player)
                return
            elif black_count == 8:
                self._set_winner(player)
                return
            elif white_count == 8:
                self._set_winner(player)    
                return
            #elif not self._are_moves_available(player):
            #    player_a = self.get_player_a()
            #    player_b = self.get_player_b()
            #    if player_a.get_name() != playername:
            #        self._set_winner(player_a)
            #    else:
            #        self._set_winner(player_b)       

    def _replace_column(self, column_index, column, board):
        """
        replaces the column in the board at column_index with the given column
        """
        row_num = 0
        for row in board:
            row[column_index] = column[row_num]
            row_num += 1

    def _replace_row(self, row_index, row, board):
        """
        replaces the row in the board at row_index with the given row
        """
        board[row_index] = list(row)

    def _get_row(self, row_index):
        """ 
        returns the row at row_index of the board
        """
        return list(self.get_board()[row_index])

    def _get_column(self, column_index):
        """
        returns the column at the column_index of the board
        """
        return [row[column_index] for row in self.get_board()]

    def _is_same_board(self, board_1, board_2):
        """
        returns true if board_1 matches board_2
        """
        for index in range(len(board_1)):
            if board_1[index] != board_2[index]:
                return False
        return True

    def _copy_board(self, board):
        """
        returns a copy of the input board
        """
        copy = []
        for row in board:
            copy.append(list(row))
        return copy

    def _push_right(self, position, a_list):
        """
        takes a list and pushes the element to the right. If there is something there, it pushes that element as well. 
        If an element gets pushed out of the list we return that
        """
        for index in range(position, len(a_list)):
            if a_list[index] == "X":
                a_list.pop(index)
                a_list.insert(position,"X")
                return None
        a_list.insert(position, "X")
        return a_list.pop()

    def _set_next_turn(self, current_player):
        """
        Sets the next turn of the game
        """
        if current_player == self.get_player_a():
            self._set_current_turn(self.get_player_b())
        else:
            self._set_current_turn(self.get_player_a())

    def _are_moves_available(self, player):
        """ 
        returns true if there is at least one move available for this player 
        """
        moves = "LRFB"
        name = player.get_name()
        player_marble = player.get_color()

        for row_index, row in enumerate(self.get_board()):
            for col_index, marble in enumerate(row):
                if marble == player_marble:
                    for move in moves:
                        if self._move_is_valid(name, (row_index, col_index), move):
                            return True
        return False

    def make_move(self, playername, coordinates, direction):
        """ 
        Win conditions are analyzed.
        Attempts to make a move for playername at coordinates in direction.
        If initial validation passes, we make the move on a copy of the current 
        board and compare it to the board 1 move prior.
        If move is unique: the board, current turn, and captured marbles for current 
        player are updated. 
        Player turn is updated (no repeated turns for our implementation).
        """
        self._check_win_conditions()

        if (not self._move_is_valid(playername, coordinates, direction)):
            return False
        
        # make copy of board
        board_copy = self._copy_board(self.get_board())
        captured = None

        # make move on the copy
        if direction == "R":
            row_index = coordinates[0]
            row = self._get_row(row_index)
            captured = self._push_right(coordinates[1], row)
            self._replace_row(row_index, row, board_copy)

        elif direction == "B":
            column_index = coordinates[1]
            column = self._get_column(column_index)
            captured = self._push_right(coordinates[0], column)
            self._replace_column(column_index, column, board_copy)

        elif direction == "L":
            row_index = coordinates[0]
            row = self._get_row(row_index)
            row.reverse()
            captured = self._push_right(6 - coordinates[1], row)
            row.reverse()
            self._replace_row(row_index, row, board_copy)

        elif direction == "F":
            column_index = coordinates[1]
            column = self._get_column(column_index)
            column.reverse()
            captured = self._push_right(6 - coordinates[0], column)
            column.reverse()
            self._replace_column(column_index, column, board_copy)      

        # check if the copy is the same as the last board
        history = self.get_board_history()
        if len(history) > 1:
            if self._is_same_board(history[-2], board_copy):
                self._document_error("Cannot make a circular move!")
                return False
        
        # set the board and capture marble!
        if captured is not None:
            self.get_player(playername).capture(captured)
        self._set_board(board_copy)
        history.append(board_copy)
        self._set_next_turn(self.get_player(playername))
        return True

# uncomment the lines below to play the game in the console!

def play_game():
    print("Welcome to the Kuba Game!")
    print("Enter q to quit during game loop.")
    print('All inputs need to be in the form "name row,col direction"')
    print('Valid directions are: R,L,F,B')
    print("Player 1 has black marbles and Player 2 has white marbles.")

    player_1 = input("Player 1 Name: ")
    player_2 = input("Player 2 Name: ")

    kg = KubaGame((player_1,'B'),(player_2, 'W'))
    kg.print_board()

    while(kg.get_winner() == None):
        # prompt user for moves
        user_input = input("name row,col direction: ")
        if user_input.lower() == "q":
            return
        inputs = user_input.split(' ')
        name = ""
        position = (0,0)
        direction = "F"
        try:
            name = inputs[0]
            position = eval(inputs[1])
            if len(position) != 2:
                print("invalid input!")
                continue
            direction = inputs[2]
        except:
            print("Input invalid!")
            continue

        if not kg.make_move(name, position, direction):
            print()
            kg.print_board()
            print()
            print(kg.get_player_a().get_name(), " has: ", kg.get_player_a().get_captured_counts())
            print(kg.get_player_b().get_name(), " has: ", kg.get_player_b().get_captured_counts())
            print()
            print(kg.pop_error())
        else:
            print()
            kg.print_board()
            print()
            print(kg.get_player_a().get_name(), " has: ", kg.get_player_a().get_captured_counts())
            print(kg.get_player_b().get_name(), " has: ", kg.get_player_b().get_captured_counts())
    print()
    print("WINNER: ", kg.get_winner())

if __name__ == "__main__":
    play_game()
