import pygame, sys, random
from pygame.color import THECOLORS
from matrix2048 import Matrix


class Game:
    # def draw(self, screen):
    #    pygame.draw.rect(screen, (0, 0, 255), (200, 150, 100, 50))

    def __init__(self):
        self.screen = ''
        self.matrix = ''

    def draw_number(self, element: int, row_number: int, column_number: int):
        # TODO: repair errors
        # TODO: make comments
        """
        draw number 'element' by coords
        :param element: int
        :param row_number: int
        :param column_number: int
        :return:
        """
        font = pygame.font.SysFont('Arial', int(self.screen.get_width() / (4 * self.matrix.size)), bold=True)
        font_fg_color = BLACK
        font_bg_color = WHITE
        # render a given font into an image
        img = font.render(str(element), True,
                          pygame.Color(font_fg_color),
                          pygame.Color(font_bg_color))

        # and finally put it onto the surface.
        # the code below centres text image
        number_width = (self.screen.get_width() * (column_number * 2 + 1) / self.matrix.size - img.get_width()) / 2
        number_height = (self.screen.get_height() * (row_number * 2 + 1) / self.matrix.size - img.get_height()) / 2
        self.screen.blit(img, (number_width, number_height))
        pygame.display.update()

    def draw_numbers(self):
        """
        draw all numbers
        :return:
        """
        for row_number, row in enumerate(self.matrix.matrix):
            for column_number, element in enumerate(row):
                self.draw_number(element, row_number, column_number)

    def draw(self, screen: pygame.display, matrix: Matrix):
        """
        draw grid and call draw numbers
        :param screen:
        :param matrix:
        :return:
        """
        self.screen = screen
        self.matrix = matrix
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


class GameManager:
    def __init__(self, screen, matrix):
        self.screen = screen
        self.scene = 0
        self.button_clicked = False
        self.game = Game()
        self.startMenu = StartMenu()
        self.matrix = matrix

    def update(self):
        """
        update game screen
        :return:
        """
        if self.scene == 0:
            self.startMenu.draw(self.screen)
        if self.scene == 1:
            self.game.draw(self.screen, self.matrix)

    def process(self):
        """
        goto process of game
        :return:
        """
        if self.button_clicked:
            self.scene = 1


if __name__ == '__main__':
    BLACK = (0, 0, 0)
    WHITE = (200, 200, 200)
    WINDOW_HEIGHT = 600
    WINDOW_WIDTH = WINDOW_HEIGHT
    quantity_of_squares = 4
    pygame.init()
    screen = pygame.display.set_mode([WINDOW_WIDTH, WINDOW_HEIGHT])
    screen.fill([255, 255, 255])

    gamematrix = Matrix(quantity_of_squares)
    manager = GameManager(screen, gamematrix)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:  # detect pressed key
                if event.key == pygame.K_LEFT:
                    direction = 'left'
                    manager.button_clicked = True
                elif event.key == pygame.K_RIGHT:
                    direction = 'right'
                    manager.button_clicked = True
                elif event.key == pygame.K_UP:
                    direction = 'up'
                    manager.button_clicked = True
                elif event.key == pygame.K_DOWN:
                    direction = 'down'
                    manager.button_clicked = True

        if manager.button_clicked:  # update display if pressed key
            manager.update()
            manager.process()
            gamematrix.move_numbers(direction=direction)
            gamematrix.add_random_pair()
            manager.button_clicked = False  # stop automatic update display
            pygame.display.flip()

    pygame.quit()
