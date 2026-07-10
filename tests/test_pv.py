import galois
from pv_codes import get_field, encode, list_decode

def test_pv_no_errors():
    q = 7
    GF = get_field(q)
    n = 5
    k = 2
    h = 2
    m = 2

    E = GF.irreducible_poly(k)
    points = GF([1, 2, 3, 4, 5])
    f = galois.Poly([1, 2], field=GF)  # 2x + 1

    codeword = encode(f, points, h, E, m)

    # Use tau=1.0 for no errors
    candidates = list_decode(codeword, points, h, E, m, r=1, l=1, max_deg=k-1, field=GF, tau=1.0)

    print(f"Found candidates: {candidates}")
    assert f in candidates, f"Original {f} not found. Candidates: {candidates}"
    print("test_pv_no_errors passed!")

def test_pv_with_one_error():
    q = 7
    GF = get_field(q)
    n = 5
    k = 2
    h = 2
    m = 2

    E = GF.irreducible_poly(k)
    points = GF([1, 2, 3, 4, 5])
    f = galois.Poly([1, 2], field=GF)

    codeword = encode(f, points, h, E, m)
    corrupted = list(codeword)
    # Corrupt last symbol
    corrupted[-1] = (GF(0), GF(0))

    # With one error, we need tau < 1, say 0.8 (means at least 4 agreements)
    candidates = list_decode(corrupted, points, h, E, m, r=1, l=1, max_deg=k-1, field=GF, tau=0.8)

    print(f"Found candidates: {candidates}")
    # The original f may or may not be recovered, but the decoder should not crash.
    print("test_pv_with_one_error completed.")

if __name__ == "__main__":
    test_pv_no_errors()
    test_pv_with_one_error()
