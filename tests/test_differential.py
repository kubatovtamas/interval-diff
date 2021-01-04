import unittest
from differential import *



class DifferentialTestCase(unittest.TestCase):
    def test_differential_init(self):
        d1 = Differential([1, 5])

        self.assertIsInstance(d1, Differential)
        self.assertEqual(d1.val, d1.interval[0])
        self.assertEqual(d1.diff, d1.interval[1])
        self.assertEqual(d1.val, 1)
        self.assertEqual(d1.diff, 5)

    def test_differential_add(self):
        d1 = Differential([2,1])
        d2 = Differential([13,1])
        c1 = Differential([3,0])
        c2 = Differential([1,0])

        self.assertTrue(d1 + c1 == Differential([5, 1]))
        self.assertTrue(c1 + d1 == Differential([5, 1]))
        self.assertTrue(c2 + d2 == Differential([14, 1]))

    def test_differential_sub(self):
        d1 = Differential([2, 1])
        d2 = Differential([13, 1])
        d3 = Differential([-5, 1])
        c1 = Differential([3, 0])
        c2 = Differential([1, 0])
        c3 = Differential([-5, 0])

        self.assertTrue(d1 - c1 == Differential([-1, 1]))
        self.assertTrue(c1 - d1 == Differential([1, -1]))
        self.assertTrue(d2 - c2 == Differential([12, 1]))
        self.assertTrue(d3 - c3 == Differential([0, 1]))

    def test_differential_mul(self):
        d1 = Differential([2, 1])
        d2 = Differential([10, 1])
        d3 = Differential([-5, 1])
        c1 = Differential([3, 0])
        c2 = Differential([12, 0])
        c3 = Differential([8, 0])

        self.assertTrue(d1 * c1 == Differential([6, 3]))
        self.assertTrue(c1 * d1 == Differential([6, 3]))
        self.assertTrue(c2 * d2 == Differential([120, 12]))
        self.assertTrue(c3 * d3 == Differential([-40, 8]))

    def test_differential_truediv(self):
        d1 = Differential([2, 1])
        d2 = Differential([10, 1])
        d3 = Differential([-5, 1])
        c1 = Differential([3, 0])
        c2 = Differential([12, 0])
        c3 = Differential([8, 0])

        self.assertTrue(d1 / c1 == Differential([2/3, 1/3]))
        self.assertTrue(c1 / d1 == Differential([3/2, -3/4]))
        self.assertTrue(d2 / c2 == Differential([5/6, 1/12]))
        self.assertTrue(d3 / c3 == Differential([-5/8, 1/8]))

    def test_differential_pow(self):
        d1 = Differential([2, 1])
        d2 = Differential([10, 1])
        d3 = Differential([-5, 1])

        self.assertTrue(d1 ** 0 == Differential([1, 0]))
        self.assertTrue(d1 ** 1 == Differential([2, 1]))
        self.assertTrue(d1 ** -1 == Differential([1/2, -1/4]))

        self.assertTrue(d2 ** 3 == Differential([1000, 300]))

        self.assertTrue(d3 ** 3 == Differential([-125, 75]))
        self.assertTrue(d3 ** -3 == Differential([-1/125, -3/625]))

    def test_differential_log(self):
        d1 = Differential([2, 1])
        d2 = Differential([10, 1])
        d3 = Differential([-5, 1])

        self.assertTrue(d1.log() == Differential([math.log(2), 1/2]))
        self.assertTrue(d2.log() == Differential([math.log(10), 1/10]))
        self.assertEqual(d2.log(2).interval[0], math.log(10) / math.log(2))
        self.assertEqual(d2.log(2).interval[1], 1 / math.log(1024))

        with self.assertRaises(ValueError):
            d3.log()

    def test_differential_sin(self):
        d1 = Differential([2, 1])
        d2 = Differential([10, 1])
        d3 = Differential([-5, 1])

        self.assertTrue(d1.sin() == Differential([math.sin(2), math.cos(2)]))
        self.assertTrue(d2.sin() == Differential([math.sin(10), math.cos(10)]))
        self.assertTrue(d3.sin() == Differential([- math.sin(5), math.cos(5)]))

    def test_differential_cos(self):
        d1 = Differential([2, 1])
        d2 = Differential([10, 1])
        d3 = Differential([-5, 1])

        self.assertTrue(d1.cos() == Differential([math.cos(2), -math.sin(2)]))
        self.assertTrue(d2.cos() == Differential([math.cos(10), -math.sin(10)]))
        self.assertTrue(d3.cos() == Differential([math.cos(5), math.sin(5)]))

    def test_differential_rmul(self):
        d1 = Differential([2, 1])
        d2 = Differential([10, 1])
        d3 = Differential([-5, 1])

        self.assertTrue(2 * d1 == Differential([4, 2]))
        self.assertTrue(5 * d2 == Differential([50, 5]))
        self.assertTrue(-3 * d3 == Differential([15, -3]))
        self.assertTrue(0 * d1 == Differential([0, 0]))