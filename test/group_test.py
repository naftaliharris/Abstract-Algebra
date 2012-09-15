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
        G = Zn(9)
        sgs = G.subgroups()
        self.assertEquals(len(sgs), 3)
        for H in sgs:
            if H.is_normal_subgroup(G):
                self.assertEquals(len(G / H) * len(H), len(G))

        G = Zn(2) * Zn(2)
        sgs = G.subgroups()
        self.assertEquals(len(sgs), 5)
        for H in sgs:
            if H.is_normal_subgroup(G):
                self.assertEquals(len(G / H) * len(H), len(G))

        G = Sn(3)
        sgs = G.subgroups()
        self.assertEquals(len(G.subgroups()), 6)
        for H in sgs:
            if H.is_normal_subgroup(G):
                self.assertEquals(len(G / H) * len(H), len(G))

    def test_group_elem(self):
        V = Zn(2) * Zn(2)
        e, a, b, c = tuple(g for g in V)
        self.assertEquals(a + b + c, e)
        self.assertEquals(a + b, c)
        self.assertEquals(b + c, a)
        self.assertEquals(a + c, b)
        for g in V:
            self.assertTrue(g in V)
            self.assertEquals(g, g)
            self.assertEquals(e * g, g)
            self.assertEquals(g * e, g)
            self.assertEquals(e + g, g)
            self.assertEquals(g + e, g)
            self.assertEquals(g * g, e)
            self.assertEquals(g + g, e)
            self.assertEquals(g ** -1, g)
            self.assertEquals(-g, g)
            self.assertEquals(-g, g ** -1)
            self.assertEquals(g ** 209325, g)
            self.assertEquals(g ** -23234, e)
            for n in range(-10, 10):
                self.assertEquals(g * n, g ** n)
                self.assertEquals(n * g, g ** n)
                self.assertEquals(n * g, g * n)
        for g in [a, b, c]:
            self.assertTrue(e != g)

        G = Sn(3)
        for g in G:
            with self.assertRaises(TypeError):
                g + g
            with self.assertRaises(TypeError):
                g * 2
            with self.assertRaises(TypeError):
                2 * g
            with self.assertRaises(TypeError):
                -g
        for H in G.subgroups():
            for g in G:
                self.assertEquals(g ** 5, g * g * g * g * g)
                for h in H:
                    self.assertEquals(h ** 2, h * h)
                    self.assertEquals(h * g, GroupElem(h.elem, G) * g)
                    self.assertEquals(g * h, g * GroupElem(h.elem, G))

    def test_generators(self):
        for G in [Zn(1), Zn(2), Zn(5), Zn(8), Sn(1), Sn(2), Sn(3), \
                  Dn(1), Dn(2), Dn(3), Dn(4)]:
            self.assertEquals(G, G.generate(G.generators()))
            self.assertEquals(G, G.generate(g.elem for g in G.generators()))

    def test_find_isomorphism(self):
        f = Dn(2).find_isomorphism(Zn(2) * Zn(2))
        self.assertTrue(f is not None)
        self.assertTrue(f.is_isomorphism())
        self.assertEquals(f.kernel(), Dn(2).generate([Dn(2).e]))
        self.assertEquals(f.image(), Zn(2) * Zn(2))

        self.assertFalse(Dn(12).is_isomorphic(Sn(4)))
        self.assertFalse(Sn(3).is_isomorphic(Zn(6)))
        self.assertFalse(Sn(3).is_isomorphic(Zn(4)))

        for G in [Zn(1), Zn(2), Zn(5), Sn(1), Sn(3), Dn(1), Dn(4)]:
            self.assertTrue(G.is_isomorphic(G))
            f = G.find_isomorphism(G)
            self.assertTrue(f is not None)
            self.assertTrue(f.is_isomorphism())
            self.assertEquals(f.kernel(), G.generate([G.e]))
            self.assertEquals(f.image(), G)

        self.assertTrue(Zn(1).is_isomorphic(Sn(1)))
        self.assertTrue(Zn(2).is_isomorphic(Sn(2)))
        self.assertTrue(Zn(2).is_isomorphic(Dn(1)))

    def test_cyclic(self):
        for n in range(1, 10):
            self.assertTrue(Zn(n).is_cyclic())

        self.assertTrue(Sn(1).is_cyclic())
        self.assertTrue(Sn(2).is_cyclic())
        self.assertFalse(Sn(3).is_cyclic())

        self.assertTrue(Dn(1).is_cyclic())
        self.assertFalse(Dn(2).is_cyclic())
        self.assertFalse(Dn(3).is_cyclic())


if __name__ == "__main__":
    unittest.main()
