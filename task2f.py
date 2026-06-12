# task2f.py
import util

def main():
    #define operations for the field Z_5 (Field)
    F_zero = 0
    def F_add(x, y): return (x + y) % 5
    def F_mul(x, y): return (x * y) % 5
    def F_neg(x): return (-x) % 5
    def F_inv(x):
        x = x % 5
        if x == 0:
            raise ValueError("Zero has no multiplicative inverse in a field")
        for i in range(1, 5):
            if (x * i) % 5 == 1:
                return i
    #polynomials a(x) = 3x^2 + 2x + 1 and b(x) = 2x + 1
    a = [1, 2, 3]
    b = [1, 2]

    #perform division using util functions
    q, r = util.poly_div(a, b, F_add, F_mul, F_neg, F_inv, F_zero)

    print("--- Task 2.f: Simulation over Field Z_5[x] ---")
    print(f"Dividend a(x): {a}")
    print(f"Divisor b(x):  {b}")
    print(f"Quotient q(x):     {q}")
    print(f"Remainder r(x):   {r}")

if __name__ == "__main__":
    main()