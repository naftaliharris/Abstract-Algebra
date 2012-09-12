"""
Implementation of Set
"""

class Set(frozenset):
    """
    Definition of a Set
    
    It's important that Set be a subclass of frozenset, (not set), because:
    1) it makes Set immutable
    2) it allows Set to contains Sets
    """
    def __mul__(self, other):
        """Cartesian product"""
        if not isinstance(other, Set):
            raise TypeError("One of the objects is not a set")
        return Set((x, y) for x in self for y in other)
