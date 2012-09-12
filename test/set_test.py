import unittest
from absalg.Set import *

class test_set(unittest.TestCase):
    def test_basics(self):
        for n in range(10):
            s = Set(range(n))
            t = Set(xrange(n))
            self.assertEquals(s, s)
            self.assertEquals(s, t)
            self.assertEquals(t, s)
            self.assertEquals(t, t)
            self.assertEquals(len(s), n)

    def test_product(self):
        for n in range(10):
            s = Set(range(n))
            self.assertEquals(s * s, \
                              Set((x, y) for x in range(n) for y in range(n)))

        self.assertEquals(Set(range(10)) * Set([]), Set([]))

if __name__ == "__main__":
    unittest.main()
