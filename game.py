import time
import pygame
import sys
import othello
import ai
import buttons
import store

white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
yellow = 255, 255, 0


class GameEngine:
    def __init__(self, difficulty=2):
        pygame.init()
        self.screenWidth = 1000
        self.screenLength = 618
        self.gameName = 'PYTHON'
        self.title = 'Othello v1.5 -- by ZZYIMPACT' + '  ~~~  ' + self.gameName
        self.images = {'board': pygame.image.load(r'.\images\board.bmp'),
                       'black': pygame.image.load(r'.\images\black.bmp'),
                       'white': pygame.image.load(r'.\images\white.bmp'),
                       'background': pygame.image.load(r'.\images\WoodTexture.png')
                       }
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenLength))
        self.boardWidth = 440
        self.y_board = (self.screenLength - self.boardWidth) / 2
        self.x_board = self.y_board
        self.clock = pygame.time.Clock()
        self.clock.tick(10)
        self.discSize = 50
        self.edgeSize = 20
        self.othello = othello.Othello()
        self.userPlayer = self.othello.black
        self.AIPlayer = self.othello.opponent_player(self.userPlayer)
        self.currentPlayer = self.userPlayer
        self.winner = self.othello.noPlayer
        self.difficulty = difficulty
        self.AI = ai.OthelloAI(self.othello.board, self.AIPlayer, difficulty=self.difficulty)
        self.x_buttons = self.screenWidth * 3 / 4 - 70 + 15
        self.y_buttons = self.screenLength / 2 - 85 - 20
        self.restartButton = buttons.Button(self.x_buttons, self.y_buttons, 'Restart Game', self.restart)
        self.saveButton = buttons.Button(self.x_buttons, self.y_buttons + 80, 'Save Game', self.save)
        self.readButton = buttons.Button(self.x_buttons, self.y_buttons + 160, 'Read Game', self.read)
        self.quitButton = buttons.Button(self.x_buttons, self.y_buttons + 240, 'Quit Game', self.quit)
        self.withdrawButton = buttons.Button(self.x_buttons, self.y_buttons + 320, 'Withdraw', None)

    def show_screen(self):
        pygame.display.set_caption(self.title)
        self.screen.blit(self.images['background'], (0, 0))
        self.screen.blit(self.images['board'], (self.x_board, self.y_board))
        self.show_buttons()

    def draw_button(self, button: buttons.Button):
        pygame.draw.rect(self.screen, white, (button.x, button.y, button.w, button.h))
        self.write_text_on_button(button.text, button.x, button.y + button.h / 3)

    def write_text_on_button(self, text, x, y):
        message = pygame.font.Font(None, 30)
        self.screen.blit(message.render(text, True, black), (x, y))

    def show_buttons(self):
        self.draw_button(self.restartButton)
        self.draw_button(self.saveButton)
        self.draw_button(self.readButton)
        self.draw_button(self.quitButton)
        # self.draw_button(self.withdrawButton)

    def get_disc_loc_on_screen(self, r, c):
        return self.x_board + self.edgeSize + c * self.discSize, \
               self.y_board + self.edgeSize + r * self.discSize

    def get_disc_loc_on_board(self, x, y):
        x -= self.x_board + self.edgeSize
        y -= self.y_board + self.edgeSize
        x //= self.discSize
        y //= self.discSize
        if not self.othello.is_inside_board(y, x):
            return -1, -1
        return round(y), round(x)

    def show_flip_disc(self, r, c):
        player = self.othello.board[r][c]
        self.spawn_disc(r, c, self.othello.opponent_player(player))

    def flip_disc(self, r, c, player):
        flipped = self.othello.flipped_discs(r, c, player)
        for x, y in flipped:
            self.show_flip_disc(x, y)

    def draw_disc(self, r, c, player):
        if player == self.othello.white:
            image = self.images['white']
        else:
            image = self.images['black']
        self.screen.blit(image, self.get_disc_loc_on_screen(r, c))

    def show_legal_moves(self, r, c):
        n_moves = len(self.othello.flipped_discs(r, c, self.userPlayer))
        message = pygame.font.Font(None, 50)
        textImage = message.render(str(n_moves), True, white)
        x, y = self.get_disc_loc_on_screen(r, c)
        x += self.discSize * 0.3
        y += self.discSize / 5
        self.screen.blit(textImage, (x, y))

    def show_all_legal_moves(self):
        for r in range(self.othello.boardLength):
            for c in range(self.othello.boardWidth):
                if self.othello.is_legal_move(r, c, self.userPlayer):
                    self.show_legal_moves(r, c)
        # pygame.display.update()

    def update_board(self):
        for r in range(self.othello.boardLength):
            for c in range(self.othello.boardWidth):
                now_player = self.othello.board[r][c]
                if now_player != self.othello.noPlayer:
                    self.draw_disc(r, c, now_player)

    def switch_player(self):
        self.currentPlayer = self.othello.opponent_player(self.currentPlayer)

    def update_AI(self):
        self.AI.board = self.othello.board

    def spawn_disc(self, r, c, player):
        # self.othello.memory.append(self.othello.board)
        self.othello.board[r][c] = player

    def winner_banner(self, if_win):
        winner_message = pygame.font.Font(None, 50)
        if if_win == self.userPlayer:
            message = 'Good! You Win!'
        elif if_win == self.othello.noPlayer:
            message = 'It is a Tie!'
        else:
            message = 'You Loose~~~'
        textImage = winner_message.render(message, True, yellow)
        self.screen.blit(textImage, (self.screenLength / 2 + 50, 50))
        pygame.display.update()

    def game_end(self):
        winner = self.othello.winner()
        if winner == self.userPlayer:
            self.winner = self.userPlayer
        elif winner == self.AIPlayer:
            self.winner = self.AIPlayer
        self.winner_banner(winner)
        if pygame.mouse.get_pressed()[0]:
            x_mouse, y_mouse = pygame.mouse.get_pos()
            self.get_mouse_order(x_mouse, y_mouse, [])

    def test_board(self):
        for r in range(8):
            for c in range(8):
                self.spawn_disc(r, c, 1)

    def show_score(self):
        x_scores = 650
        y_user_score = 100 - 30
        y_AI_score = 180 - 30
        self.othello.update_nums()
        message_user = pygame.font.Font(None, 50)
        message_AI = pygame.font.Font(None, 50)

        if self.userPlayer == self.othello.black:
            num_user, num_AI = self.othello.blackDiscNum, self.othello.whiteDiscNum
            color_user, color_AI = black, white
        else:
            num_AI, num_user = self.othello.blackDiscNum, self.othello.whiteDiscNum
            color_AI, color_user = black, white
        self.screen.blit(message_user.render(f'Your Score: {num_user}', True, color_user),
                         (x_scores, y_user_score))
        self.screen.blit(message_AI.render(f'AI\'s Score: {num_AI}', True, color_AI), (x_scores, y_AI_score))

    def restart(self):
        self.othello = othello.Othello()

    def save(self):
        saver = store.BoardStorer(self.othello, self.gameName)
        saver.write()

    def read(self):
        reader = store.BoardReader(self.othello, self.gameName)
        self.othello = reader.process_str()
        self.update_board()

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()

    def put_disc(self, x, y, legal_moves):
        r, c = self.get_disc_loc_on_board(x, y)
        if (r, c) in legal_moves:
            self.othello.memory.append(self.othello.board)
            self.spawn_disc(r, c, self.userPlayer)
            self.flip_disc(r, c, self.userPlayer)
            self.switch_player()
        else:
            message = pygame.font.Font(None, 50)
            textImage = message.render('X', True, red)
            x, y = self.get_disc_loc_on_screen(r, c)
            x += self.discSize * 0.3
            y += self.discSize / 5
            self.screen.blit(textImage, (x, y))

    def get_mouse_order(self, x, y, legal_moves):
        if self.x_board + self.edgeSize <= x <= self.boardWidth + self.x_board + self.edgeSize and \
                self.y_board + self.edgeSize <= y <= self.boardWidth + self.y_board + self.edgeSize:
            self.put_disc(x, y, legal_moves)
        elif self.restartButton.activate(x, y):
            self.restartButton.react()
        elif self.saveButton.activate(x, y):
            self.saveButton.react()
        elif self.readButton.activate(x, y):
            self.readButton.react()
        elif self.quitButton.activate(x, y):
            self.quitButton.react()
        elif self.withdrawButton.activate(x, y):
            self.withdrawButton.react()
        else:
            return

    def game_loop(self):
        # self.test_board()
        pygame.mixer.music.load(r'.\bgm\bgm.ogg')
        pygame.mixer.music.play(-1)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
            self.show_screen()
            self.update_board()
            self.show_score()
            legal_moves = self.othello.find_legal_moves(self.currentPlayer)
            opp_legal_moves = self.othello.find_legal_moves(self.othello.opponent_player(self.currentPlayer))
            if len(legal_moves) == 0 and len(opp_legal_moves) == 0:
                self.game_end()
            self.update_AI()
            if self.currentPlayer == self.userPlayer:
                if len(legal_moves) == 0:
                    self.switch_player()
                    continue
                self.show_all_legal_moves()
                if pygame.mouse.get_pressed()[0]:
                    x_mouse, y_mouse = pygame.mouse.get_pos()
                    self.get_mouse_order(x_mouse, y_mouse, legal_moves)
            else:
                if len(legal_moves) == 0:
                    self.switch_player()
                    continue
                r, c = self.AI.solution()
                time.sleep(0.25)
                self.spawn_disc(r, c, self.AIPlayer)
                self.flip_disc(r, c, self.AIPlayer)
                self.switch_player()

            self.update_board()
            pygame.display.update()


if __name__ == '__main__':
    g = GameEngine()
    g.game_loop()
