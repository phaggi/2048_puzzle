import pygame, sys, random
from pygame.color import THECOLORS
from matrix2048 import Matrix, Constants


class Game:
    # def draw(self, screen):
    #    pygame.draw.rect(screen, (0, 0, 255), (200, 150, 100, 50))

    def __init__(self, screen, matrix, constants):
        self.screen = screen
        self.matrix = matrix
        self.element = 0
        self.WHITE, self.BLACK, self.WINDOW_WIDTH, self.WINDOW_HEIGHT = constants

    def make_img(self):
        # render a given font into an image
        font_fg_color = self.BLACK
        font_bg_color = self.WHITE
        font = pygame.font.SysFont('Arial', int(self.screen.get_width() / (4 * self.matrix.size)), bold=True)
        return font.render(str(self.element), True,
                           pygame.Color(font_fg_color),
                           pygame.Color(font_bg_color))

    def check_element(self):
        if self.element == 0:
            self.element = ' '
        elif self.element == 2048:
            self.element = 'You win!'

    def draw_number(self, row_number: int, column_number: int):
        # TODO: repair errors
        # TODO: make comments
        """
        draw number 'element' by coords
        :param row_number: int
        :param column_number: int
        :return:
        """

        # and finally put it onto the surface.
        # the code below centres text image
        self.check_element()
        img = self.make_img()
        number_width = (self.screen.get_width() * (column_number * 2 + 1) / self.matrix.size - img.get_width()) / 2
        number_height = (self.screen.get_height() * (row_number * 2 + 1) / self.matrix.size - img.get_height()) / 2
        self.screen.blit(img, (number_width, number_height))
        pygame.display.flip()

    def draw_numbers(self):
        """
        draw all numbers
        :return:
        """
        for row_number, row in enumerate(self.matrix.matrix):
            for column_number, self.element in enumerate(row):
                self.draw_number(row_number, column_number)

    def draw(self, screen: pygame.display, matrix: Matrix):
        """
        draw grid and call draw numbers
        :param screen:
        :param matrix:
        :return:
        """
        self.screen = screen
        self.matrix = matrix

        self.screen.fill(self.WHITE)
        block_size = self.WINDOW_WIDTH / self.matrix.size  # Set the size of the grid block
        for x in range(self.WINDOW_WIDTH):
            for y in range(self.WINDOW_HEIGHT):
                rect = pygame.Rect(x * block_size, y * block_size,
                                   block_size, block_size)
                pygame.draw.rect(self.screen, self.WHITE, rect, 1)
        self.draw_numbers()


class StartMenu:
    def __init__(self, screen, constants):
        self.screen = screen
        self.WHITE = constants[0]

    def draw(self):
        """
        TODO: make startmenu in future
        """
        pass


class Final:
    def __init__(self, screen, game, constants):
        self.screen = screen
        self.game = game
        self.WHITE = constants[0]

    def draw(self, ):
        self.screen.fill(self.WHITE)
        self.game.draw_number(1, 1)


class GameManager:
    def __init__(self, screen, matrix, constants):
        self.screen = screen
        self.matrix = matrix
        self.scene = 0
        self.button_clicked = False
        self.game = Game(screen=self.screen, matrix=self.matrix, constants=constants)
        self.startMenu = StartMenu(screen=self.screen, constants=constants)
        self.final = Final(screen=self.screen, game=self.game, constants=constants)

    def update(self):
        """
        update game screen
        :return:
        """

        if self.scene == 0:
            self.startMenu.draw()
        if self.scene == 1:
            self.game.draw(self.screen, self.matrix)
        if self.scene == 2:
            self.final.draw()

    def process(self):
        """
        goto process of game
        :return:
        """
        if self.matrix.end_detector():
            self.scene = 2
        elif self.button_clicked:
            self.scene = 1


def get_pressed_key(scancode, event):
    """

    :param event:
    :return: str direction
    """
    return dict_of_keys.get(scancode, None), True


class GameProcess:
    def __init__(self):
        self.test = False
        self.testfinal = True
        self.BLACK = Constants.BLACK
        self.WHITE = Constants.WHITE
        self.WINDOW_HEIGHT = self.WINDOW_WIDTH = Constants.WINDOW_HEIGHT
        self.constants = (self.WHITE, self.BLACK, self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.quantity_of_squares = Constants.SIZE
        self.dict_of_keys = {80: 'left',
                             79: 'right',
                             82: 'up',
                             81: 'down'
                             }
        self.pygame = pygame
        self.pygame.init()
        self.screen = self.pygame.display.set_mode([self.WINDOW_WIDTH, self.WINDOW_HEIGHT])
        self.screen.fill([255, 255, 255])
        self.gamematrix = Matrix(self.quantity_of_squares)
        self.manager = GameManager(screen=self.screen, matrix=self.gamematrix, constants=self.constants)
        self.direction = None
        self.running = None

    def get_pressed_key(self, scancode, event):
        """

        :param scancode:
        :param event:
        :return: str direction
        """
        return self.dict_of_keys.get(scancode, None), True

    def start_game(self):
        self.running = True
        self.direction = ''
        while self.running:
            for event in self.pygame.event.get():
                if event.type == self.pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:  # detect pressed key
                    scancode = event.scancode
                    if scancode in self.dict_of_keys.keys():
                        self.direction, self.manager.button_clicked = self.get_pressed_key(scancode=scancode,
                                                                                           event=event)
            if self.manager.button_clicked:  # update display if pressed key
                self.gamematrix.move_numbers(direction=self.direction)
                self.gamematrix.add_random_pair()
                if self.testfinal: self.gamematrix.add_number(0, 0, 2048)
                if self.test: self.gamematrix.print_matrix()
                self.manager.update()
                self.manager.process()
                self.manager.button_clicked = False  # stop automatic update display
            self.pygame.display.flip()
        self.end_game()

    def end_game(self):
        self.pygame.quit()


if __name__ == '__main__':
    my_game = GameProcess()
    my_game.start_game()
