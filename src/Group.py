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

    def inverse(self, elem):
        """Returns the inverse of elem"""
        if not elem in self.G:
            raise TypeError("elem isn't in the group G")
        for a in self.G:
            if self.binary_op((a, elem)) == self.e:
                return a
        raise RuntimeError("Didn't find an inverse for elem")

    def __mul__(self, other):
        """The cartesian product of the two groups"""
        binary_op = Function((self.G * other.G) * (self.G * other.G), \
                             (self.G * other.G), \
                             lambda x: (self.binary_op((x[0][0], x[1][0])), \
                                    other.binary_op((x[0][1], x[1][1]))))

        return Group(self.G * other.G, binary_op)

def Zn(n):
    """ Returns the group (Z_n, +) """
    G = Set(range(n))
    binary_op = Function(G * G, G, lambda x: (x[0] + x[1]) % n)
    return Group(G, binary_op)

