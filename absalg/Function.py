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
        self.domain = domain
        self.codomain = codomain
        self.function = function
    
    def __call__(self, elem):
        if elem not in self.domain:
            raise TypeError("Function must be called on elements of the domain")
        return self.function(elem)

    def __hash__(self):
        return hash(self.domain) ^ hash(self.codomain) ^ hash(self.function)

    def __eq__(self, other):
        if not isinstance(other, Function):
            return False

        return id(self) == id(other) or ( \
               isinstance(other, Function) and self.domain == other.domain and \
               self.codomain == other.codomain and \
               all(self(elem) == other(elem) for elem in self.domain) )

    def image(self):
        return Set(self(elem) for elem in self.domain)

    def __str__(self):
        """Pretty outputing of functions"""

        # Figure out formatting
        maxlen = max(len(str(x)) for x in self.domain) if self.domain else 0
        formatstr1 = "{0:<%d} -> {1}\n" % maxlen
        formatstr2 = "{0:<%d}{1}\n" % (maxlen + 4)
        nothit = self.codomain - self.image()

        return("".join(formatstr1.format(x, self(x)) for x in self.domain) + \
               "".join(formatstr2.format("", y) for y in nothit))

    def is_surjective(self):
        return self.image() == self.codomain

    def is_injective(self):
        return len(self.image()) == len(self.domain)

    def is_bijective(self):
        return self.is_surjective() and self.is_injective()

    def compose(self, other):
        """Returns x -> self(other(x))"""
        if not self.domain == other.codomain:
            raise ValueError("codomain of other must match domain of self")
        return Function(other.domain, self.codomain, lambda x: self(other(x)))

def identity(s):
    """Returns the identity function on the set s"""
    if not isinstance(s, Set):
        raise TypeError("s must be a set")
    return Function(s, s, lambda x: x)
