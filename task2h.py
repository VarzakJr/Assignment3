# task2h.py
import util

#helper functions to go from polynomial to bytes and back

#takes a number between 0 and 255 and turns it into a list of 8 bits (Little-Endian)
def byte_to_poly(b):
    poly = []
    for i in range(8):
        poly.append((b >> i) & 1)   #shift right i times, then take the last bit with AND 1
    return poly

#takes a list of bits (Little-Endian) and turns it back into a number between 0 and 255
def poly_to_byte(poly):
    b = 0
    for i in range(len(poly)):  #len(poly) is always 8
        if poly[i] == 1:
            b = b | (1 << i) #turn on the i-th bit of b, 1 << i means add i zeros to the right of 1, then OR it with b to set that bit
    return b

#the main AES Sub Bytes function, applies AES S-Box to a single byte (0-255)
def sub_bytes(byte_val):
    #define the field GF(2) and the polynomial f(x) for the AES field GF(2^8)
    F_zero = 0
    F_one = 1
    def F_add(x, y): return (x + y) % 2
    def F_mul(x, y): return x * y 
    def F_neg(x): return x  #in GF(2), negation is the same as the original number (0 and 1 are their own additive inverses)
    def F_inv(x):
        if x == 1: return 1
        raise ValueError("0 has no multiplicative inverse in GF(2)")

    #the AES irreducible polynomial f(x) = x^8 + x^4 + x^3 + x + 1
    f = [1, 1, 0, 1, 1, 0, 0, 0, 1]

    #step 1: turn the input byte into a polynomial representation (list of bits)
    a = byte_to_poly(byte_val)

    # step 2: find the multiplicative inverse
    if byte_val == 0:
        #the inverse of 0 in AES is 0
        inv_poly = [] 
    else:
        inv_poly = util.poly_inv(a, f, F_add, F_mul, F_neg, F_inv, F_zero, F_one)

    #since utils trim might return a shorter list, pad it with zeros to make sure its 8 bits long
    while len(inv_poly) < 8:
        inv_poly.append(0)
    inv_poly = inv_poly[:8] 

#step 3: apply the affine transformation defined by the AES S-Box
#the constamt vector c for the affine transformation is [1, 1, 0, 0, 0, 1, 1, 0]
    c = [1, 1, 0, 0, 0, 1, 1, 0]
    
    out_poly = [0] * 8 #result of the affine transformation, initialized to all zeros

    #apply the affine transformation to each bit of the output polynomial and %2 
    for i in range(8):
        sum = (
            inv_poly[i] + 
            inv_poly[(i + 4) % 8] + 
            inv_poly[(i + 5) % 8] + 
            inv_poly[(i + 6) % 8] + 
            inv_poly[(i + 7) % 8] + 
            c[i]
        )
        out_poly[i] = sum % 2

    # step 4: convert the output polynomial back to a byte and return it
    return poly_to_byte(out_poly)

#simulation
def main():
    print("------ Task 2.h: AES SubBytes Implementation ------")
    
    # example 1: in AES, the input 0x53 (83) should produce 0xED (237)
    test_1 = 0x53
    res_1 = sub_bytes(test_1)
    print(f"Input: {hex(test_1)} -> Output (SubBytes): {hex(res_1)}")
    
    # example 2: the input 0x00 should produce 0x63 (99)
    test_2 = 0x00
    res_2 = sub_bytes(test_2)
    print(f"Input: {hex(test_2)} -> Output (SubBytes): {hex(res_2)}")

    print("--------------------------------------------")
    if res_1 == 0xED and res_2 == 0x63:
        print("S-Box works correctly")
    else:
        print("Something went wrong.")

if __name__ == "__main__":
    main()