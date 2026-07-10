import galois
from typing import List, Tuple, Optional
import itertools

def list_decode(
    received: List[Tuple],
    points: List,
    h: int,
    E: galois.Poly,
    m: int,
    r: int,          # kept for API compatibility (not used)
    l: int,          # kept for API compatibility (not used)
    max_deg: int,    # degree of f (usually k-1)
    field: galois.FieldArray = None,
    tau: float = 1.0
) -> List[galois.Poly]:
    """
    Brute-force list decoder: enumerates all polynomials f of degree <= max_deg
    and keeps those that agree with the received word on at least tau fraction
    of the evaluation points.
    """
    if field is None:
        field = E.field

    n = len(points)
    min_agreements = int(tau * n) if tau < 1.0 else n
    candidates = []
    elements = list(field.elements)

    # Generate all coefficient tuples of length (max_deg+1)
    for coeffs in itertools.product(elements, repeat=max_deg+1):
        f = galois.Poly(coeffs, field=field)   # constant term first
        # Compute f_1, ..., f_{m-1}
        polys = [f]
        for _ in range(m - 1):
            polys.append((polys[-1] ** h) % E)

        # Count agreements
        agreements = 0
        for i, alpha in enumerate(points):
            symbol = tuple(poly(alpha) for poly in polys)
            if symbol == received[i]:
                agreements += 1

        if agreements >= min_agreements:
            candidates.append(f)

    # Remove duplicates (shouldn't happen, but just in case)
    unique = []
    for f in candidates:
        if f not in unique:
            unique.append(f)
    return unique
