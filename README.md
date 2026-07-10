# PV-Codes

Forward Error Correction is a digital signal processing technique used to improve data reliability. It works by adding redundant data (parity bits) to a message before it is transmitted. This redundancy allows the receiver to detect and correct errors independently, without needing to request a retransmission from the sender.

FEC is critical in environments where re-sending data is impossible or impractical, such as deep space communications, satellite links, and live streaming, where high latency or one-way communication channels exist. Parvaresh-Vardy (PV) codes are a sophisticated class of error-correcting codes specifically designed for list decoding. In traditional decoding, the system attempts to find the single most likely codeword; however, list decoding allows the receiver to output a small list of potential codewords that are all within a certain distance of the received (and potentially corrupted) signal.

The primary significance of PV codes is their ability to correct a larger number of errors than the traditional "half-the-minimum-distance" bound, allowing communication to remain reliable even under higher noise levels than previously thought possible for certain code rates.

## **1. Installation**


git clone https://github.com/amirhoseinbghr91/pv-codes.git
cd pv-codes
pip install -e .

## **2. Dependencies**

    Python ≥ 3.9
    numpy (≥ 1.24)
    galois (≥ 0.3.0) – for finite field arithmetic

These will be installed automatically when you install the package via pip.
## **3. Basic Usage**
Encoding a message
python

from pv\_codes import get\_field, encode
import galois

# Choose parameters
q = 7                     # field size (prime power)
GF = get\_field(q)
n = 5                     # number of evaluation points (codeword length)
k = 2                     # degree of message polynomial < k
h = 2                     # exponent used in PV construction
m = 2                     # number of levels (polynomials to evaluate)

# Define the irreducible polynomial E of degree k
E = GF.irreducible\_poly(k)

# Evaluation points (must be distinct elements of GF(q))
points = GF([1, 2, 3, 4, 5])

# Message polynomial (coefficients: constant term first)
f = galois.Poly([1, 2], field=GF)   # f(x) = 2x + 1

# Encode
codeword = encode(f, points, h, E, m)
print("Codeword:", codeword)

List-decoding (brute-force for small fields)
python

from pv\_codes import list\_decode

# Received word (could be corrupted)
received = codeword  # no errors, or modify some symbols

# Decode: r and l are degree bounds for interpolation (choose enough)
r = 1      # max degree in x
l = 1      # max degree in each y\_i
max\_deg = k - 1

candidates = list\_decode(
    received, points, h, E, m, r, l, max\_deg, field=GF, tau=1.0
)
print("Candidates:", candidates)

## **4. Testing the Library**
bash

# Inside the project directory (after cloning or installing)
python -m pytest tests/

# Or run a specific test file
python tests/test\_pv.py

## **5. Important Notes**

    The current decoder uses a brute-force search over all polynomials of degree ≤ max_deg. This is fine for small fields (e.g., GF(7), GF(16)) and small degrees. For larger parameters, you'll need to replace it with a more efficient algorithm (e.g., Hensel lifting or Guruswami–Sudan).
    The parameters r and l must be chosen so that the interpolation problem has a non-zero solution. A rule of thumb: the number of monomials (r+1)*(l+1)^m must be greater than the number of evaluation points n.
    The tau parameter in list_decode sets the required fraction of agreements. Use tau=1.0 for no errors, lower for list-decoding with errors.

## **6. Example: Decoding with One Error**
python

# Corrupt the last symbol
corrupted = list(codeword)
corrupted[-1] = (GF(0), GF(0))

# Decode with tau=0.8 (at least 4 agreements out of 5)
candidates = list\_decode(corrupted, points, h, E, m, r, l, max\_deg, tau=0.8)
print("Candidates with one error:", candidates)

## **7. Getting Help**

If you encounter issues:

    Check that your field size q is a prime power.
    Ensure n ≤ q (you can't have more than q distinct evaluation points).
    Increase r and/or l if interpolation fails (the error will say "Not enough monomials").
    For more details, see the docstrings in src/pv_codes/init.py and each module.
Amirhosein Bagheri
