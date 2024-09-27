import random

# Define the Tic-Tac-Toe board and rules
class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # 3x3 board
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        # Show board with numbers for each square
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # Check the row
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True
        # Check column
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        # Check diagonals
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        return False

# Unbeatable rule-based agent (O)
class RuleBasedAgent:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        # If center is available, take it
        if 4 in game.available_moves():
            return 4

        # Check if O can win in the next move
        for move in game.available_moves():
            game.make_move(move, self.letter)
            if game.current_winner:
                return move
            game.board[move] = ' '  # Undo move

        # Check if X is about to win, and block it
        opponent = 'X'
        for move in game.available_moves():
            game.make_move(move, opponent)
            if game.current_winner:
                game.board[move] = ' '  # Undo move
                return move
            game.board[move] = ' '  # Undo move

        # Take any available corner
        for move in [0, 2, 6, 8]:
            if move in game.available_moves():
                return move

        # Take any remaining side
        for move in game.available_moves():
            return move

# Play the game
def play_game(game, x_player, o_player, print_game=True):
    if print_game:
        game.print_board_nums()

    letter = 'X'  # Human player goes first
    while game.empty_squares():
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            valid_square = False
            while not valid_square:
                square = input('Your turn (0-8): ')
                try:
                    square = int(square)
                    if square not in game.available_moves():
                        raise ValueError
                    valid_square = True
                except ValueError:
                    print('Invalid move. Try again.')

        if game.make_move(square, letter):
            if print_game:
                print(f'{letter} makes a move to square {square}')
                game.print_board()
                print('')

            if game.current_winner:
                if print_game:
                    print(f'{letter} wins!')
                return letter
            letter = 'O' if letter == 'X' else 'X'

    if print_game:
        print("It's a tie!")
    return 'Tie'


if __name__ == '__main__':
    game = TicTacToe()
    x_player = None  # Human player X
    o_player = RuleBasedAgent('O')  # Rule-based agent O
    play_game(game, x_player, o_player, print_game=True)
