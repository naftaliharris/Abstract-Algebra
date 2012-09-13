import unittest
from math import factorial
from absalg.Group import *

class test_group(unittest.TestCase):
    def test_Zn(self):
        for n in range(1, 10):
            Z = Zn(n)
            str(Z)
            self.assertEquals(Z.e, GroupElem(0,Z))
            self.assertEquals(len(Z), n)
            self.assertTrue(all(a * b == GroupElem((a.elem + b.elem) % n, Z) for a in Z for b in Z))
            self.assertTrue(all(Z.inverse(a) == GroupElem((n - a.elem) % n, Z) for a in Z))
            self.assertTrue(Z.is_abelian())
            self.assertTrue(Z <= Z)
            self.assertTrue(Z.is_normal_subgroup(Z))
            self.assertEquals(len(Z/Z), 1)
            if n <= 5: # takes a while
                self.assertEquals(len(Z * Z), n * n)
            self.assertEquals(Z.generate(Z), Z)

    def test_Sn(self):
        for n in range(1, 5):
            S = Sn(n)
            str(S)
            self.assertEquals(S.e, GroupElem(tuple(xrange(n)), S))
            self.assertEquals(len(S), factorial(n))
            self.assertTrue(all(S.inverse(a) == GroupElem( \
                            tuple(dict((a.elem[j], j) for j in a.elem)[i] \
                                  for i in range(n)), S) \
                            for a in S))
            if n <= 2:
                self.assertTrue(S.is_abelian())
            else:
                self.assertFalse(S.is_abelian())
            self.assertTrue(S <= S)
            self.assertTrue(S.is_normal_subgroup(S))
            self.assertEquals(len(S/S), 1)
            if n <= 3:
                self.assertEquals(len(S * S), factorial(n)**2)
            self.assertEquals(S.generate(S), S)

    def test_subgroups(self):
        Z9 = Zn(9)
        self.assertEquals(len(Z9.subgroups()), 3)
        V = Zn(2) * Zn(2)
        self.assertEquals(len(V.subgroups()), 5)
        S3 = Sn(3)
        self.assertEquals(len(S3.subgroups()), 6)

if __name__ == "__main__":
    unittest.main()
