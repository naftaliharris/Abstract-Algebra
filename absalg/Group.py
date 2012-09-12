"""Group implementation"""

import string
import itertools

from Set import Set
from Function import Function

class Group:
    """Group definition"""
    def __init__(self, G, binary_op):
        """Create a group, checking group axioms"""

        # Test types
        if not isinstance(G, Set): raise TypeError("G must be a set")
        if not isinstance(binary_op, Function):
            raise TypeError("binary_op must be a function")
        if binary_op.codomain != G:
            raise TypeError("binary operation must have codomain equal to G")
        if binary_op.domain != G * G:
            raise TypeError("binary operation must have domain equal to G * G")

        # Test associativity
        if not all(binary_op((a, binary_op((b, c)))) == \
                   binary_op((binary_op((a, b)), c)) \
                   for a in G for b in G for c in G):
            raise ValueError("binary operation is not associative")

        # Find the identity
        found_id = False
        for e in G:
            if all(binary_op((e, a)) == a for a in G):
                found_id = True
                break
        if not found_id:
            raise ValueError("G doesn't have an identity")

        # Test for inverses
        for a in G:
            if not any(binary_op((a,  b)) == e for b in G):
                raise ValueError("G doesn't have inverses")

        self.G = G
        self.e = e
        self.binary_op = binary_op

    def __iter__(self):
        """Iterate over the elements in G, returning the identity first"""
        yield self.e
        for g in self.G:
            if g != self.e: yield g

    def __len__(self):
        return len(self.G)

    def __call__(self, a, b):
        """Returns a * b"""
        return self.binary_op((a, b))

    def __str__(self):
        """Returns the Cayley table"""
        
        letters = "eabcdfghijklmnopqrstuvwxyz"
        if len(self) > len(letters):
            return "This group is too big to print a Cayley table"

        # connect letters to elements
        toletter = {}
        toelem = {}
        for letter, elem in zip(letters, self):
            toletter[elem] = letter
            toelem[letter] = elem
        letters = letters[:len(self)]

        # Display the mapping:
        result = "\n".join("%s: %s" % (l, toelem[l]) for l in letters) + "\n\n"

        # Make the graph
        head = "   | " + " | ".join(l for l in letters) + " |"
        border = (len(self) + 1) * "---+" + "\n"
        result += head + "\n" + border
        result += border.join(" %s | " % l + \
                              " | ".join(toletter[self(toelem[l], toelem[l1])] \
                                         for l1 in letters) + \
                              " |\n" for l in letters)
        result += border
        return result

    def is_abelian(self):
        """Checks if the group is abelian"""
        return all(self(a, b) == self(b, a) for a in self for b in self)

    def is_subgroup(self, other):
        """Checks if self is a subgroup of other"""
        if not isinstance(other, Group):
            raise TypeError("other must be a group")
        return self.G <= other.G and \
               all(self(a, b) == other(a, b) for a in self for b in self)

    def is_normal_subgroup(self, other):
        """Checks if self is a normal subgroup of other"""
        return self.is_subgroup(other) and \
               all(Set(other(g, h) for h in self) == \
                   Set(other(h, g) for h in self) \
                   for g in other)

    def __div__(self, other):
        """ Returns the quotient group self / other """
        if not other.is_normal_subgroup(self):
            raise ValueError("other must be a normal subgroup of self")
        G = Set(Set(self(g, h) for h in other) for g in self)

        def multiply_cosets(x):
            for h in x[0]: break # pick some h from the first coset
            return Set(self(h, g) for g in x[1])

        return Group(G, Function(G * G, G, multiply_cosets))

    def inverse(self, elem):
        """Returns the inverse of elem"""
        if not elem in self.G:
            raise TypeError("elem isn't in the group G")
        for a in self.G:
            if self(a, elem) == self.e:
                return a
        raise RuntimeError("Didn't find an inverse for elem")

    def __mul__(self, other):
        """Returns the cartesian product of the two groups"""
        if not isinstance(other, Group):
            raise TypeError("other must be a group")
        binary_op = Function((self.G * other.G) * (self.G * other.G), \
                             (self.G * other.G), \
                             lambda x: (self(x[0][0], x[1][0]), \
                                    other(x[0][1], x[1][1])))

        return Group(self.G * other.G, binary_op)

def Zn(n):
    """ Returns the cylic group of order n"""
    G = Set(range(n))
    binary_op = Function(G * G, G, lambda x: (x[0] + x[1]) % n)
    return Group(G, binary_op)

def Sn(n):
    """ Returns the symmetric group of order n! """
    G = Set(g for g in itertools.permutations(range(n)))
    binary_op = Function(G * G, G, lambda x: tuple(x[0][j] for j in x[1]))
    return Group(G, binary_op)
