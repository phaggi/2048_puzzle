import pygame, sys, random
from pygame.color import THECOLORS
from matrix2048 import Matrix


class Game:
    # def draw(self, screen):
    #    pygame.draw.rect(screen, (0, 0, 255), (200, 150, 100, 50))

    def __init__(self, screen, matrix):
        self.screen = screen
        self.matrix = matrix
        self.element = 0

    def make_img(self):
        # render a given font into an image
        font_fg_color = BLACK
        font_bg_color = WHITE
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
        self.screen.fill(WHITE)
        block_size = WINDOW_WIDTH / self.matrix.size  # Set the size of the grid block
        for x in range(WINDOW_WIDTH):
            for y in range(WINDOW_HEIGHT):
                rect = pygame.Rect(x * block_size, y * block_size,
                                   block_size, block_size)
                pygame.draw.rect(screen, WHITE, rect, 1)
        self.draw_numbers()


class StartMenu:
    def draw(self, screen):
        """
        TODO: make startmenu in future
        :param screen:
        :return:
        """
        pass


class Final:
    def draw(self, screen, game):
        screen.fill(WHITE)
        game.draw_number(1, 1)


class GameManager:
    def __init__(self, screen, matrix):
        self.screen = screen
        self.matrix = matrix
        self.scene = 0
        self.button_clicked = False
        self.game = Game(screen=self.screen, matrix=self.matrix)
        self.startMenu = StartMenu()
        self.final = Final()

    def update(self):
        """
        update game screen
        :return:
        """
        if self.scene == 0:
            self.startMenu.draw(self.screen)
        if self.scene == 1:
            self.game.draw(self.screen, self.matrix)
        if self.scene == 2:
            self.final.draw(self.screen, self.game)

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


if __name__ == '__main__':
    test = False
    testfinal = False
    BLACK = (0, 0, 0)
    WHITE = (200, 200, 200)
    WINDOW_HEIGHT = 400
    WINDOW_WIDTH = WINDOW_HEIGHT
    quantity_of_squares = 5
    dict_of_keys = {80: 'left',
                    79: 'right',
                    82: 'up',
                    81: 'down'
                    }
    pygame.init()
    screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
    screen.fill([255, 255, 255])

    gamematrix = Matrix(quantity_of_squares)
    manager = GameManager(screen, gamematrix)

    running = True
    direction = ''
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:  # detect pressed key
                scancode = event.scancode
                if scancode in dict_of_keys.keys():
                    direction, manager.button_clicked = get_pressed_key(scancode=scancode, event=event)
        if manager.button_clicked:  # update display if pressed key
            gamematrix.move_numbers(direction=direction)
            gamematrix.add_random_pair()
            if testfinal: gamematrix.add_number(0, 0, 2048)
            if test: gamematrix.print_matrix()
            manager.update()
            manager.process()
            manager.button_clicked = False  # stop automatic update display
        pygame.display.flip()

    pygame.quit()
