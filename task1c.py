# task1c.py

from util import compose_wrap, identity_wrap, inverse_wrap, random_action

def encrypt_wrap(message):
    """message is a list of elements in G (integers 0..5)."""
    keys = [random_action() for _ in message]
    ciphertext = [compose_wrap(m, k) for m, k in zip(message, keys)]
    return ciphertext, keys

def decrypt_wrap(ciphertext, keys):
    inv_keys = [inverse_wrap(k) for k in keys]
    plaintext = [compose_wrap(c, k_inv) for c, k_inv in zip(ciphertext, inv_keys)]
    return plaintext

def main():
    # Example with 100-length message
    msg = [0] * 100  # all identity actions, for testing
    c, ks = encrypt_wrap(msg)
    dec = decrypt_wrap(c, ks)
    print("Decryption correct?", dec == msg)

if __name__ == "__main__":
    main()