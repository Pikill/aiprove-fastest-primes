/*
 * fastest-primes — count primes <= N (1 <= N <= 5,000,000), N read from stdin.
 *
 * Approach: odd-only Sieve of Eratosthenes over a byte array of
 * "composite" flags with inverted semantics:
 *   - index i represents the odd number 2*i + 1 (index 0 -> 1, not prime).
 *   - flags start at 0 ("still a prime candidate") via calloc, which hands
 *     back zeroed pages without an explicit fill pass over 2.5 MB.
 *   - only odd primes are sieved; marking starts at p*p with index step p
 *     (numbers advance by 2p), a tight strided store loop.
 *   - the final count is a plain byte sum of the flags (auto-vectorized),
 *     subtracted from the candidate count, plus 1 for the prime 2.
 * No precomputed tables: the sieve is computed at runtime for the given N.
 *
 * Build: gcc -O3 -march=native -o primes primes.c   (gcc -O3 also works)
 * Run:   echo 5000000 | ./primes        -> 348513
 */
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    long n;
    if (scanf("%ld", &n) != 1) return 1;
    if (n < 2) {
        printf("0\n");
        return 0;
    }

    /* number of odd integers in [1, n] */
    long size = (n + 1) / 2;
    unsigned char *comp = (unsigned char *)calloc((size_t)size, 1);
    if (!comp) return 1;
    comp[0] = 1; /* 1 is not prime */

    long limit = 0;
    while ((limit + 1) * (limit + 1) <= n) limit++;   /* floor(sqrt(n)) */

    for (long p = 3; p <= limit; p += 2) {
        if (!comp[p >> 1]) {
            long start = (p * p) >> 1;   /* index of p*p */
            for (long j = start; j < size; j += p)
                comp[j] = 1;
        }
    }

    long marked = 0;
    for (long i = 1; i < size; i++)
        marked += comp[i];

    long count = 1 + (size - 1) - marked;   /* prime 2 + unmarked odd numbers */
    printf("%ld\n", count);
    free(comp);
    return 0;
}
