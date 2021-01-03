import random
from copy import deepcopy


class Constants:
    SIZE = 4
    KEY_UP_ALT = "\'\\uf700\'"
    KEY_DOWN_ALT = "\'\\uf701\'"
    KEY_LEFT_ALT = "\'\\uf702\'"
    KEY_RIGHT_ALT = "\'\\uf703\'"

    KEY_UP = "'w'"
    KEY_DOWN = "'s'"
    KEY_LEFT = "'a'"
    KEY_RIGHT = "'d'"
    KEY_BACK = "'b'"

    KEY_J = "'j'"
    KEY_K = "'k'"
    KEY_L = "'l'"
    KEY_H = "'h'"


class Matrix:
    def __init__(self, size):
        self.size = size
        self.matrix = [[0 for _ in range(self.size)] for _ in range(self.size)]

    def __repr__(self):
        return str(m.matrix)

    def print_line(self, row, line):
        """

        :param row:
        :param line:
        :return:
        """
        print(line)
        for element in row:
            if element == 0:
                element = ''
            print(f'|{str(element):^6s}', end='')
        print('|')

    def print_matrix(self):
        line = '-' * 7 * len(self.matrix) + '-'
        for row in self.matrix:
            self.print_line(row, line)
        print(line)
        return ''

    def add_number(self, row, col, value):
        """

        :param row:
        :param col:
        :param value:
        :return:
        """
        row = self.matrix[row]
        row[col] = value

    def move_numbers(self, direction):
        """

        :param direction:
        :return:
        """
        result = True
        if direction == 'down':
            self.rotate_matrix()
            result = self.move_matrix()
            self.rotate_matrix(3)
        elif direction == 'up':
            self.rotate_matrix(3)
            result = self.move_matrix()
            self.rotate_matrix()
        elif direction == 'left':
            result = self.move_matrix()
        elif direction == 'right':
            self.rotate_matrix(2)
            result = self.move_matrix()
            self.rotate_matrix(2)
        else:
            pass
        return result

    def rotate_matrix(self, number=1):
        """

        :param number:
        :return:
        """
        for i in range(number):
            self.matrix = [list(i) for i in zip(*self.matrix[::-1])]

    def move_element(self, i, row):
        """

        :param i:
        :param row:
        :return:
        """
        element = row[i]
        result = False
        if (element != 0) and (i > 0):
            if element == row[i - 1]:
                row[i - 1] *= 2
                row[i] = 0
                result = True
            elif row[i - 1] == 0:
                if i - 1 > 0 and row[i - 1] == element:
                    row[i - 1] *= 2
                else:
                    row[i - 1] = element
                row[i] = 0
                result = True
            return result

    def end_detector(self):
        return True

    def move_left(self, row):
        """
        :param row:
        :return:
        """
        for i, element in enumerate(row):
            if 0 < i < self.size:
                if self.move_element(i, row):
                    self.move_left(row)

    def move_matrix(self):
        for row in self.matrix:
            self.move_left(row)

    def get_zeros(self):
        zeros = []
        for i, row in enumerate(self.matrix):
            for j, element in enumerate(row):
                if element == 0:
                    zeros.append([i, j])
        return zeros


def the_2048_game():
    running = True
    m.print_matrix()
    game_keys = {'w': 'up',
                 's': 'down',
                 'a': 'left',
                 'd': 'right',
                 ' ': 'bye'}
    while running:
        key = input()
        if key is None:
            key = 'q'
        if key in game_keys.keys():
            if key == ' ':
                running = False
                print('Bye')
            else:
                running = m.end_detector()
                m.move_numbers(game_keys[key])
                zeros = m.get_zeros()
                if not len(zeros):
                    running = False
                else:
                    pair = random.choice(zeros)
                    m.matrix[pair[0]][pair[1]] = 2
                m.print_matrix()
        else:
            continue


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    C = Constants()
    m = Matrix(C.SIZE)
    the_2048_game()
