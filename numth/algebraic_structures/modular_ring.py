#   numth/algebraic_structures/modular_ring.py
#===========================================================
from collections import Counter
from functools import reduce

from ..basic import gcd, mod_inverse, mod_power, prime_to
from ..factorization import factor
from ..modular import carmichael_lambda, euler_phi, mod_sqrt
#===========================================================

class ModularRing:
    """
    Class for arithmetic in the ring of integers relative to a modulus.
    """
    def __init__(self, modulus):
        self.modulus = modulus
        if modulus == 2:
            self.orders = {1 : 1}
        else:
            self.orders = {1 : 1, modulus - 1 : 2}

        self._factorization = None
        self._euler = None
        self._carmichael = None
        self._carmichael_factorization = None
        self._multiplicative_group = None
        self._generator = None
        self._as_cyclic_group = None
        self._discrete_log = None

    #=========================

    def factorization(self):
        """Factorize the modulus."""
        if self._factorization is None:
            self._factorization = factor(self.modulus)
        return self._factorization

    #-------------------------

    def euler(self):
        """Compute size of multiplicative group."""
        if self._euler is None:
            self._euler = euler_phi(self.factorization())
        return self._euler

    #-------------------------

    def carmichael(self):
        """Compute maximum order of element of multiplicative group."""
        if self._carmichael is None:
            self._carmichael = carmichael_lambda(self.factorization())
        return self._carmichael

    #-------------------------

    def carmichael_factorization(self):
        """Factorize the maximum order.  Used for calculating orders."""
        if self._carmichael_factorization is None:
            self._carmichael_factorization = factor(self.carmichael())
        return self._carmichael_factorization

    #-------------------------

    def carmichael_primes(self):
        """Prime factors of maximum order.  Used for calculating orders."""
        return Counter(self.carmichael_factorization()).elements()

    #-------------------------

    def is_cyclic(self):
        """Whether the multiplicative group is cyclic."""
        return self.euler() == self.carmichael()

    #-------------------------

    def multiplicative_group(self):
        """Compute the multiplicative group."""
        if self._multiplicative_group is None:
            self._multiplicative_group = prime_to(self.factorization())
        return self._multiplicative_group

    #-------------------------

    def generator(self):
        """Find a generator of the multiplicative group if cyclic."""
        if self._generator is None and self.is_cyclic():
            for x in self.multiplicative_group():
                if self.order_of(x) == self.euler():
                    self._generator = x
                    break
        return self._generator

    #-------------------------

    def as_cyclic_group(self):
        """Realize multiplicative group as a cyclic group for a generator."""
        if self._as_cyclic_group is None and self.is_cyclic():
            self._as_cyclic_group = self.cyclic_subgroup_from(self.generator())
            if self._multiplicative_group is None:
                self._multiplicative_group = sorted(self._as_cyclic_group.values())
        return self._as_cyclic_group

    #-------------------------

    def discrete_log(self):
        """Compute a discrete log table for multiplicative group if cyclic."""
        if self._discrete_log is None and self.is_cyclic():
            self._discrete_log = {x : e for e, x in self.as_cyclic_group().items()}
        return self._discrete_log

    #-------------------------

    def all_orders(self):
        """Compute orders of all elements of multiplicative group."""
        if len(self.orders) != self.euler():
            if self.is_cyclic():
                self.generator()
            for x in self.multiplicative_group():
                self.order_of(x)
        return self.orders

    #-------------------------

    def all_generators(self):
        """Compute all generators of multiplicative group if cyclic."""
        return [x for x, o in self.all_orders().items() if o == self.euler()]

    #=========================

    def elem(self, number):
        """Cast number to element of modular ring."""
        return number % self.modulus

    #-------------------------

    def add(self, *elements):
        """Add elements in modular ring."""
        return reduce(lambda x, y: (x + y) % self.modulus, elements, 0)

    #-------------------------

    def mult(self, *elements):
        """Multiply elements in modular ring."""
        return reduce(lambda x, y: (x * y) % self.modulus, elements, 1)

    #-------------------------

    def power_of(self, element, exponent):
        """Compute power of element in modular ring."""
        return mod_power(element, exponent, self.modulus)

    #-------------------------

    def inverse_of(self, element):
        """Compute inverse of element of multiplicative group."""
        return mod_inverse(element, self.modulus)

    #-------------------------

    def sqrt_of(self, element):
        """Compute square roots of element of multiplicative group if modulus is prime."""
        return mod_sqrt(element, self.modulus)

    #=========================

    def order_of(self, element):
        """Compute order of element of multiplicative group."""
        if element in self.orders:
            return self.orders[element]

        if self._generator is not None:
            order = self.euler() // gcd(self.discrete_log()[element], self.euler())
            self.orders[element] = order
            return order

        elem = self.elem(element)
        powers = {1 : elem}
        for p in self.carmichael_primes():
            new_powers = {p*e : self.power_of(x, p) for e, x in powers.items() if p*e not in powers.keys()}
            try:
                order = min(e for e, x in new_powers.items() if x == 1)
                self.orders[element] = order
                return order

            except ValueError:
                powers = {**powers, **new_powers}

    #-------------------------

    def cyclic_subgroup_from(self, element):
        """Compute subgroup generated by element of multiplicative group."""
        subgroup = {0 : 1}
        curr_elem = element
        curr_power = 1
        while curr_elem != 1:
            subgroup[curr_power] = curr_elem
            curr_elem = self.mult(curr_elem, element)
            curr_power += 1

        if element not in self.orders:
            self.orders[element] = curr_power

        return subgroup

    #   TODO mod_sqrt of element, use discrete log to comput inverse, mult, power, etc
