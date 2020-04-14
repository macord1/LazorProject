import unittest
from Lazor import Laser
import Lazor
import numpy as np
'''
LAZOR PROJECT

Molly Accord
Sreelakshmi Sunil

'''
'''
This file contains tests for some of the functions in Lazor.py
'''


class TestCases(unittest.TestCase):

    '''
    Performs Unit test on various functions in Laser class
    '''

    def test_valid_pos(self):
        '''
        Tests valid_poos function in Laser class
        '''
        # specifies x and y size of a grid_matrix
        self.size1 = 3
        self.size2 = 4
        # should return true if the positions are within 3 x 4
        self.assertTrue(Laser.valid_pos(self, 1, 2))

        self.assertFalse(Laser.valid_pos(self, 4, 4))

        self.assertFalse(Laser.valid_pos(self, -1, 2))

    def test_reflect(self):
        '''
        Tests reflect function in Laser class
        '''
        d1, d2 = Laser.reflect(self, 'right', 1, -1)
        self.assertEqual((d1, d2), (-1, -1))

        d1, d2 = Laser.reflect(self, 'left', 1, -1)
        self.assertEqual((d1, d2), (-1, -1))

        d1, d2 = Laser.reflect(self, 'up', 1, -1)
        self.assertEqual((d1, d2), (1, 1))

        d1, d2 = Laser.reflect(self, 'down', 1, -1)
        self.assertEqual((d1, d2), (1, 1))

    def test_intial_values(self):
        '''
        Tests intial_values function in Laser class
        '''

        t1, t2 = Laser.intial_values(self, 1, -1, 3, 2)
        self.assertEqual((t1, t2), (4, 1))

        t1, t2 = Laser.intial_values(self, 1, 1, 3, 2)
        self.assertEqual((t1, t2), (4, 3))

        t1, t2 = Laser.intial_values(self, -1, 1, 3, 2)
        self.assertEqual((t1, t2), (2, 3))

        t1, t2 = Laser.intial_values(self, -1, -1, 3, 2)
        self.assertEqual((t1, t2), (2, 1))

    def test_check_allhit(self):
        '''
        Tests check_allhit function in laser class
        '''

        self.grid_matrix = np.zeros((2, 7), dtype=int)
        self.grid_matrix[0][1] = 11
        self.grid_matrix[1][6] = 20
        P = [[1, 0], [6, 1]]
        self.assertFalse(Laser.check_allhit(self, P))

        self.grid_matrix[0][1] = 11
        self.grid_matrix[1][6] = 11
        self.assertTrue(Laser.check_allhit(self, P))


if __name__ == '__main__':

    unittest.main()
