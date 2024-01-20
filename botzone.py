import copy
import random
import json
from copy import deepcopy


class Othello:
    def __init__(self):
        self.white = 1
        self.black = -1
        self.noPlayer = 0
        self.boardWidth = 8
        self.boardLength = 8
        self.board = [[self.noPlayer for _ in range(self.boardWidth)] for __ in range(self.boardLength)]

        self.board[3][3] = self.white
        self.board[3][4] = self.black
        self.board[4][3] = self.black
        self.board[4][4] = self.white

        self.whiteDiscNum = 2
        self.blackDiscNum = 2

    def opponent_player(self, player):
        if player == self.noPlayer:
            return self.noPlayer
        elif player == self.white:
            return self.black
        else:
            return self.white

    def is_inside_board(self, r, c):
        return 0 <= r < self.boardLength and 0 <= c < self.boardWidth

    def flipped_discs_in_dir(self, r, c, r_delta, c_delta, player):
        flipped = []
        r += r_delta
        c += c_delta
        while self.is_inside_board(r, c) and self.board[r][c] != self.noPlayer:
            if self.board[r][c] == self.opponent_player(player):
                flipped.append((r, c))
                r += r_delta
                c += c_delta
            else:
                return flipped
        return []

    def flipped_discs(self, r, c, player):
        flipped = []
        for r_delta in range(-1, 2):
            for c_delta in range(-1, 2):
                if r_delta == 0 and c_delta == 0:
                    continue
                flipped += self.flipped_discs_in_dir(r, c, r_delta, c_delta, player)
        return flipped

    def is_legal_move(self, r, c, player):
        if self.board[r][c] != self.noPlayer:
            return False
        return len(self.flipped_discs(r, c, player)) > 0

    def find_legal_moves(self, player):
        legal_moves = []
        for r in range(self.boardLength):
            for c in range(self.boardWidth):
                if self.is_legal_move(r, c, player):
                    legal_moves.append((r, c))
        return legal_moves

    def update_board(self, r, c, player):
        if r == -1:
            return
        self.board[r][c] = player
        for r, c in self.flipped_discs(r, c, player):
            self.board[r][c] = player

    def update_nums(self):
        self.whiteDiscNum, self.blackDiscNum = 0, 0
        for r in range(self.boardLength):
            for c in range(self.boardWidth):
                player = self.board[r][c]
                if player == self.white:
                    self.whiteDiscNum += 1
                elif player == self.black:
                    self.blackDiscNum += 1

    def winner(self):
        n_white, n_black = 0, 0
        for r in range(self.boardLength):
            for c in range(self.boardWidth):
                player = self.board[r][c]
                if player == self.white:
                    n_white += 1
                elif player == self.black:
                    n_black += 1
        if n_white > n_black:
            return self.white
        elif n_white < n_black:
            return self.black
        else:
            return self.noPlayer


weight = [
    [20, -3, 11, 8, 8, 11, -3, 20],
    [-3, -7, -4, 1, 1, -4, -7, -3],
    [11, -4, 2, 2, 2, 2, -4, 11],
    [8, 1, 2, -3, -3, 2, 1, 8],
    [8, 1, 2, -3, -3, 2, 1, 8],
    [11, -4, 2, 2, 2, 2, -4, 11],
    [-3, -7, -4, 1, 1, -4, -7, -3],
    [20, -3, 11, 8, 8, 11, -3, 20]
]
minScore = -20 * 64


class OthelloAI:
    def __init__(self, board, player, difficulty=2):
        self.othello = Othello()
        self.othello.board = board
        self.player = player
        self.board = self.othello.board
        self.difficulty = difficulty
        self.legal_moves = self.othello.find_legal_moves(self.player)

    def solution(self):
        self.othello.board = self.board
        if not self.legal_moves:
            return -1, -1
        if self.difficulty == 0:
            return self.random_algorithm()
        elif self.difficulty == 1:
            return self.greedy_algorithm()
        elif self.difficulty == 2:
            return self.basic_heuristic()
        elif self.difficulty == 3:
            return self.minimax(max_depth=1)

    def random_algorithm(self):
        return random.choice(self.legal_moves)

    def greedy_algorithm(self):
        r_best, c_best = self.legal_moves[0]
        max_flipped = self.othello.flipped_discs(r_best, c_best, self.player)
        for r, c in self.othello.find_legal_moves(self.player):
            if self.othello.flipped_discs(r, c, self.player) > max_flipped:
                r_best, c_best = r, c
                max_flipped = self.othello.flipped_discs(r_best, c_best, self.player)
        return r_best, c_best

    def compute_score(self, measure_board):
        score = 0
        for r in range(8):
            for c in range(8):
                if measure_board[r][c] == self.player:
                    score += weight[r][c]
                elif measure_board[r][c] == self.othello.opponent_player(self.player):
                    score -= weight[r][c]
        return score

    def basic_heuristic(self):
        r_best, c_best = self.legal_moves[0]
        max_score = minScore
        for r, c in self.legal_moves:
            new_othello = Othello()
            new_othello.board = copy.deepcopy(self.othello.board)
            new_othello.update_board(r, c, self.player)
            now_score = self.compute_score(new_othello.board)
            if now_score > max_score:
                r_best, c_best = r, c
                max_score = now_score
        return r_best, c_best

    def compute_move_score(self, r, c, board, depth, max_depth):
        new_othello = Othello()
        new_othello.board = copy.deepcopy(board)
        new_othello.update_board(r, c, self.player)
        opponent = OthelloAI(new_othello.board, self.othello.opponent_player(self.player))
        nr, nc = opponent.basic_heuristic()
        new_othello.update_board(nr, nc, opponent.player)
        if depth == max_depth:
            return self.compute_score(new_othello.board)
        max_score = minScore
        for rx, cx in new_othello.find_legal_moves(self.player):
            score = self.compute_move_score(rx, cx, new_othello.board, depth+1, max_depth)
            if score > max_score:
                max_score = score
        return max_score

    def minimax(self, max_depth):
        # n = len(self.legal_moves)
        r_best, c_best = self.legal_moves[0]
        max_score = minScore
        for r, c in self.legal_moves:
            score = self.compute_move_score(r, c, self.board, 1, max_depth)
            if score > max_score:
                r_best, c_best = r, c
                max_score = score
        return r_best, c_best


def initBoard():
    fullInput = json.loads(input())
    requests = fullInput["requests"]
    responses = fullInput["responses"]
    othello = Othello()
    my_color = -1
    if requests[0]["x"] >= 0:
        my_color = 1
        othello.update_board(requests[0]["x"], requests[0]["y"], -my_color)
    turn = len(responses)
    for i in range(turn):
        othello.update_board(responses[i]["x"], responses[i]["y"], my_color)
        othello.update_board(requests[i + 1]["x"], requests[i + 1]["y"], -my_color)
    return othello.board, my_color


board, color = initBoard()
ai = OthelloAI(board, color, difficulty=3)
x, y = ai.solution()
print(json.dumps({"response": {"x": x, "y": y}}))
