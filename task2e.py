# util.py (polynomial ops over a ring R)

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