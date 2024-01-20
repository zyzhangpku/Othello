import othello


class BoardStorer:
    def __init__(self, othello_game: othello.Othello, file_name):
        self.othello = othello_game
        self.board = self.othello.board
        self.file_path = '.\\GameStorage\\' + file_name + '.txt'

    def get_board_info(self):
        message = ''
        for r in range(self.othello.boardLength):
            for c in range(self.othello.boardWidth):
                message += str(self.othello.board[r][c])
        return message

    def write(self):
        message = self.get_board_info()
        with open(self.file_path, 'w') as f:
            f.write(message)


class BoardReader:
    def __init__(self, othello_game: othello.Othello, file_name):
        self.othello = othello_game
        self.file_path = '.\\GameStorage\\' + file_name + '.txt'

    def read(self):
        with open(self.file_path, 'r') as f:
            message = f.readline()
        return message

    def process_str(self):
        new_game = othello.Othello()
        message = self.read()
        for x in range(len(message)):
            i = int(message[x])
            r, c = x // self.othello.boardLength, x % self.othello.boardWidth
            new_game.board[r][c] = i
        return new_game

