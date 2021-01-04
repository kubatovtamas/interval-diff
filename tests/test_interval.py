import unittest
from interval import *



class IntervalClassTestCase(unittest.TestCase):
    def test_interval_init(self):
        t1 = Interval([1, 5])
        self.assertIsInstance(t1, Interval)
        self.assertEqual(t1.low, t1.interval[0])
        self.assertEqual(t1.high, t1.interval[1])
        self.assertEqual(t1.low, 1)
        self.assertEqual(t1.high, 5)

    def test_interval_str(self):
        t1 = Interval([1, 5])
        t3 = Interval([1.0001, 5])
        self.assertEqual(str(t1), "[1, 5]")
        self.assertEqual(str(t3), "[1.0001, 5]")

    def test_interval_eq(self):
        t1 = Interval([1, 5])
        t2 = Interval([1, 5])
        t3 = Interval([1.0001, 5])
        t4 = Interval([1.0002, 5])
        self.assertTrue(t1 == t2)
        self.assertTrue(t1 == t3)
        self.assertFalse(t1 == t4)

    def test_interval_add(self):
        t1 = Interval([0, 1])
        t2 = Interval([2, 3])
        t3 = Interval([1, 2])
        t4 = Interval([-3, 4])

        self.assertTrue((t1 + t2) == Interval([2, 4]))
        self.assertTrue((t3 + t4) == Interval([-2, 6]))

        self.assertTrue((t3 + t4) == (t4 + t3))
        self.assertTrue((t3 + t4) == (t4 + t3))

        t5 = (t3 + t4)
        self.assertTrue(t5 == (t4 + t3))
        self.assertTrue(t5 + t1 == (t4 + t3) + t1)

        self.assertTrue(t1 + t2 + t3 == Interval([3, 6]))

    def test_interval_sub(self):
        t1 = Interval([0, 1])
        t2 = Interval([2, 3])
        t3 = Interval([1, 2])
        t4 = Interval([-3, 4])

        self.assertTrue(t1 - t2 == Interval([-3, -1]))
        self.assertTrue(t2 - t1 == Interval([1, 3]))
        self.assertTrue(t3 - t4 == Interval([-3, 5]))

    def test_interval_mul(self):
        t1 = Interval([0, 1])
        t2 = Interval([2, 3])
        t3 = Interval([1, 2])
        t4 = Interval([-3, 4])

        self.assertTrue(t1 * t2 == Interval([0, 3]))
        self.assertTrue(t3 * t4 == Interval([-6, 8]))

    def test_interval_div(self):
        t1 = Interval([1, 2])
        t2 = Interval([-3, 4])

        with self.assertRaises(ZeroDivisionError):
            t3 = t1 / t2
        self.assertTrue(t1 / t1 == Interval([0.5, 2]))

    def test_interval_pow(self):
        t1 = Interval([-1, 2])
        t2 = Interval([1, 2])
        t3 = Interval([-2, -1])
        t4 = Interval([-3, -2])

        self.assertTrue(t1 ** 3 == Interval([0, 8]))
        self.assertTrue(t1 ** 2 == Interval([0, 4]))

        self.assertTrue(t2 ** 2 == Interval([1, 4]))
        self.assertTrue(t2 ** 0 == Interval([1, 1]))
        self.assertTrue(t2 ** 1 == t2)
        self.assertTrue(t2 ** 3 == Interval([1, 8]))

        self.assertTrue(t2 ** -1 == Interval([0.5, 1]))
        self.assertTrue(t2 ** -2 == Interval([0.25, 1]))
        self.assertTrue(t2 ** -3 == Interval([1/8, 1]))

        self.assertTrue(t3 ** -1 == Interval([-1, -1/2]))
        self.assertTrue(t3 ** -3 == Interval([-1, -1/8]))
        self.assertTrue(t3 ** -4 == Interval([1/16, 1]))

        self.assertTrue(t4 ** -3 == Interval([-1/8, -1/27]))
        self.assertTrue(t4 ** 0 == Interval([1, 1]))

    def test_interval_exp(self):
        t1 = Interval([1, 2])
        t2 = Interval([-2, 2])
        t3 = Interval([-6, 8])
        t4 = Interval([0, 2])

        self.assertTrue(math.e ^ t1 == Interval([math.e, math.e ** 2]))
        self.assertTrue(2 ^ t2 == Interval([2 ** -2, 2 ** 2]))
        self.assertTrue(math.pi ^ t3 == Interval([math.pi ** -6, math.pi ** 8]))
        self.assertTrue(2 ^ t4 == Interval([1, 4]))

    def test_interval_log(self):
        t1 = Interval([-1, 2])
        t2 = Interval([0, 2])
        t3 = Interval([2, 5])
        t4 = Interval([1, 3])

        with self.assertRaises(ValueError):
            Interval.log(t1)
            Interval.log(t2)
            Interval.log(t3, 0)
            Interval.log(t3, 0.5)

        self.assertEqual(Interval.log(t3), Interval([math.log(2), math.log(5)]))
        self.assertEqual(Interval.log(t4), Interval([math.log(1), math.log(3)]))

    def test_interval_sin(self):
        t1 = Interval([0, math.pi])
        t2 = Interval([-4 * math.pi, 5 * math.pi / 2])
        t3 = Interval([math.pi, 4 * math.pi])
        t4 = Interval([0, 4])
        t5 = Interval([0, 2 * math.pi])
        t6 = Interval([-1 * math.pi / 2, 0])
        t7 = Interval([-1 * math.pi / 2, 1])

        self.assertTrue(Interval.sin(t1) == Interval([0, 1]))
        self.assertTrue(Interval.sin(t2) == Interval([-1, 1]))
        self.assertTrue(Interval.sin(t3) == Interval([-1, 1]))
        self.assertTrue(Interval.sin(t4) == Interval([-0.7568, 1]))
        self.assertTrue(Interval.sin(t5) == Interval([-1, 1]))
        self.assertTrue(Interval.sin(t6) == Interval([-1, 0]))
        self.assertTrue(Interval.sin(t7) == Interval([-1, math.sin(1)]))

    def test_cos_interval(self):
        t1 = Interval([0, 4])
        t2 = Interval([math.pi, 4 * math.pi])
        t3 = Interval([0, 13])
        t4 = Interval([0, 7])
        t5 = Interval([-math.pi / 2, 0])
        t6 = Interval([-math.pi, -math.pi / 2])

        self.assertTrue(Interval.cos(t1) == Interval([-1, 1]))
        self.assertTrue(Interval.cos(t2) == Interval([-1, 1]))
        self.assertTrue(Interval.cos(t3) == Interval([-1, 1]))
        self.assertTrue(Interval.cos(t4) == Interval([-1, 1]))
        self.assertTrue(Interval.cos(t5) == Interval([0, 1]))
        self.assertTrue(Interval.cos(t6) == Interval([-1, 0]))