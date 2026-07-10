import galois

def get_field(q: int):
    """
    Return GF(q) field class.
    q must be a prime power (e.g., 2, 3, 4, 5, 7, 8, 9, ...).
    """
    if not galois.is_prime_power(q):
        raise ValueError(f"{q} is not a prime power")
    return galois.GF(q)
