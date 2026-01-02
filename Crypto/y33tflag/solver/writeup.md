# CTF Writeup — Recovering 12‑byte Secret Blocks from Decimal Fraction Hints

**Challenge (summary)**
```
import mpmath as mp
mp.mp.prec = 2000
FLAG = b"XMAS{this_is_actually_an_exercise_problem_from_the_book_An-Introduction-To-Mathematical-Cryptography_by_silverman}"
FLAG += b"X" * (-len(FLAG) % 12)
secrets = [int.from_bytes(FLAG[i:i+12]) for i in range(0, len(FLAG), 12)]
print(list(map(lambda x : str(mp.mpf(x).sqrt()).split('.')[-1], secrets)))
```
The challenge prints, for each 12‑byte secret block `s`, the decimal fractional digits of `sqrt(s)` as a plain decimal string (i.e. it computes `mp.mpf(s).sqrt()`, converts to string and takes the part after the decimal point). The file `output.txt` contains the printed decimal strings which are the *hints* we use to recover each secret block.

---

## Goal
Recover each 12‑byte secret (i.e. 96‑bit integer) and reconstruct the flag. The provided solver uses lattice reduction (LLL) to recover the integer blocks from their decimal fractional parts of the square root.

---

## Key observation
Let `s` be a secret block (an integer). The code prints the fractional digits of `sqrt(s)` — call that fractional part `β` (a real number in `[0,1)`). Let `a = floor(sqrt(s))` (the integer part). Then
```
sqrt(s) = a + β
s = (a + β)^2 = a^2 + 2aβ + β^2.
```
We don't know `a` or `s` but we do know a decimal string representing `β` to high precision. Let `L` be the number of digits printed for that `β`. The hint file gives the decimal digits of `β` as a string; convert that into a rational approximation `β ≈ B / 10^L` where `B` is the integer formed by those digits. Put `mf = 10^L` so `β ≈ B/mf`.

Rewriting:
```
mf * s = mf*a^2 + mf*(2 a β) + mf*(β^2).
```
All terms on the right are (very) close to integers: `mf*s` and `mf*a^2` are integers; the other two contain `β` but after multiplication by `mf` they become integers or near-integers because `mf*β` is exactly `B` (if the printed digits were exact to L digits; numerical precision and rounding need slight care).

We can build a small lattice so that LLL returns a short vector revealing `a` and `s`. The solver constructs a basis matrix tuned to find integer relations between `1`, `2`, `t` and the scaled decimals; after LLL a short vector encodes `a` (called `alpha` in the code) and `s` can be recovered from it.

> Implementation detail: the solver uses `t = 2**48` as a scaling parameter for the third dimension. Choosing `t` large enough relative to secret magnitude helps separate the components in the lattice and helps LLL find the short relation corresponding to the true integers. For 12‑byte blocks (`< 2^96`) the empirical choice `t = 2**48` was used successfully by the author — it balances lattice shape for LLL in these parameters.

---

## The solver (explained)

We present the solver used, and then explain each step.

```python
from sage.all import matrix
import mpmath as mp
from Crypto.Util.number import long_to_bytes

mp.mp.prec = 3000
float = lambda x : mp.mpf(x)

with open('output.txt', 'r') as f :
    hints = eval(f.read())   # hints is a Python list of decimal strings (the outputs)

for beta in hints :
    lb = len(str(beta))                # number of decimal digits in the printed string
    beta = float(beta) / (10**lb)      # convert to mpf in (0,1)
    mult_factor = float(10**lb)        # mf = 10^L
    t = 2**48                          # scaling parameter for the lattice

    solve_matrix = matrix([
        (1, 0, 0, int(mult_factor)),
        (0, 2, 0, int(mult_factor * beta)),
        (0, 0, t, int(mult_factor * beta**2)),
    ])

    result_matrix = solve_matrix.LLL()
    result_row = result_matrix[0]
    alpha = result_row[1] // 4
    secret = -(result_row[0] - alpha**2)
    print(long_to_bytes(secret).decode(), end="")
print()
```

**Line‑by‑line (intuition)**

* `lb = len(str(beta))` — the printed digit string length; we use it to set `mf = 10**lb`.
* `beta = float(beta) / (10**lb)` — the fractional part as `mp.mpf` in `(0,1)`.
* `solve_matrix` — construct a 3×4 integer matrix. Each row is a lattice basis vector. The 4th column holds the large integer approximations `mf`, `mf*β`, `mf*β^2`. The diagonal entries `(1,2,t)` are scaling choices that make the lattice favor short vectors corresponding to the true integer relation. (Empirically this construction lets LLL find a vector whose components reveal `2a` and `a^2 - s` up to simple algebraic operations.)
* `result_matrix = solve_matrix.LLL()` — run LLL to produce a reduced basis. The first row typically is the short vector encoding the relation we want.
* `alpha = result_row[1] // 4` and `secret = -(result_row[0] - alpha**2)` — recover the integer `alpha` (which corresponds to `2a` or a small multiple of it depending on scaling), and compute `secret` from the relation held in the first vector. The integer arithmetic on `result_row` extracts the secret block and then `long_to_bytes(secret)` converts it back to ASCII bytes and prints it.

> The exact extraction (`// 4`, the minus signs, and squared terms) follow from the particular short vector LLL returns with the chosen basis; that vector approximately corresponds to `[ -(mf*s - mf*a^2), 4*a, something, ... ]` up to scaling in practice. The code recovers `alpha` and `s` accordingly. In short: LLL provides an integer relation between the scaled hints and small integers; the algebra shown converts that relation to `s`.

---

## Reproducing locally

1. Put the challenge `output.txt` (the printed decimal strings produced by the original program) into the same folder as the solver.
2. Make sure you have **SageMath** (for `matrix(...).LLL()`), **mpmath**, and **pycryptodome** (for `long_to_bytes`) — or adapt the solver to use any LLL implementation that you have. Using `sage` command or `sagecell` is fine.
3. Run the solver:
```
sage -python solver.py
```
(or run inside a Sage shell / environment). The solver prints the concatenated recovered secret blocks which form the flag string.

---

## Example run (expected output)

The original flag used in the challenge source was:
```
XMAS{this_is_actually_an_exercise_problem_from_the_book_An-Introduction-To-Mathematical-Cryptography_by_silverman}XXXX...
```
(where `XXXX...` are padding bytes up to a multiple of 12). The solver recovers the ASCII text of each 12‑byte block and prints the flag.

---

## Notes, pitfalls and robustness

* Precision: the original program used `mp.mp.prec = 2000` — you should use `mp.mp.prec` in the solver that is equal or larger than the decimal strings' precision. In the example solver we set `mp.mp.prec = 3000` to be safe.
* Printed digits: if the challenge truncated/rounded the fractional digits (or printed fewer digits), `mf*β` may not be exact; the lattice approach tolerates small rounding errors but if many digits are missing or the precision is low, you might need to increase the `t` parameter or adjust the basis scaling.
* Lattice parameters: the choice `t = 2**48` worked here — other problem instances might need different `t`. If LLL fails to find a short vector revealing the secret, try tuning the diagonal scales `(1,2,t)` or increasing the `mp` precision.
* If you are not using Sage, you can replace the LLL call with `fpylll` (Python) or `pycryptodome`'s `Crypto.Util.number` helpers combined with `fpylll`'s `LLL` interface. The important part is producing integer basis and calling LLL reliably.

---

## Full solver (copyable)
```python
# solver.py (requires SageMath + mpmath + pycryptodome)
from sage.all import matrix
import mpmath as mp
from Crypto.Util.number import long_to_bytes

mp.mp.prec = 3000
float = lambda x : mp.mpf(x)

with open('output.txt', 'r') as f :
    hints = eval(f.read())   # e.g. ["14159265...", "27182818...", ...]

for beta in hints :
    lb = len(str(beta))
    beta = float(beta) / (10**lb)
    mult_factor = float(10**lb)
    t = 2**48

    solve_matrix = matrix([
        (1, 0, 0, int(mult_factor)),
        (0, 2, 0, int(mult_factor * beta)),
        (0, 0, t, int(mult_factor * beta**2)),
    ])

    result_matrix = solve_matrix.LLL()
    result_row = result_matrix[0]
    alpha = result_row[1] // 4
    secret = -(result_row[0] - alpha**2)
    print(long_to_bytes(secret).decode(), end="")
print()
```

---

## Final remarks
This is a neat demonstration of using *real‑valued* side information (digits of a square root) together with lattice techniques to recover large integer secrets. The trick is converting the printed decimal fractional digits into high precision rational approximations and building an integer lattice that encodes the algebraic relations between `s`, `a`, and the known decimals. LLL then finds the short relation and lets you solve for the unknown integer.

---

*If you want, I can also produce a runnable containerized environment (Dockerfile) that installs Sage + dependencies and runs the solver automatically — tell me and I'll add it.*
