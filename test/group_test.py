import unittest
from math import factorial
from absalg.Group import *

class test_group(unittest.TestCase):
    def test_Zn(self):
        for n in range(1, 10):
            Z = Zn(n)
            str(Z)
            self.assertEquals(Z.e, 0)
            self.assertEquals(len(Z), n)
            self.assertTrue(all(Z(a, b) == (a + b) % n for a in Z for b in Z))
            self.assertTrue(all(Z.inverse(a) == (n - a) % n for a in Z))
            self.assertTrue(Z.is_abelian())
            self.assertTrue(Z.is_subgroup(Z))
            self.assertTrue(Z.is_normal_subgroup(Z))
            self.assertEquals(len(Z/Z), 1)
            if n <= 5: # takes a while
                self.assertEquals(len(Z * Z), n * n)
            self.assertEquals(Z.generate(Z.G), Z)

    def test_Sn(self):
        for n in range(1, 5):
            S = Sn(n)
            str(S)
            self.assertEquals(S.e, tuple(xrange(n)))
            self.assertEquals(len(S), factorial(n))
            self.assertTrue(all(S.inverse(a) == \
                            tuple(dict((a[j], j) for j in a)[i] \
                                  for i in range(n)) \
                            for a in S))
            if n <= 2:
                self.assertTrue(S.is_abelian())
            else:
                self.assertFalse(S.is_abelian())
            self.assertTrue(S.is_subgroup(S))
            self.assertTrue(S.is_normal_subgroup(S))
            self.assertEquals(len(S/S), 1)
            if n <= 3:
                self.assertEquals(len(S * S), factorial(n)**2)
            self.assertEquals(S.generate(S.G), S)

    def test_subgroups(self):
        Z9 = Zn(9)
        self.assertEquals(len(Z9.subgroups()), 3)
        V = Zn(2) * Zn(2)
        self.assertEquals(len(V.subgroups()), 5)
        S3 = Sn(3)
        self.assertEquals(len(S3.subgroups()), 6)

if __name__ == "__main__":
    unittest.main()
