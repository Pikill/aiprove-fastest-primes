#!/usr/bin/env python3
"""
fastest-primes — fallback implementation (pure Python, no dependencies).

Counts primes <= N (N read from stdin) with an odd-only bytearray sieve.
Composite clearing uses bytearray slice assignment, which runs at C speed;
there are no per-number Python-level loops over the sieve body.

Index i of the bytearray represents the odd number 2*i + 1. After sieving,
sum(sieve) is the number of odd primes <= N (index 0, the number 1, is
cleared up front). Adding 1 for the prime 2 gives pi(N).
"""
import sys


def prime_count(n: int) -> int:
    if n < 2:
        return 0
    size = (n + 1) // 2
    sieve = bytearray(b"\x01") * size
    sieve[0] = 0  # 1 is not prime
    limit = int(n ** 0.5)
    for p in range(3, limit + 1, 2):
        if sieve[p >> 1]:
            start = (p * p) >> 1
            step = p
            sieve[start::step] = b"\x00" * ((size - 1 - start) // step + 1)
    return sum(sieve) + 1  # odd primes + the prime 2


def main() -> None:
    data = sys.stdin.read().split()
    if not data:
        return
    print(prime_count(int(data[0])))


if __name__ == "__main__":
    main()
