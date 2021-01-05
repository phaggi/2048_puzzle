import sys

import pygame.locals as pygl
import pygame.time as pytime
import pygame.event as pyevent
import pygame


class MyGame:

    def __init__(self):
        self.clock = pytime.Clock()
        pygame.init()
        self.SIZE = (640, 400)
        self.BG_COLOUR = (0, 0, 0)
        self.LINE_COLOUR = (255, 255, 255)

        self.screen = pygame.display.set_mode(self.SIZE)
        self.clock = pygame.time.Clock()

    def get_event(self):
        while True:
            self.clock.tick(30)
            event = pyevent.wait()
            if event.type not in self.dispatch().keys():
                pass
            else:
                return event

    def run(self):
        while True:
            event = self.get_event()
            print(self.dispatch().get(event.type)(event.type))

    def dispatch(self):
        result = {pygl.QUIT: self.quit_game,  # whatever else
                  pygl.KEYDOWN: 'key_pressed'}
        return result

    def quit_game(self, key=None):
        if key == pygl.QUIT:
            pygame.quit()
            sys.exit()

    def draw_screen(self):
        self.screen.fill(self.BG_COLOUR)
        pygame.draw.aaline(self.screen, self.LINE_COLOUR, (1, 1), (639, 399))
        pygame.display.flip()


if __name__ == '__main__':
    game = MyGame()
    game.run()
