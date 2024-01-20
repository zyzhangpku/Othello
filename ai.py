import othello
import store
import interface

WEIGHTS = [
    [20, -3, 11, 8, 8, 11, -3, 20],
    [-3, -7, -4, 1, 1, -4, -7, -3],
    [11, -4, 2, 2, 2, 2, -4, 11],
    [8, 1, 2, -3, -3, 2, 1, 8],
    [8, 1, 2, -3, -3, 2, 1, 8],
    [11, -4, 2, 2, 2, 2, -4, 11],
    [-3, -7, -4, 1, 1, -4, -7, -3],
    [20, -3, 11, 8, 8, 11, -3, 20]
]


class OthelloAI:
    def __init__(self, board, player, difficulty=0):
        self.othello = othello.Othello()
        self.othello.board = board
        self.player = player
        self.board = self.othello.board
        self.difficulty = difficulty
        self.legal_moves = self.othello.find_legal_moves(self.player)

    def solution(self):
        self.othello.board = self.board
        if self.difficulty == -1:
            return self.weak_algorithm()
        elif self.difficulty <= 1:
            return self.greedy_algorithm()
        elif self.difficulty == 2:
            return self.basic_heuristic()

    def weak_algorithm(self):
        r_best, c_best = self.legal_moves[0]
        max_flipped = self.othello.flipped_discs(r_best, c_best, self.player)
        for r, c in self.othello.find_legal_moves(self.player):
            if self.othello.flipped_discs(r, c, self.player) < max_flipped:
                r_best, c_best = r, c
                max_flipped = self.othello.flipped_discs(r_best, c_best, self.player)
        return r_best, c_best

    def greedy_algorithm(self):
        r_best, c_best = self.legal_moves[0]
        max_flipped = self.othello.flipped_discs(r_best, c_best, self.player)
        for r, c in self.othello.find_legal_moves(self.player):
            if self.othello.flipped_discs(r, c, self.player) > max_flipped:
                r_best, c_best = r, c
                max_flipped = self.othello.flipped_discs(r_best, c_best, self.player)
        return r_best, c_best

    def compute_score(self, board):
        score = 0
        for r in range(8):
            for c in range(8):
                if board[r][c] == self.player:
                    score += WEIGHTS[r][c]
                else:
                    score -= WEIGHTS[r][c]
        return score

    def basic_heuristic(self):
        r_best, c_best = self.legal_moves[0]
        max_score = -20 * 64
        for r, c in self.othello.find_legal_moves(self.player):
            new_othello = othello.Othello()
            for rx in range(8):
                for cx in range(8):
                    new_othello.board[rx][cx] = self.othello.board[rx][cx]
            new_othello.update_board(r, c, self.player)
            now_score = self.compute_score(new_othello.board)
            if now_score > max_score:
                r_best, c_best = r, c
                max_score = now_score
        return r_best, c_best

    def invoke_ai(self):
        board_storer = store.BoardStorer(self.othello, '')
        board_info = board_storer.get_board_info()
        return interface.response(board_info)
