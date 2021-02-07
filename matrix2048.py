import random
import unittest
from unittest.mock import patch


from copy import deepcopy


class Constants:
    SIZE = 5
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
    def __init__(self, size=None):
        """
        covered unittest
        :param size:
        """
        if size:
            self.size = size
        else:
            self.size = 4
        self.matrix = [[0 for _ in range(self.size)] for _ in range(self.size)]

    def __repr__(self):
        return str(self.matrix)

    def add_random_pair(self):
        pair = random.choice(self.get_zeros())
        self.matrix[pair[0]][pair[1]] = 2

    def print_line(self, row, line):
        """
        covered unittest
        :param row:
        :param line:
        :return:
        """

        result = line + '\n'
        for element in row:
            if element == 0:
                element = ''
            result += f'|{str(element):^6s}'
        result += '|'
        print(result)

    def make_line(self):
        return '-' * 7 * len(self.matrix) + '-'

    def print_matrix(self):
        """
        covered unittest
        TODO: need to refactor - strings > result, print(result), and refactor unittest
        :return:
        """
        line = self.make_line()
        for row in self.matrix:
            self.print_line(row, line)
        print(line)
        return ''

    def add_number(self, row_num, col_num, value):
        """
        covered unittest
        :param row_num:
        :param col_num:
        :param value:
        :return:
        """
        row = self.matrix[row_num]
        row[col_num] = value

    def move_numbers(self, direction):
        """

        :param direction:
        :return:
        """
        result = True
        if direction == 'down':
            self.rotate_matrix()
            self.move_matrix()
            self.rotate_matrix(3)
        elif direction == 'up':
            self.rotate_matrix(3)
            self.move_matrix()
            self.rotate_matrix()
        elif direction == 'left':
            self.move_matrix()
        elif direction == 'right':
            self.rotate_matrix(2)
            self.move_matrix()
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
        result = False
        for row in self.matrix:
            if 2048 in row:
                result = True
        return result

    def move_left(self, row):
        """
        covered unittest
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
        """
        covered unittest

        :return:
        """
        zeros = []
        for i, row in enumerate(self.matrix):
            for j, element in enumerate(row):
                if element == 0:
                    zeros.append([i, j])
        return zeros


def the_2048_game():
    constants = Constants()
    m = Matrix(constants.SIZE)
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
                m.move_numbers(game_keys[key])
                zeros = m.get_zeros()
                if not len(zeros):
                    running = False
                else:
                    m.add_random_pair()
                    if testfinal: m.add_number(0, 0, 2048)
                m.print_matrix()
                if m.end_detector():
                    running = False
                    print('You win!')
        else:
            continue


class TestStringMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.matrix = Matrix()

    def test_init_matrix(self):
        result = str([[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]])
        self.matrix = Matrix()
        self.assertEqual(str(Matrix()), result)
        self.assertEqual(str(self.matrix), str(Matrix(4)))
        self.assertEqual(self.matrix.size, 4)
        self.assertEqual(Matrix(5).size, 5)

    def test_get_zeros(self):
        result = str([[0, 0], [0, 1], [0, 2], [0, 3], [1, 0], [1, 1], [1, 2], [1, 3],
                      [2, 0], [2, 1], [2, 2], [2, 3], [3, 0], [3, 1], [3, 2], [3, 3]]
                     )
        self.matrix = Matrix()
        self.assertEqual(str(self.matrix.get_zeros()), result)

    @patch('builtins.print')
    def test_print_matrix(self, mock_print):
        result = '''-----------------------------'''
        self.matrix = Matrix()
        self.matrix.print_matrix()
        mock_print.assert_called_with(result)

    @patch('builtins.print')
    def test_print_line(self, mock_print):
        line = '''-----------------------------'''
        result = '''-----------------------------\n|  2   |      |      |      |'''
        self.matrix = Matrix()
        self.matrix.add_number(0, 0, 2)
        self.matrix.print_line(self.matrix.matrix[0], line)
        mock_print.assert_called_with(result)

    def test_add_number(self):
        result1 = [[2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        result2 = [[2, 0, 0, 0], [0, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.matrix = Matrix()
        self.matrix.add_number(0, 0, 2)
        self.assertEqual(self.matrix.matrix, result1)
        self.matrix.add_number(1, 1, 2)
        self.assertEqual(self.matrix.matrix, result2)

    def test_move_left(self):
        result1 = [[0, 0, 0, 0], [0, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        result2 = [[0, 0, 0, 0], [2, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        result3 = [[0, 0, 0, 0], [2, 2, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        result4 = [[0, 0, 0, 0], [4, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.matrix = Matrix()
        self.matrix.add_number(1, 1, 2)
        self.assertEqual(self.matrix.matrix, result1)
        self.matrix.move_left(row=self.matrix.matrix[1])
        self.assertEqual(self.matrix.matrix, result2)
        self.matrix.add_number(1, 1, 2)
        self.assertEqual(self.matrix.matrix, result3)
        self.matrix.move_left(row=self.matrix.matrix[1])
        self.assertEqual(self.matrix.matrix, result4)
    '''
    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # Проверим, что s.split не работает, если разделитель - не строка
        with self.assertRaises(TypeError):
            s.split(2)'''



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    utest = True
    #utest = False
    if utest:
        unittest.main()

    testfinal = False
    #the_2048_game()
    matrix = Matrix(5)
    matrix.print_matrix()
