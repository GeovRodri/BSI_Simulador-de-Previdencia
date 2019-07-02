import unittest
from Utils import Utils


class MyTest(unittest.TestCase):
    def test(self):
        self.assertTrue((Utils.calcular_inflacao(200, 2000) > 0))
