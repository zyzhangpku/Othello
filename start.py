import pygame
import sys
import buttons
import game

white = 255, 255, 255
black = 0, 0, 0
red = 255, 0, 0
yellow = 255, 255, 0


class GameEngine:
    def __init__(self):
        pygame.init()
        self.screenWidth = 1000
        self.screenLength = 618
        self.gameName = 'PYTHON'
        self.title = 'Othello v1.5 -- by ZZYIMPACT' + '  ~~~  ' + self.gameName
        self.images = {'background': pygame.image.load(r'.\images\StartBackGround.jpg')}
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenLength))
        self.clock = pygame.time.Clock()
        self.clock.tick(10)
        self.x_buttons = self.screenWidth * 3 / 4 - 70
        self.y_buttons = self.screenLength / 2 - 284 - 9
        self.buttonGap = 30
        self.skipButton = buttons.Button(self.x_buttons, self.y_buttons, 'Quick Start', self.skip, h=30, w=115)
        self.quitButton = buttons.Button(self.x_buttons + 130, self.y_buttons, 'Quit Game', self.quit, h=30, w=115)
        self.d0Button = buttons.Button(445, 260, 'REALLY Easy', None, h=40, w=140)
        self.d1Button = buttons.Button(445, 360, 'Moderate?', None, h=40, w=140)
        self.d2Button = buttons.Button(445, 460, 'A Little Hard', None, h=40, w=140)
        self.difficulty = 2

    def skip(self):
        main_game = game.GameEngine(difficulty=self.difficulty)
        main_game.game_loop()

    def show_screen(self):
        pygame.display.set_caption(self.title)
        self.screen.blit(self.images['background'], (0, 0))
        # self.screen.blit(self.images['Lumine'], (-80, 310))
        # self.screen.blit(self.images['Navia'], (300, 200))
        self.show_buttons()
        self.write_text('Welcome to Othello!', self.screenWidth / 2 - 150, self.screenLength / 3 - 100, 50, yellow)
        self.write_text('Please Select Difficulty:', self.screenWidth / 2 - 108, self.screenLength / 3 - 10, 30, yellow)

    def draw_button(self, button: buttons.Button):
        pygame.draw.rect(self.screen, white, (button.x, button.y, button.w, button.h))
        self.write_text(button.text, button.x, button.y + button.h / 3)

    def write_text(self, text, x, y, size=28, color=black):
        message = pygame.font.Font(None, size)
        self.screen.blit(message.render(text, True, color), (x, y))

    def show_buttons(self):
        self.draw_button(self.skipButton)
        self.draw_button(self.quitButton)
        self.draw_button(self.d0Button)
        self.draw_button(self.d1Button)
        self.draw_button(self.d2Button)

    def winner_banner(self, if_win):
        winner_message = pygame.font.Font(None, 50)
        if if_win:
            message = 'Good! You Win!'
        else:
            message = '?You Loose??'
        textImage = winner_message.render(message, True, yellow)
        self.screen.blit(textImage, (self.screenLength / 2 + 50, 50))
        pygame.display.update()

    @staticmethod
    def quit():
        pygame.quit()
        sys.exit()

    def get_mouse_order(self, x, y):
        if self.skipButton.activate(x, y):
            self.skipButton.react()
        elif self.quitButton.activate(x, y):
            self.quitButton.react()
        else:
            if self.d0Button.activate(x, y):
                self.difficulty = 0
            elif self.d1Button.activate(x, y):
                self.difficulty = 1
            elif self.d2Button.activate(x, y):
                self.difficulty = 2
            else:
                return
        self.skip()

    def start_game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
            self.show_screen()
            if pygame.mouse.get_pressed()[0]:
                x_mouse, y_mouse = pygame.mouse.get_pos()
                self.get_mouse_order(x_mouse, y_mouse)
            pygame.display.update()


if __name__ == '__main__':
    g = GameEngine()
    g.start_game()
