"""Group implementation"""

import itertools

from Set import Set
from Function import Function

class GroupElem:
    """
    Group element definition
    
    This is mainly syntactic sugar, so you can write stuff like g * h
    instead of group.binary_op(g, h), or group(g, h).
    """

    def __init__(self, elem, group):
        if not isinstance(group, Group):
            raise TypeError("group is not a Group")
        if not elem in group.G:
            raise TypeError("elem is not an element of group")
        self.elem = elem
        self.group = group
        self.abelian = group.is_abelian()

    def __str__(self):
        return str(self.elem)

    def __eq__(self, other):
        if not isinstance(other, GroupElem):
            raise TypeError("other is not a GroupElem")
        return id(self) == id(other) or \
               (self.elem == other.elem and self.group == other.group)

    def __hash__(self):
        return hash(self.elem) ^ hash(self.group)

    def __mul__(self, other):
        """
        If other is a group element, returns self * other.
        If other = n is an int, and self is in an abelian group, returns self**n
        """
        if self.abelian and isinstance(other, (int, long)):
            return self ** other

        if not isinstance(other, GroupElem):
            raise TypeError("other must be a GroupElem, or an int " \
                            "(if self's group is abelian)")
        if not self.group == other.group:
            raise ValueError("self and other must be in the same group")

        return GroupElem(self.group(self.elem, other.elem), self.group)

    def __rmul__(self, other):
        """Returns self ** n if self is in an abelian group"""
        if self.abelian and isinstance(other, (int, long)):
            return self ** other
        raise TypeError("self's group must be abelian and other must be an int")

    def __add__(self, other):
        """Returns self + other for Abelian groups"""
        if self.abelian:
            return self * other
        raise TypeError("not an element of an abelian group")
        
    def __pow__(self, n, modulo=None):
        """
        Returns self**n
        
        modulo is included as an argument to comply with the API, and ignored
        """
        if not isinstance(n, (int, long)):
            raise TypeError("n must be an int or a long")

        if n == 0:
            return self.group.e
        elif n < 0:
            return GroupElem(self.group.inverse(self.elem), self.group) ** -n
        elif n % 2 == 1:
            return self * (self ** (n - 1))
        else:
            return (self * self) ** (n / 2)

    def __neg__(self):
        """Returns self ** -1 if self is in an abelian group"""
        if not self.abelian:
            raise TypeError("self must be in an abelian group")
        return self ** (-1)

    def __sub__(self, other):
        """Returns self * (other ** -1) if self is in an abelian group"""
        if not self.abelian:
            raise TypeError("self must be in an abelian group")
        return self * (other ** -1)

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
        self.abelian = None # Compute this lazily

    def __iter__(self):
        """Iterate over the elements in G, returning the identity first"""
        yield self.e
        for g in self.G:
            if g != self.e: yield g

    def __hash__(self):
        return hash(self.G) ^ hash(self.binary_op)

    def __eq__(self, other):
        if not isinstance(other, Group):
            return False

        return id(self) == id(other) or \
               (self.G == other.G and self.binary_op == other.binary_op)

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
        if self.abelian is None:
            self.abelian = all(self(a, b) == self(b, a) \
                               for a in self for b in self)

        return self.abelian

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

    def generate(self, elems):
        """
        Returns the subgroup of self generated by elems
        
        elems must be iterable
        """
        if not Set(elems) <= self.G:
            raise ValueError("elems must be a subset of self.G")
        if len(elems) == 0:
            raise ValueError("elems must have at least one element")

        oldG = Set(elems)
        while True:
            newG = oldG | Set(self(a, b) for a in oldG for b in oldG)
            if oldG == newG: break
            else: oldG = newG

        return Group(oldG, Function(oldG * oldG, oldG, self.binary_op))

    def subgroups(self):
        """Returns the Set of self's subgroups"""

        old_sgs = Set([self.generate([self.e])])
        while True:
            new_sgs = old_sgs | Set(self.generate(list(sg.G) + [g]) \
                                     for sg in old_sgs for g in self \
                                     if g not in sg.G)
            if new_sgs == old_sgs: break
            else: old_sgs = new_sgs

        return old_sgs

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
