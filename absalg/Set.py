"""
Definition of a set
"""

class Set(set):
    def __mul__(self, other):
        """Cartesian product"""
        if not isinstance(other, Set):
            raise TypeError("One of the objects is not a set")
        return Set((x, y) for x in self for y in other)
