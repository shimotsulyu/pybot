import unittest
from pybot.code.pybot import Actions
class Testpybot(unittest.TestCase):
    def test_checkNotOverlapping_false(self):
        self.assertFalse(Actions().checkNotOverlapping([308, 400, 180, 152], [306, 401, 180, 152]), "Should be False")

    def test_checkNotOverlapping_true(self):
        self.assertTrue(Actions().checkNotOverlapping([308, 400, 180, 152], [534, 399, 180, 152]), "Should be True")

if __name__ == '__main__':
    unittest.main()