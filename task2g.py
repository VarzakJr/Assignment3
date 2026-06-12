# task2g.py
import util

def main():
    # Define the operations for the GF(2) field (Z_2)
    F_zero = 0
    F_one = 1
    
    #In GF(2), addition and subtraction are XOR (modulo 2)
    def F_add(x, y): 
        return (x + y) % 2
        
    def F_mul(x, y): 
        return (x * y) % 2
        
    def F_neg(x): 
        return x % 2  # The additive inverse of a bit is itself in GF(2)
        
    def F_inv(x):
        # In GF(2) the only non-zero element is 1, and its inverse is 1
        if x == 1:
            return 1
        raise ValueError("Zero does not have a multiplicative inverse.")

    # The irreducible polynomial f(x) = x^3 + x^2 + 1
    # representation: [1, 0, 1, 1]
    f = [1, 0, 1, 1]

    # The polynomial a(x) = x^2 + 1 for which we want the inverse
    # representation: [1, 0, 1]
    a = [1, 0, 1]

    # Call the poly_inv function from util.py
    inverse_poly = util.poly_inv(a, f, F_add, F_mul, F_neg, F_inv, F_zero, F_one)

    # Verification: (a(x) * a^-1(x)) mod f(x) should be equal to 1
    prod = util.poly_mul(a, inverse_poly, F_add, F_mul, F_zero)
    q, rem = util.poly_div(prod, f, F_add, F_mul, F_neg, F_inv, F_zero)

    print("--- Task 2.g: Multiplicative Inverse in GF(2)[x]/(x^3+x^2+1) ---")
    print(f"Irreducible f(x):  {f}")
    print(f"Polynomial a(x):   {a}")
    print(f"Inverse a^-1(x):   {inverse_poly}")
    print("-" * 60)
    print("Verification:")
    print(f"(a(x) * a^-1(x)) mod f(x) = {rem}")
    
    if rem == [F_one]:
        print("Success! The calculated inverse is correct.")
    else:
        print("Error in calculation.")

if __name__ == "__main__":
    main()