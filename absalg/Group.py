"""Group implementation"""

import itertools

from Set import Set
from Function import Function

class GroupElem:
    """
    Group element definition
    
    This is mainly syntactic sugar, so you can write stuff like g * h
    instead of group.bin_op(g, h), or group(g, h).
    """

    def __init__(self, elem, group):
        if not isinstance(group, Group):
            raise TypeError("group is not a Group")
        if not elem in group.Set:
            raise TypeError("elem is not an element of group")
        self.elem = elem
        self.group = group

    def __str__(self):
        return str(self.elem)

    def __eq__(self, other):
        """
        Two GroupElems are equal if they represent the same element,
        regardless of the Groups they belong to
        """

        if not isinstance(other, GroupElem):
            raise TypeError("other is not a GroupElem")
        return self.elem == other.elem

    def __hash__(self):
        return hash(self.elem)

    def __mul__(self, other):
        """
        If other is a group element, returns self * other.
        If other = n is an int, and self is in an abelian group, returns self**n
        """
        if self.group.is_abelian() and isinstance(other, (int, long)):
            return self ** other

        if not isinstance(other, GroupElem):
            raise TypeError("other must be a GroupElem, or an int " \
                            "(if self's group is abelian)")
        try:
            return GroupElem(self.group.bin_op((self.elem, other.elem)), \
                             self.group)
        # This can return a TypeError in Funcion.__call__ if self and other
        # belong to different Groups. So we see if we can make sense of this
        # operation the other way around.
        except TypeError:
            return other.__rmul__(self)

    def __rmul__(self, other):
        """
        If other is a group element, returns other * self.
        If other = n is an int, and self is in an abelian group, returns self**n
        """
        if self.group.is_abelian() and isinstance(other, (int, long)):
            return self ** other

        if not isinstance(other, GroupElem):
            raise TypeError("other must be a GroupElem, or an int " \
                            "(if self's group is abelian)")

        return GroupElem(self.group.bin_op((other.elem, self.elem)), self.group)

    def __add__(self, other):
        """Returns self + other for Abelian groups"""
        if self.group.is_abelian():
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
        if not self.group.is_abelian():
            raise TypeError("self must be in an abelian group")
        return self ** (-1)

    def __sub__(self, other):
        """Returns self * (other ** -1) if self is in an abelian group"""
        if not self.group.is_abelian():
            raise TypeError("self must be in an abelian group")
        return self * (other ** -1)

class Group:
    """Group definition"""
    def __init__(self, G, bin_op):
        """Create a group, checking group axioms"""

        # Test types
        if not isinstance(G, Set): raise TypeError("G must be a set")
        if not isinstance(bin_op, Function):
            raise TypeError("bin_op must be a function")
        if bin_op.codomain != G:
            raise TypeError("binary operation must have codomain equal to G")
        if bin_op.domain != G * G:
            raise TypeError("binary operation must have domain equal to G * G")

        # Test associativity
        if not all(bin_op((a, bin_op((b, c)))) == \
                   bin_op((bin_op((a, b)), c)) \
                   for a in G for b in G for c in G):
            raise ValueError("binary operation is not associative")

        # Find the identity
        found_id = False
        for e in G:
            if all(bin_op((e, a)) == a for a in G):
                found_id = True
                break
        if not found_id:
            raise ValueError("G doesn't have an identity")

        # Test for inverses
        for a in G:
            if not any(bin_op((a,  b)) == e for b in G):
                raise ValueError("G doesn't have inverses")

        # At this point, we've verified that we have a Group.
        # Now determine if the Group is abelian:
        self.abelian = all(bin_op((a, b)) == bin_op((b, a)) \
                           for a in G for b in G)

        self.Set = G
        self.group_elems = Set(GroupElem(g, self) for g in G)
        self.e = GroupElem(e, self)
        self.bin_op = bin_op

    def __iter__(self):
        """Iterate over the GroupElems in G, returning the identity first"""
        yield self.e
        for g in self.group_elems:
            if g != self.e: yield g

    def __hash__(self):
        return hash(self.Set) ^ hash(self.bin_op)

    def __eq__(self, other):
        if not isinstance(other, Group):
            return False

        return id(self) == id(other) or \
               (self.Set == other.Set and self.bin_op == other.bin_op)

    def __len__(self):
        return len(self.Set)

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
                              " | ".join(toletter[toelem[l] * toelem[l1]] \
                                         for l1 in letters) + \
                              " |\n" for l in letters)
        result += border
        return result

    def is_abelian(self):
        """Checks if the group is abelian"""
        return self.abelian

    def __le__(self, other):
        """Checks if self is a subgroup of other"""
        if not isinstance(other, Group):
            raise TypeError("other must be a Group")
        return self.Set <= other.Set and \
               all(self.bin_op((a, b)) == other.bin_op((a, b)) \
                   for a in self.Set for b in self.Set)

    def is_normal_subgroup(self, other):
        """Checks if self is a normal subgroup of other"""
        return self <= other and \
               all(Set(g * h for h in self) == Set(h * g for h in self) \
                   for g in other)

    def __div__(self, other):
        """ Returns the quotient group self / other """
        if not other.is_normal_subgroup(self):
            raise ValueError("other must be a normal subgroup of self")
        G = Set(Set(self.bin_op((g, h)) for h in other.Set) for g in self.Set)

        def multiply_cosets(x):
            for h in x[0]: break # pick some h from the first coset
            return Set(self.bin_op((h, g)) for g in x[1])

        return Group(G, Function(G * G, G, multiply_cosets))

    def inverse(self, g):
        """Returns the inverse of elem"""
        if not g in self.group_elems:
            raise TypeError("g isn't a GroupElem in the Group")
        for a in self:
            if g * a == self.e:
                return a
        raise RuntimeError("Didn't find an inverse for g")

    def __mul__(self, other):
        """Returns the cartesian product of the two groups"""
        if not isinstance(other, Group):
            raise TypeError("other must be a group")
        bin_op = Function((self.Set * other.Set) * (self.Set * other.Set), \
                             (self.Set * other.Set), \
                             lambda x: (self.bin_op((x[0][0], x[1][0])), \
                                        other.bin_op((x[0][1], x[1][1]))))

        return Group(self.Set * other.Set, bin_op)

    def generate(self, elems):
        """
        Returns the subgroup of self generated by GroupElems elems
        
        elems must be iterable
        """
        if not Set(elems) <= self.group_elems:
            raise ValueError("elems must be a subset of self.group_elems")
        if len(elems) == 0:
            raise ValueError("elems must have at least one element")

        oldG = Set(elems)
        while True:
            newG = oldG | Set(a * b for a in oldG for b in oldG)
            if oldG == newG: break
            else: oldG = newG
        oldG = Set(g.elem for g in oldG)

        return Group(oldG, Function(oldG * oldG, oldG, self.bin_op))

    def subgroups(self):
        """Returns the Set of self's subgroups"""

        old_sgs = Set([self.generate([self.e])])
        while True:
            new_sgs = old_sgs | Set(self.generate(list(sg.group_elems) + [g]) \
                                     for sg in old_sgs for g in self \
                                     if g not in sg.group_elems)
            if new_sgs == old_sgs: break
            else: old_sgs = new_sgs

        return old_sgs

def Zn(n):
    """ Returns the cylic group of order n"""
    G = Set(range(n))
    bin_op = Function(G * G, G, lambda x: (x[0] + x[1]) % n)
    return Group(G, bin_op)

def Sn(n):
    """ Returns the symmetric group of order n! """
    G = Set(g for g in itertools.permutations(range(n)))
    bin_op = Function(G * G, G, lambda x: tuple(x[0][j] for j in x[1]))
    return Group(G, bin_op)
