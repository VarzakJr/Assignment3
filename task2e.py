import util

def main():
    #define the ring Z_6 and its operations
    R_zero = 0
    def R_add(x, y): return (x + y) % 6
    def R_mul(x, y): return (x * y) % 6
    def R_neg(x): return (-x) % 6

    #polynomials a(x) = 3x^2 + 2x + 1 and b(x) = 4x + 5
    a = [1, 2, 3]
    b = [5, 4]

    # operations are done through util functions
    add_res = util.poly_add(a, b, R_add, R_zero)
    neg_res = util.poly_neg(a, R_neg, R_zero)
    mul_res = util.poly_mul(a, b, R_add, R_mul, R_zero)

    print("--- Task 2.e: Simulation over Ring Z_6[x] ---")
    print(f"a(x):      {a}")
    print(f"b(x):      {b}")
    print(f"a(x)+b(x): {add_res}")
    print(f"-a(x):     {neg_res}")
    print(f"a(x)*b(x): {mul_res}")

if __name__ == "__main__":
    main()