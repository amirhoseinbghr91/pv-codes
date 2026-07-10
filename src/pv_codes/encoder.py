from typing import List, Tuple

def encode(
    f,                  # galois.Poly: message polynomial (degree < k)
    points: List,       # list of field elements (evaluation points)
    h: int,             # exponent
    E,                  # galois.Poly: irreducible polynomial of degree k
    m: int              # number of levels (polynomials to evaluate)
) -> List[Tuple]:
    """
    Encode a message polynomial into a Parvaresh–Vardy codeword.
    Returns: list of tuples [(f(p), f1(p), ..., f_{m-1}(p)) for p in points]
    """
    polys = [f]
    for _ in range(m - 1):
        polys.append((polys[-1] ** h) % E)
    
    codeword = []
    for p in points:
        entry = tuple(poly(p) for poly in polys)
        codeword.append(entry)
    return codeword
