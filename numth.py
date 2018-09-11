
#   numth/numth.py

##############################

def div(num, div, METHOD=None):
    """
    Performs division with remainder and returns the quotient and remainder.

    Keyword arguments:
    num -- any integer
    div -- any nonzero integer
    METHOD -- None (default) or SMALL (for small remainders)
    """

    if div == 0:
        raise ValueError('Attempted division by zero')
    
    if div > 0 or num == 0:
        q, r = num//div, num%div
    else:
        q, r = num//div + 1, (num%div) + abs(div)

    if (METHOD == 'SMALL') and (r > abs(div)//2):
        q += div // abs(div)
        r -= abs(div)

    return (q, r)

##############################

def euclidean_algorithm(a, b, METHOD=None):
    """
    Prints the Euclidean algorithm on two integers.

    Keyword arguments:
    a -- any integer
    b -- any nonzero integer
    METHOD -- None (default) or SMALL (for small remainders)
    """

    q, r = div(a, b, METHOD)
    print('{} = {} * {} + {}'.format(a, q, b, r))
    if r != 0:
        euclidean_algorithm(b, r, METHOD)

##############################

def gcd(a, b):
    """
    Computes the greatest common divisor.

    Keyword arguments:
    a, b -- any two integers
    """

    if (a, b) == (0, 0):
        raise ValueError('gcd(0, 0) is undefined')
    
    a_, b_ = a, b
    while b_ != 0:
        a_, b_ = b_, div(a_, b_, METHOD='SMALL')[1]
    return abs(a_)

##############################

def lcm(a, b):
    """
    Computes least common multiple.

    Keyword arguments:
    a, b -- any two nonzero integers
    """

    if a*b == 0:
        raise ValueError('lcm(_,0) is undefined')
    
    return a // gcd(a, b) * b

##############################

def bezout(a, b):
    """
    Computes integer an solution to Bezout's lemma.

    Keyword arguments:
    a_, b_ -- any two integers, not both zero

    Returns:
    x, y -- satisfying a*x + b*y == gcd(a, b)
    """

    if (a, b) == (0, 0):
        raise ValueError('gcd(0, 0) is undefined')

    if b == 0:
        if a > 0:
            return (1, 0)
        else:
            return (-1, 0)

    a_, b_ = a, b
    q, r = div(a_, b_, METHOD='SMALL')
    xx, x = 0, 1
    yy, y = 1, -q

    while r != 0:
        a_, b_ = b_, r
        q, r = div(a_, b_, METHOD='SMALL')
        xx, x = x, -q*x + xx
        yy, y = y, -q*y + yy

    if a*xx + b*yy > 0:
        return (xx, yy)
    else:
        return (-xx, -yy)
        
##############################

def padic(num, base):
    """
    Computes p-adic representation of a number.

    Keyword arguments:
    num -- any integer
    base -- any integer greater than 1

    Returns:
    exp, rest -- satisfying num == (base**exp) ** rest and rest % base != 0
    """

    if base < 2:
        raise ValueError('p-adic base must be at least 2')

    exp = 0
    rest = num
    while rest % base == 0:
        exp += 1
        rest //= base
    return (exp, rest)

##############################

def mod_inverse(num, mod):
    """
    Computes the inverse of a number relative to a modulus.

    Keyword arguments:
    num -- any integer
    mod -- any integer greater than 1

    Returns:
    inv -- satisfying (num * inv) % mod == 1
    """

    if mod < 1:
        raise ValueError('Modulus must be at least 2')
    if gcd(num, mod) != 1:
        raise ValueError('{} is not invertible modulo {}'.format(num, mod))

    return bezout(num, mod)[0] % mod

##############################

def mod_power(num, exp, mod):
    """
    Computes power of a number relative to a modulus.

    Keyword arguments:
    num -- any integer
    exp -- any integer
    mod -- any integer greater than 1

    Returns:
    (num**exp) % mod
    """
    if mod < 2:
        raise ValueError('Modulus must be at least 2')

    if exp < 0:
        return mod_power(mod_inverse(num, mod), -exp, mod)
    elif exp == 0:
        return 1
    elif exp == 1:
        return num % mod
    elif (exp % 2) == 0:
        return mod_power(num*num, exp//2, mod)
    else:
        return (num * mod_power(num*num, exp//2, mod)) % mod

##############################

def jacobi(a, b):
    """
    Computes Jacobi symbol for two odd integers.

    Keyword arguments:
    a -- any odd integer
    b -- any odd integer

    Returns:
    Jacobi ( a | b ) in [0, 1, -1]
    """

    if b % 2 == 0:
        raise ValueError(
                'Jacobi symbol ( {} | {} ) is undefined'.format(num, mod))

    if b == 1:
        return 1
    if gcd(a, b) != 1:
        return 0

    exp, a_ = padic(a % b, 2)
    if (exp % 2 == 1) and (b % 8 in [3, 5]):
        sgn = -1
    else:
        sgn = 1
    if a_ == 1:
        return sgn
    else:
        if (b % 4 != 1) and (a_ % 4 != 1):
            sgn *= -1
        return sgn * jacobi(b, a_)

##############################
















############################################################
############################################################
############################################################
############################################################
############################################################

##  testing

#############################

if __name__ == '__main__':
    from random import randint, choice
    
    ##########################
    #   test div
    for j in range(10):
        a, b = (choice([-1,1]) * randint(1,10**6) for i in range(2))
        q, r = div(a, b)
        assert( a == q*b + r )
        assert( r < abs(b) )
        q, r = div(a, b, 'SMALL')
        assert( a == q*b + r )
        assert( (r <= abs(b)//2) and (r > -abs(b)//2) )

    #########################
    #   test gcd
    for j in range(10):
        a, b = (choice([-1,1]) * randint(1,10**6) for i in range(2))
        d = gcd(a, b)
        assert( (a%d, b%d) == (0, 0) )
        assert( gcd(a//d, b//d) == 1 )

    ##########################
    #   test lcm
    for j in range(10):
        a, b = (choice([-1,1]) * randint(1,10**6) for i in range(2))
        m = lcm(a, b)
        assert( (m%a, m%b) == (0, 0) )
        assert( gcd(m//a, m//b) == 1 )

    ##########################
    #   test bezout
    for j in range(10):
        a, b = (choice([-1,1]) * randint(1,10**6) for i in range(2))
        x, y = bezout(a, b)
        d = gcd(a, b)
        assert( a*x + b*y == d )

    ##########################
    #   test padic
    for j in range(10):
        num, base = choice([-1,1])*randint(1,10**6), randint(2,10**6)
        exp, rest = padic(num, base)
        assert( num == base**exp * rest )
        assert( rest % base != 0 )

    ##########################
    #   test mod_inverse
    for j in range(10):
        num, mod = choice([-1,1])*randint(1,10**6), randint(2,10**6)
        while gcd(num, mod) != 1:
            num += 1
        inv = mod_inverse(num, mod)
        assert( inv > 0 and inv < mod )
        assert( (num * inv) % mod == 1 )

    ##########################
    #   test mod_power
    for j in range(10):
        num, exp, mod = (randint(1,10**4) for i in range(3))
        ans = mod_power(num, exp, mod)
        assert( (num**exp) % mod == ans )
        if gcd(num, mod) == 1:
            inv = mod_power(num, -exp, mod)
            assert( mod_inverse(ans, mod) == inv )

    ##########################
    #   test jacobi
    jacobi_row_15 = [0,1,1,0,1,0,0,-1,1,0,0,-1,0,-1,-1]
    assert( [jacobi(a, 15) for a in range(15)] == jacobi_row_15 )
