import util

#helper functions - same as task 2.h
def byte_to_poly(b):
    poly = []
    for i in range(8):
        poly.append((b >> i) & 1)
    return poly

def poly_to_byte(poly):
    b = 0
    for i in range(len(poly)):
        if poly[i] == 1:
            b = b + (1 << i)
    return b

#multiplication function for GF(2^8), multiplies two bytes in the AES field
def GF_multiply(byte_a, byte_b):

    #define the field GF(2) and the polynomial f(x) for the AES field GF(2^8)
    F_zero = 0
    
    def F_add(x, y): return (x + y) % 2
    def F_mul(x, y): return x * y
    def F_neg(x): return x    #in GF(2), negation is the same as the original number (0 and 1 are their own additive inverses)
    def F_inv(x):
        if x == 1: return 1
        raise ValueError("0 has no multiplicative inverse in GF(2)")

    #the AES irreducible polynomial f(x) = x^8 + x^4 + x^3 + x + 1
    f = [1, 1, 0, 1, 1, 0, 0, 0, 1] 

    #turn the bytes into polynomial representations (lists of bits)
    poly_a = byte_to_poly(byte_a)
    poly_b = byte_to_poly(byte_b)

    #multiply the polynomials 
    res_mul = util.poly_mul(poly_a, poly_b, F_add, F_mul, F_zero)

    #divide the result by f. Since poly_div returns [quotient, remainder], we only care about the remainder
    #which is the result of the multiplication in GF(2^8)
    _, rem = util.poly_div(res_mul, f, F_add, F_mul, F_neg, F_inv, F_zero)

    #the remainder is our answer. We convert it back to a number.t
    return poly_to_byte(rem)

#mix columns function. Takes a list of 4 bytes (a column) and applies the AES MixColumns transformation to it.
def mix_single_column(col):
        

    #addition is XOR (^)
    #the equations for the MixColumns are the result of multiplying the input column by a fixed matrix in GF(2^8)
    #1st byte is mixed with (2 * the 1st) + (3 * the 2nd) + (1 * the 3rd) + (1 * the 4th)
    r0 = GF_multiply(2, col[0]) ^ GF_multiply(3, col[1]) ^ col[2] ^ col[3]
    
    #2nd byte is mixed with (1 * the 1st) + (2 * the 2nd) + (3 * the 3rd) + (1 * the 4th)
    r1 = col[0] ^ GF_multiply(2, col[1]) ^ GF_multiply(3, col[2]) ^ col[3]
    
    #3rd byte is mixed with (1 * the 1st) + (1 * the 2nd) + (2 * the 3rd) + (3 * the 4th)
    r2 = col[0] ^ col[1] ^ GF_multiply(2, col[2]) ^ GF_multiply(3, col[3])
    
    #4th byte is mixed with (3 * the 1st) + (1 * the 2nd) + (1 * the 3rd) + (2 * the 4th   )
    r3 = GF_multiply(3, col[0]) ^ col[1] ^ col[2] ^ GF_multiply(2, col[3])
    
    return [r0, r1, r2, r3]

#simulation
def main():

    #input: D4, BF, 5D, 30
    test_col = [0xd4, 0xbf, 0x5d, 0x30]
    
    print("Initial Column:", [hex(b) for b in test_col])
    
    mixed_col = mix_single_column(test_col)
    
    # The correct output should be: 04, 66, 81, E5
    print("Mixed Column (MixColumns):", [hex(b) for b in mixed_col])

if __name__ == "__main__":
    main()