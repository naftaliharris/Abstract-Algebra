import unittest
from absalg.Set import Set
from absalg.Function import *

class test_function(unittest.TestCase):
    def test_basics(self):
        s = Set([0, 1, 2, 3])
        t = Set([1, 2, 3, 4])
        f = Function(s, t, lambda x: x + 1)
        for x in range(4):
            self.assertEquals(f(x), x + 1)
        self.assertEquals(f, f)

        with self.assertRaises(TypeError):
            Function([0, 1, 2, 3], t, lambda x: x + 1)
        with self.assertRaises(TypeError):
            Function(s, [1, 2, 3, 4], lambda x: x + 1)
        with self.assertRaises(TypeError):
            Function(s, t, lambda x: x + 2)

    def test_simple(self):
        s = Set([0, 1, 2, 3])
        t = Set([1, 2, 3, 4])
        u = Set([0, 1, 2, 3, 4, 5])
        f = Function(s, t, lambda x: x + 1)
        g = Function(t, u, lambda x: x + 1)
        h = g.compose(f)
        i = Function(Set([-1, 0, 1]), Set([0, 1]), lambda x: abs(x))

        self.assertEquals(f.is_surjective(), True)
        self.assertEquals(f.is_injective(), True)
        self.assertEquals(f.is_bijective(), True)
        self.assertEquals(f.image(), t)

        self.assertEquals(g.is_surjective(), False)
        self.assertEquals(g.is_injective(), True)
        self.assertEquals(g.is_bijective(), False)
        self.assertEquals(g.image(), Set([2, 3, 4, 5]))

        self.assertEquals(h.is_surjective(), False)
        self.assertEquals(h.is_injective(), True)
        self.assertEquals(h.is_bijective(), False)
        self.assertEquals(h.image(), Set([2, 3, 4, 5]))

        self.assertEquals(i.is_surjective(), True)
        self.assertEquals(i.is_injective(), False)
        self.assertEquals(i.is_bijective(), False)
        self.assertEquals(i.image(), Set([0, 1]))

        with self.assertRaises(ValueError):
            i.compose(f)
        with self.assertRaises(ValueError):
            f.compose(i)

    def test_identity(self):
        s = Set(["las", 3, "ksjfdlka"])
        ID = identity(s)
        for item in s:
            self.assertEquals(ID(item), item)

if __name__ == "__main__":
    unittest.main()
