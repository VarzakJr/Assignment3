from secrets import randbelow  # allowed by the assignment rules

# Task 1: Group Operations & Grid

# Grid dimensions for Task 1.a (wrap-around)
WIDTH = 3
HEIGHT = 2

def idx_to_disp(g):
    dx = g // HEIGHT  # 0..2
    dy = g % HEIGHT   # 0..1
    return dx, dy

def disp_to_idx(dx, dy):
    return dx * HEIGHT + dy  # 0..5

def compose_wrap(a, b):
    """Operation * for Task 1.a (wrap-around grid)."""
    ax, ay = idx_to_disp(a)
    bx, by = idx_to_disp(b)
    cx = (ax + bx) % WIDTH
    cy = (ay + by) % HEIGHT
    return disp_to_idx(cx, cy)

def identity_wrap():
    return 0  # (0,0) displacement

def inverse_wrap(a):
    """Inverse in the group of Task 1.a."""
    ax, ay = idx_to_disp(a)
    dx = (-ax) % WIDTH
    dy = (-ay) % HEIGHT
    return disp_to_idx(dx, dy)

def random_action():
    return randbelow(WIDTH * HEIGHT)  # uniform in G


# Task 2: Polynomial Arithmetic

# Task 2.e -> Basic Ring Operations
def trim(poly, R_zero):
    """Remove trailing zeros from coefficient list."""
    i = len(poly) - 1
    while i > 0 and poly[i] == R_zero:
        i -= 1
    return poly[:i+1]

def poly_add(a, b, R_add, R_zero):
    """a(x) ⊕ b(x) over ring R."""
    n = max(len(a), len(b))
    res = []
    for i in range(n):
        ai = a[i] if i < len(a) else R_zero
        bi = b[i] if i < len(b) else R_zero
        res.append(R_add(ai, bi))
    return trim(res, R_zero)

def poly_neg(a, R_neg, R_zero):
    """Additive inverse of a(x)."""
    if not a:
        return [R_zero]
    return trim([R_neg(ai) for ai in a], R_zero)

def poly_mul(a, b, R_add, R_mul, R_zero):
    """a(x) ⊙ b(x) over ring R."""
    if not a or not b:
        return [R_zero]
    res = [R_zero] * (len(a) + len(b) - 1)
    for i, ai in enumerate(a):
        for j, bj in enumerate(b):
            res[i + j] = R_add(res[i + j], R_mul(ai, bj))
    return trim(res, R_zero)

# Task 2.f -> Polynomial Division over a Field
def poly_div(a, b, F_add, F_mul, F_neg, F_inv, F_zero):
    """
    division between a(x) and b(x) over field F.
    returns thr quotient q(x) and remainder r(x) such that a(x) = q(x)*b(x) + r(x).
    """
    a = trim(a, F_zero)
    b = trim(b, F_zero)

    if not b or (len(b) == 1 and b[0] == F_zero):
        raise ZeroDivisionError("polynomial division by zero")

    q = [F_zero]
    r = list(a)

    deg_b = len(b) - 1
    largest_coeff_b_inv = F_inv(b[-1])  #b[-1] id the largest degree coefficient of b(x) and we need its inverse to perform the division

    # keep dividing as long as the remainder actually exists (not empty), 
    # its degree is at least as large as our divisors degree, 
    # and it hasnt become a zero polynomial
    while len(r) > 0 and (len(r) - 1) >= deg_b and r != [F_zero]:
        
        # get the degree and the leading coefficient (highest powers number) 
        # of the current remainder, needed to figure out the target 
        deg_r = len(r) - 1
        largest_coeff_r = r[-1]

        # calculate the coefficient and degree for the new term of our quotient
        # math equivalent (remainder's leading coeff) / (divisor's leading coeff)
        #  since we are in a field, we multiply by the inverse instead of dividing
        term_coeff = F_mul(largest_coeff_r, largest_coeff_b_inv)
        term_deg = deg_r - deg_b

        # convert this single term into a proper little-endian polynomial list
        term_poly = [F_zero] * term_deg + [term_coeff]          # e.g if we found 4x^2, we pad the lower degrees with zeros: [0, 0, 4]

        # add this term to our running total quotient 'q'.
        q = poly_add(q, term_poly, F_add, F_zero)

        # now perform the subtraction step of the long division: r = r - (term * b)
        # multiply our new term by the entire divisor polynomial 'b'
        term_times_b = poly_mul(term_poly, b, F_add, F_mul, F_zero)
        
        # we need to find the additive inverse (negative) of the result since we dont have a sutraction function
        neg_term_times_b = poly_neg(term_times_b, F_neg, F_zero)
        
        # add the negative result to the current remainder
        # this effectively cancels out the remainders highest degree
        r = poly_add(r, neg_term_times_b, F_add, F_zero)

    return trim(q, F_zero), r


#Task 2.g -> inverse of a polynomial in F[x]/f(x)
def poly_inv(a, f, F_add, F_mul, F_neg, F_inv, F_zero, F_one):
    """
    Computes the multiplicative inverse of a(x) in F[x]/f(x)
    using the Extended Euclidean Algorithm (Algorithm 4)
    """
    a = trim(a, F_zero)
    f = trim(f, F_zero)

    if not a or a == [F_zero]:
        raise ValueError("The zero polynomial does not have a multiplicative inverse.")

    # Initialization based on Algorithm 4: EXTENDED_GCD(a, b)
    # Here, r{-1} is f (the modulus) and r0 is a (the polynomial)
    r0 = list(f)  # r{-1} in Algorithm 4
    r1 = list(a)  # r0 in Algorithm 4

    # We only need to track the 'y' coefficients from Algorithm 4
    # to find the inverse of 'a' modulo 'f'
    t0 = [F_zero] # y{-1} in Algorithm 4
    t1 = [F_one]  # y0 in Algorithm 4

    # repeat until r0 = 0 (Algorithm 4)
    while len(r1) > 0 and r1 != [F_zero]:
        # divide r{-1} by r0: r{-1} = q * r0 + r
        q, rem = poly_div(r0, r1, F_add, F_mul, F_neg, F_inv, F_zero)

        # y <- y{-1} - q * y0
        q_times_t1 = poly_mul(q, t1, F_add, F_mul, F_zero)
        neg_q_times_t1 = poly_neg(q_times_t1, F_neg, F_zero)
        t_new = poly_add(t0, neg_q_times_t1, F_add, F_zero)

        # apply Lemma 1.28: (a, b) = (b, r)
        # r{-1} <- r0, r0 <- r
        # y{-1} <- y0, y0 <- y
        r0, r1 = r1, rem
        t0, t1 = t1, t_new

    # according to theorem 10.4, for F[x]/f(x) to be a field, f(x) must be irreducible
    # If f(x) is irreducible, the GCD (which is now in r0) must be a non-zero scalar
    if len(r0) != 1 or r0[0] == F_zero:
        raise ValueError("f(x) is not irreducible or a(x) is not coprime to f(x). Inverse does not exist.")

    # Normalize the result. If the GCD is a scalar 'c' other than 1,
    # we multiply the inverse polynomial by c^-1.
    scalar_inv = F_inv(r0[0])
    inv_poly = [F_mul(c, scalar_inv) for c in t0]
    
    return trim(inv_poly, F_zero)