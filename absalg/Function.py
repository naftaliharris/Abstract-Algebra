"""
Definition of a function
"""

from Set import Set

class Function:
    """Definition of a finite function"""
    def __init__(self, domain, codomain, function):
        if not isinstance(domain, Set):
            raise TypeError("Domain must be a Set")
        if not isinstance(codomain, Set):
            raise TypeError("Codomain must be a Set")
        if not all(function(elem) in codomain for elem in domain):
            raise TypeError("Function returns some value outside of codomain")

        self._extras(domain, codomain, function)

        self.domain = domain
        self.codomain = codomain
        self.function = function

    def _extras(self, domain, codomain, function):
        """implemented in Function subclasses for extra __init__ procedures"""
        pass
    
    def __call__(self, elem):
        if elem not in self.domain:
            raise TypeError("Function must be called on elements of the domain")
        return self.function(elem)

    def __hash__(self):
        """Returns the hash of self"""

        # Need to be a little careful, since self.domain and self.codomain are
        # often the same, and we don't want to cancel out their hashes by xoring
        # them against each other.
        # 
        # Also, functions we consider equal, like lambda x: x + 1, and 
        # def jim(x): return x + 1, have different hashes, so we can't include 
        # the hash of self.function.
        #
        # Finally, we should make sure that if you switch the domain and 
        # codomain, the hash will (usually) change, so you can't just add or
        # multiply the hashes together.

        return hash(self.domain) + 2 * hash(self.codomain)

    def __eq__(self, other):
        if not isinstance(other, Function):
            return False

        return id(self) == id(other) or ( \
               self.domain == other.domain and \
               self.codomain == other.codomain and \
               all(self(elem) == other(elem) for elem in self.domain) )

    def __ne__(self, other):
        return not self == other

    def _image(self):
        """The literal image of the function"""
        return Set(self(elem) for elem in self.domain)

    def image(self):
        """
        The API image of the function; can change depending on the subclass.

        For example, GroupHomomorphisms return the image as a Group, not a Set.
        """
        return self._image()

    def __str__(self):
        """Pretty outputing of functions"""

        # Figure out formatting
        maxlen = max(len(str(x)) for x in self.domain) if self.domain else 0
        formatstr1 = "{0:<%d} -> {1}\n" % maxlen
        formatstr2 = "{0:<%d}{1}\n" % (maxlen + 4)
        nothit = self.codomain - self._image()

        return("".join(formatstr1.format(x, self(x)) for x in self.domain) + \
               "".join(formatstr2.format("", y) for y in nothit))

    def is_surjective(self):
        return self._image() == self.codomain

    def is_injective(self):
        return len(self._image()) == len(self.domain)

    def is_bijective(self):
        return self.is_surjective() and self.is_injective()

    def compose(self, other):
        """Returns x -> self(other(x))"""
        if not self.domain == other.codomain:
            raise ValueError("codomain of other must match domain of self")
        return Function(other.domain, self.codomain, lambda x: self(other(x)))

    def new_domains(self, domain, codomain):
        return Function(domain, codomain, self.function)

def identity(s):
    """Returns the identity function on the set s"""
    if not isinstance(s, Set):
        raise TypeError("s must be a set")
    return Function(s, s, lambda x: x)
