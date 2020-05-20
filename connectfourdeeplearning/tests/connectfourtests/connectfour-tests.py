import unittest
from connectfourdeeplearning.game.connectfour import create_board

class ConnectFourTests(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def noideayet(self):
        # board = create_board()
        self.assertEqual(True, False)

if __name__ == '__main__':
    unittest.main()