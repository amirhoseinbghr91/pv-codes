import galois
from pv_codes import get_field, encode

def test_encode_reed_solomon_reduction():
    # When m=1, PV reduces to standard Reed-Solomon
    GF = get_field(7)
    points = GF([1, 2, 3, 4, 5])
    E = GF.irreducible_poly(2)  # degree 2, irrelevant when m=1 but required
    f = galois.Poly([1, 2, 3], field=GF)  # 3x^2 + 2x + 1
    
    codeword = encode(f, points, h=2, E=E, m=1)
    
    # Each entry should be just (f(p),)
    for p, entry in zip(points, codeword):
        assert entry == (f(p),)
    print("test_encode_reed_solomon_reduction passed.")

if __name__ == "__main__":
    test_encode_reed_solomon_reduction()
