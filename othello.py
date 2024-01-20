class Othello:
    def __init__(self):
        self.white = 0
        self.black = 1
        self.noPlayer = 2
        self.boardWidth = 8
        self.boardLength = 8
        self.board = [[self.noPlayer for _ in range(self.boardWidth)] for __ in range(self.boardLength)]

        self.board[3][3] = self.white
        self.board[3][4] = self.black
        self.board[4][3] = self.black
        self.board[4][4] = self.white

        self.whiteDiscNum = 2
        self.blackDiscNum = 2

        self.memory = [self.board]

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
