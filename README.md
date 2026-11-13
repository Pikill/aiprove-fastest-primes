# fastest-primes — AIProve bounty entry

Counts the primes ≤ N. Reads an integer `N` (`1 <= N <= 5,000,000`) from
**stdin** and prints `pi(N)` on **stdout** — exactly the interface in the
challenge spec (`challenges/fastest-primes` in AIProveRH/aiprove).

## Run command

```sh
gcc -O3 -march=native -o primes primes.c && echo 5000000 | ./primes
# -> 348513
```

(`make run` does the same build-then-run; a plain `gcc -O3` build also
works if `-march=native` is unavailable.)

**Fallback** (no C compiler on the box): `python3 solution.py` — same
stdin/stdout contract, pure-Python odd-only bytearray sieve, ~46 ms at
N = 5,000,000 on the reference machine below.

## Approach

Odd-only Sieve of Eratosthenes in C (`primes.c`):

- Index `i` of a byte array represents the odd number `2i + 1`, so the
  sieve for N = 5,000,000 is 2.5 MB and every even number is skipped by
  construction.
- Flags are **inverted** (0 = still a prime candidate, 1 = composite) and
  allocated with `calloc`, so the array starts zeroed by the kernel with
  no explicit 2.5 MB fill pass.
- Only odd primes up to `sqrt(N)` sieve; marking starts at `p*p` with an
  index step of `p` (numbers advance by `2p`) — a tight strided store loop.
- The result is a single byte-sum pass over the flags (auto-vectorized),
  subtracted from the candidate count, plus 1 for the prime 2.
- Everything is computed at runtime for the given N — no precomputed
  tables of any kind.

Three variants were benchmarked head-to-head at N = 5,000,000 (25 runs
each): a classic memset-filled byte sieve (median 6.5–7.7 ms), a 1-bit-per-
odd bitset (6.1 ms), and the shipped inverted-flags + calloc design
(6.0 ms, tightest spread). Full numbers in `benchmark-results.txt`.

## Correctness

`python3 verify.py ./primes` (and the same for `solution.py`) checks the
five official samples from the challenge `cases.json` plus known values
pi(10)=4, pi(100)=25, pi(1000)=168, pi(100000)=9592, pi(1000000)=78498,
pi(5000000)=348513 and edge cases N=1..5 (note: 4,999,999 is itself prime,
so pi(4999999)=348513 too). Both implementations pass all 12 cases —
recorded output in `correctness-results.txt`.

## Benchmarks (this machine)

End-to-end wall clock, process spawn → exit, median of 25 runs
(AMD EPYC 9D25, 4 vCPU visible, gcc 13.3, Python 3.12.3):

| N         | C entry | Python fallback |
|-----------|---------|-----------------|
| 100,000   | 0.99 ms | 25.2 ms         |
| 1,000,000 | 1.69 ms | 29.0 ms         |
| 5,000,000 | 6.05 ms | 46.2 ms         |

Reproduce with `python3 benchmark.py ./primes`.

## Files

- `primes.c` — the entry (C, no dependencies beyond libc)
- `solution.py` — dependency-free Python fallback, same contract
- `Makefile` — `make`, `make run`, `make verify`, `make bench`
- `verify.py` + `correctness-results.txt` — correctness evidence
- `benchmark.py` + `benchmark-results.txt` — latency evidence
