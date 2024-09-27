
import random

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]  # 3x3 Tic-Tac-Toe board
        self.current_winner = None  # Track the winner!

    def print_board(self):
        # Print the board in 3x3 format
        for row in [self.board[i * 3:(i + 1) * 3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        # Print a sample board with index numbers (for users to pick a move)
        number_board = [[str(i) for i in range(j * 3, (j + 1) * 3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        # Return a list of available moves (empty spots)
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        # Return whether there are any empty squares
        return ' ' in self.board

    def num_empty_squares(self):
        # Return the number of empty squares
        return self.board.count(' ')

    def make_move(self, square, letter):
        # Make a move on the board
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        # Check if there's a winner (3 in a row, column or diagonal)
        row_ind = square // 3
        row = self.board[row_ind * 3:(row_ind + 1) * 3]
        if all([spot == letter for spot in row]):
            return True
        col_ind = square % 3
        column = [self.board[col_ind + i * 3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        return False


def evaluate(board, depth):
    # Return a score based on the current state
    if board.current_winner == 'X':  # AI is 'X'
        return 1 * (9 - depth)
    elif board.current_winner == 'O':  # Opponent is 'O'
        return -1 * (9 - depth)
    else:
        return 0


def a_star_move(board, player):
    # Recursive A* search to choose the best move
    if player == 'X':  # AI
        best = {'position': None, 'score': -float('inf')}
    else:  # Human
        best = {'position': None, 'score': float('inf')}

    if not board.empty_squares() or board.current_winner:
        score = evaluate(board, 0)
        return {'position': None, 'score': score}

    for possible_move in board.available_moves():
        board.make_move(possible_move, player)

        if player == 'X':  # AI is maximizing
            sim_score = a_star_move(board, 'O')  # Simulate opponent's move
        else:  # Human is minimizing
            sim_score = a_star_move(board, 'X')  # Simulate AI's move

        board.board[possible_move] = ' '  # Undo the move
        board.current_winner = None  # Reset winner

        sim_score['position'] = possible_move  # Record this move

        if player == 'X':  # AI is maximizing
            if sim_score['score'] > best['score']:
                best = sim_score
        else:  # Human is minimizing
            if sim_score['score'] < best['score']:
                best = sim_score

    return best


def rule_based_agent(board):
    return random.choice(board.available_moves())


def simulate_game():
    results = {'wins': 0, 'losses': 0, 'draws': 0}

    for _ in range(100):
        game = TicTacToe()

        while game.empty_squares():
            # Rule-based agent move
            rule_move = rule_based_agent(game)
            if game.make_move(rule_move, 'O'):
                if game.current_winner:
                    results['losses'] += 1
                    break

            # A*-search AI move
            if game.empty_squares():
                best_move = a_star_move(game, 'X')['position']
                game.make_move(best_move, 'X')

                if game.current_winner:
                    results['wins'] += 1
                    break

        if not game.current_winner:
            results['draws'] += 1

    return results


if __name__ == '__main__':
    results = simulate_game()
    print(f"After 100 games: {results['wins']} wins, {results['losses']} losses, and {results['draws']} draws.")
