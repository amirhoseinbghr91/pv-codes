import galois

def is_irreducible(poly):
    """Check if a polynomial is irreducible over its field."""
    return poly.is_irreducible()

def random_irreducible(field, degree):
    """Generate a random irreducible polynomial of given degree."""
    return field.irreducible_poly(degree)
