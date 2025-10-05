import argparse
import copy
import sys
import time

cache = {} 
depth_limit = 7
class Board:
    def __init__(self, board: list[list[str]]):
        self.board = board
        self.width = 8
        self.height = 8

    def display(self) -> None:
        for row in self.board:
            print(''.join(row))
        print("")

class State:
    def __init__(self, board: Board, turn: str = 'r', depth: int = 0):
        """
        Initialize a State object representing the current state of the game.
        
        Parameters:
            board (Board): The current board state.
            turn (str): The current player's turn ('r' or 'b'). Default is 'r'.
            depth (int): The depth of the current state in the search tree. Default is 0.
        """
        self.board = board
        self.turn = turn
        self.depth = depth

    def get_possible_moves(self) -> list[Board]:
        mandatory_jumps = self.get_mandatory_jumps()
        if mandatory_jumps:
            return mandatory_jumps
        moves = []
        for r in range(self.board.height):
            for c in range(self.board.width):
                if self.board.board[r][c].lower() == self.turn:
                    moves.extend(self.get_piece_moves(r, c))
        return moves
    
    def get_mandatory_jumps(self) -> list[Board]:
        jumps = []
        for r in range(self.board.height):
            for c in range(self.board.width):
                if self.board.board[r][c].lower() == self.turn:
                    jumps.extend(self.get_piece_jumps(r, c))
        #print(f"get mandatory jumps called, {len(jumps)} available")
        return jumps
    
    # def get_piece_jumps(self, r: int, c: int) -> list[Board]:
    #     piece = self.board.board[r][c]
    #     jumps = []
    #     if piece.lower() == 'r' or piece == 'R':
    #         jumps.extend(self.get_jumps_for_piece(r, c, -1, 1))
    #         jumps.extend(self.get_jumps_for_piece(r, c, -1, -1))
    #         if piece == 'R':
    #             jumps.extend(self.get_jumps_for_piece(r, c, 1, 1))
    #             jumps.extend(self.get_jumps_for_piece(r, c, 1, -1))
    #     elif piece.lower() == 'b' or piece == 'B':
    #         jumps.extend(self.get_jumps_for_piece(r, c, 1, 1))
    #         jumps.extend(self.get_jumps_for_piece(r, c, 1, -1))
    #         if piece == 'B':
    #             jumps.extend(self.get_jumps_for_piece(r, c, -1, 1))
    #             jumps.extend(self.get_jumps_for_piece(r, c, -1, -1))
    #     return jumps
    
    def get_piece_jumps(self, r: int, c: int) -> list[Board]:
        piece = self.board.board[r][c]
        jumps = []
        directions = []
        if piece.lower() == 'r' or piece == 'R':
            directions = [(-1, 1), (-1, -1)]
            if piece == 'R':
                directions.extend([(1, 1), (1, -1)])
        elif piece.lower() == 'b' or piece == 'B':
            directions = [(1, 1), (1, -1)]
            if piece == 'B':
                directions.extend([(-1, 1), (-1, -1)])
        
        for dr, dc in directions:
            jumps.extend(self.get_jumps_for_piece(r, c, dr, dc, []))
        return jumps


    # def get_jumps_for_piece(self, r: int, c: int, dr: int, dc: int) -> list[Board]:
    #     jumps = []
    #     new_r, new_c = r + dr, c + dc
    #     jump_r, jump_c = new_r + dr, new_c + dc
    #     if 0 <= new_r < self.board.height and 0 <= new_c < self.board.width and \
    #        self.board.board[new_r][new_c].lower() != self.turn and self.board.board[new_r][new_c] != '.' and \
    #        0 <= jump_r < self.board.height and 0 <= jump_c < self.board.width and self.board.board[jump_r][jump_c] == '.':
    #         new_board = copy.deepcopy(self.board.board)
    #         new_board[r][c], new_board[new_r][new_c], new_board[jump_r][jump_c] = '.', '.', self.board.board[r][c]
    #         if (jump_r == 0 and self.board.board[r][c] == 'r') or (jump_r == self.board.height - 1 and self.board.board[r][c] == 'b'):
    #             new_board[jump_r][jump_c] = new_board[jump_r][jump_c].upper()
    #         jumps.append(Board(new_board))
    #         subsequent_jumps = self.get_piece_jumps(jump_r, jump_c)
    #         for sj in subsequent_jumps:
    #             jumps.append(sj)
    #     print(f"get jumps for piece called on {self.turn} at {r}, {c}, {len(jumps)} available")
    #     return jumps

    def get_jumps_for_piece(self, r: int, c: int, dr: int, dc: int, jumped: list[tuple[int, int]]) -> list[Board]:
        jumps = []
        new_r, new_c = r + dr, c + dc
        jump_r, jump_c = new_r + dr, new_c + dc
        if 0 <= new_r < self.board.height and 0 <= new_c < self.board.width and \
           self.board.board[new_r][new_c].lower() != self.turn and self.board.board[new_r][new_c] != '.' and \
           0 <= jump_r < self.board.height and 0 <= jump_c < self.board.width and self.board.board[jump_r][jump_c] == '.':
            new_board = copy.deepcopy(self.board.board)
            new_board[r][c], new_board[new_r][new_c], new_board[jump_r][jump_c] = '.', '.', self.board.board[r][c]
            if (jump_r == 0 and self.board.board[r][c] == 'r') or (jump_r == self.board.height - 1 and self.board.board[r][c] == 'b'):
                new_board[jump_r][jump_c] = new_board[jump_r][jump_c].upper()
            new_state = State(Board(new_board), self.turn, self.depth)
            subsequent_jumps = new_state.get_piece_jumps(jump_r, jump_c)
            if not subsequent_jumps:
                jumps.append(Board(new_board))
            else:
                for sj in subsequent_jumps:
                    jumps.append(sj)
        return jumps

    def get_piece_moves(self, r: int, c: int) -> list[Board]:
        piece = self.board.board[r][c]
        moves = []
        if piece.lower() == 'r' or piece == 'R':
            
            # moves.extend(self.get_moves_for_piece(r, c, 1, 1))
            # moves.extend(self.get_moves_for_piece(r, c, 1, -1))
            moves.extend(self.get_moves_for_piece(r, c, -1, 1))
            moves.extend(self.get_moves_for_piece(r, c, -1, -1))
            #print("piece is red and len moves: ", len(moves))
            if piece == 'R':
                # moves.extend(self.get_moves_for_piece(r, c, -1, 1))
                # moves.extend(self.get_moves_for_piece(r, c, -1, -1))
                moves.extend(self.get_moves_for_piece(r, c, 1, 1))
                moves.extend(self.get_moves_for_piece(r, c, 1, -1))
        elif piece.lower() == 'b' or piece == 'B':
            # moves.extend(self.get_moves_for_piece(r, c, -1, 1))
            # moves.extend(self.get_moves_for_piece(r, c, -1, -1))
            moves.extend(self.get_moves_for_piece(r, c, 1, 1))
            moves.extend(self.get_moves_for_piece(r, c, 1, -1))
            #print("piece is black and len moves: ", len(moves))
            if piece == 'B':
                # moves.extend(self.get_moves_for_piece(r, c, 1, 1))
                # moves.extend(self.get_moves_for_piece(r, c, 1, -1))
                moves.extend(self.get_moves_for_piece(r, c, -1, 1))
                moves.extend(self.get_moves_for_piece(r, c, -1, -1))
        return moves

    def get_moves_for_piece(self, r: int, c: int, dr: int, dc: int) -> list[Board]:
        moves = []
        new_r, new_c = r + dr, c + dc
        if 0 <= new_r < self.board.height and 0 <= new_c < self.board.width:
            if self.board.board[new_r][new_c] == '.':
                new_board = copy.deepcopy(self.board.board)
                new_board[r][c], new_board[new_r][new_c] = '.', self.board.board[r][c]
                if (new_r == 0 and self.board.board[r][c] == 'r') or (new_r == self.board.height - 1 and self.board.board[r][c] == 'b'):
                    new_board[new_r][new_c] = new_board[new_r][new_c].upper()
                moves.append(Board(new_board))
            elif self.board.board[new_r][new_c].lower() != self.turn:
                jump_r, jump_c = new_r + dr, new_c + dc
                if 0 <= jump_r < self.board.height and 0 <= jump_c < self.board.width and self.board.board[jump_r][jump_c] == '.':
                    new_board = copy.deepcopy(self.board.board)
                    new_board[r][c], new_board[new_r][new_c], new_board[jump_r][jump_c] = '.', '.', self.board.board[r][c]
                    if (jump_r == 0 and self.board.board[r][c] == 'r') or (jump_r == self.board.height - 1 and self.board.board[r][c] == 'b'):
                        new_board[jump_r][jump_c] = new_board[jump_r][jump_c].upper()
                    moves.append(Board(new_board))
                    subsequent_jumps = self.get_moves_for_piece(jump_r, jump_c, dr, dc)
                    for sj in subsequent_jumps:
                        moves.append(sj)
        return moves

    def apply_move(self, move: Board) -> 'State':
        new_board = move
        # move.display()
        # print("current depth", self.depth)
        return State(new_board, get_next_turn(self.turn), self.depth + 1)

    def get_successors(self) -> list['State']:
        successors = []
        moves = self.get_possible_moves()
        for move in moves:
            successors.append(self.apply_move(move))
        #print("get successors called, len successor = ", len(successors))
        # for s in successors:
        #     s.board.display()
        return successors

    def evaluate(self) -> int:
        eval = 0
        if self.is_terminal():
            red_pieces = sum(row.count('r') + row.count('R') for row in self.board.board)
            black_pieces = sum(row.count('b') + row.count('B') for row in self.board.board)
            if red_pieces == 0:
                return -10
            elif black_pieces == 0:
                return 10

        piece_values = {'r': 1, 'R': 3, 'b': -1, 'B': -3}
        center_control_bonus = 0.5
        mobility_bonus = 0.1
        piece_safety_bonus = 0.2
        chain_jump_bonus = 1.0
        positional_advantage_bonus = 0.5
        distance_penalty = 0.2
        numerical_advantage_bonus = 0.3

        total_red_pieces = sum(row.count('r') + row.count('R') for row in self.board.board)
        total_black_pieces = sum(row.count('b') + row.count('B') for row in self.board.board)

        for r, row in enumerate(self.board.board):
            for c, piece in enumerate(row):
                if piece in piece_values:
                    eval += piece_values[piece]
                    
                    if 2 <= r <= 5 and 2 <= c <= 5:
                        eval += center_control_bonus if piece.lower() == 'r' else -center_control_bonus
                    
                    if piece == 'r' and r <= 2:
                        eval += 1
                    elif piece == 'b' and r >= 5:
                        eval -= 1
                    
                    if r in [0, 7] or c in [0, 7]:
                        eval += piece_safety_bonus if piece.lower() == 'r' else -piece_safety_bonus

                    if piece.lower() == self.turn:
                        potential_jumps = self.get_piece_jumps(r, c)
                        if potential_jumps:
                            eval += chain_jump_bonus * len(potential_jumps) if self.turn == 'r' else -chain_jump_bonus * len(potential_jumps)

                    if piece.lower() == 'r':
                        eval += positional_advantage_bonus * (self.board.height - 1 - r)
                    elif piece.lower() == 'b':
                        eval -= positional_advantage_bonus * r

                    if total_red_pieces > total_black_pieces:
                        if piece.lower() == 'r':
                            eval += distance_penalty * (self.board.height - 1 - r)
                        elif piece.lower() == 'b':
                            eval -= distance_penalty * r
                    opponent_pieces = get_opp_char(piece.lower())
                    for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.board.height and 0 <= nc < self.board.width:
                            if self.board.board[nr][nc] in opponent_pieces:
                                eval += numerical_advantage_bonus if piece.lower() == 'r' else -numerical_advantage_bonus

        return eval

    # def evaluate(self) -> int:
    #     """
    #     Evaluate the utility of the current state for the current player.
        
    #     Returns:
    #         int: The evaluation score of the current state.
    #     """
    #     eval = 0
    #     if self.is_terminal():
    #         red_pieces = sum(row.count('r') + row.count('R') for row in self.board.board)
    #         black_pieces = sum(row.count('b') + row.count('B') for row in self.board.board)
    #         #print(self.board.display())
    #         #print(f"state is terminal, red pieces = {red_pieces}, blue peices = {black_pieces}")
    #         if red_pieces == 0:
    #             return -10
    #         elif black_pieces == 0:
    #             return 10
            
    #     for row in self.board.board:
    #         for piece in row:
    #             if piece == 'r':
    #                 eval += 1
    #             elif piece == 'R':
    #                 eval += 2
    #             elif piece == 'b':
    #                 eval -= 1
    #             elif piece == 'B':
    #                 eval -= 2
    #     return eval




    def is_terminal(self) -> bool:
        red_pieces = sum(row.count('r') + row.count('R') for row in self.board.board)
        black_pieces = sum(row.count('b') + row.count('B') for row in self.board.board)
        # if red_pieces == 0 or black_pieces == 0:
        #     print("board terminated + red pieces: ", red_pieces, " black pieces: ", black_pieces)
        return red_pieces == 0 or black_pieces == 0

def get_opp_char(player: str) -> list[str]:
    if player in ['b', 'B']:
        return ['r', 'R']
    else:
        return ['b', 'B']

def get_next_turn(curr_turn: str) -> str:
    return 'b' if curr_turn == 'r' else 'r'

def read_from_file(filename: str) -> Board:
    """
    Read the initial board state from a file.
    
    Parameters:
        filename (str): The name of the file to read from.
    
    Returns:
        Board: The 8x8 board read from the file.
    """
    with open(filename) as f:
        lines = f.readlines()
    board = [[str(x) for x in l.rstrip()] for l in lines]
    return Board(board)



def alpha_beta_search(state: State, depth: int) -> Board:
    #print("alpha_beta called on ", state.turn)
    if state.turn == 'r':
        value, best_move = max_value(state, -10000, 10000, 0)
    else:
        value, best_move = min_value(state, -10000, 10000, 0)
    return best_move

def max_value(state: State, alpha: float, beta: float, depth: int) -> tuple[int, Board]:
    if state.is_terminal() or state.depth >= depth_limit:
        return state.evaluate(), state.board
    value = -10000
    best_move = None
    for successor in state.get_successors():
        #print("max value successors = ", len(state.get_successors()))
        successor_value, _ = min_value(successor, alpha, beta, depth + 1)
        if successor_value > value:
            value = successor_value
            best_move = successor.board
        if value >= beta:
            return value, best_move
        alpha = max(alpha, value)
    if best_move == None:
        print(f"Min: best move is none and state.get_successors is: {state.get_successors()[0].board.display()}")
    return value, best_move

def min_value(state: State, alpha: float, beta: float, depth: int) -> tuple[int, Board]:
    if state.is_terminal() or depth >= depth_limit:
        return state.evaluate(), state.board
    value = 10000
    best_move = None
    for successor in state.get_successors():
        #print("min value successors = ", len(state.get_successors()))
        successor_value, _ = max_value(successor, alpha, beta, depth + 1)
        if successor_value < value:
            value = successor_value
            best_move = successor.board
        if value <= alpha:
            return value, best_move
        beta = min(beta, value)
    if best_move == None:
        print("Min: best move is none")
    return value, best_move

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzles."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    args = parser.parse_args()
    initial_board = read_from_file(args.inputfile)
    state = State(initial_board)
    # state.turn = 'r'
    with open(args.outputfile, 'w') as f:
        for row in initial_board.board:
            f.write(''.join(row) + '\n')
        f.write('\n')
        while not state.is_terminal():
            next_board = alpha_beta_search(state, depth_limit)
            # red_pieces = sum(row.count('r') + row.count('R') for row in state.board.board)
            # black_pieces = sum(row.count('b') + row.count('B') for row in state.board.board)
            # if red_pieces == 0 or black_pieces == 0:
            #next_board.display()
            # time.sleep(3)
            # print("board terminated + red pieces: ", red_pieces, " black pieces: ", black_pieces)
            
            state = State(next_board, get_next_turn(state.turn), 0)
            #print("get next turn returns: ", get_next_turn(state.turn))
            # Write the board state to the output file
            for row in next_board.board:
                f.write(''.join(row) + '\n')
            f.write('\n')
