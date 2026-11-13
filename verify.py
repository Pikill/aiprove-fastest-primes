#!/usr/bin/env python3
"""Correctness check: run an implementation against known pi(N) values."""
import json, subprocess, sys

CASES = [
    (1, 0), (2, 1), (3, 2), (4, 2), (5, 3),
    (10, 4), (100, 25), (1000, 168), (100000, 9592),
    (1000000, 78498), (4999999, 348513), (5000000, 348513),  # 4999999 is itself prime
]
# also load the official public samples and merge
with open("/tmp/aiprove-spec2/challenges/fastest-primes/cases.json") as f:
    for c in json.load(f):
        if (c["n"], c["count"]) not in CASES:
            CASES.append((c["n"], c["count"]))
CASES.sort()

def run(cmd, n):
    out = subprocess.run(cmd, input=f"{n}\n", capture_output=True, text=True, timeout=120)
    if out.returncode != 0:
        raise RuntimeError(f"{cmd} failed for N={n}: {out.stderr}")
    return int(out.stdout.strip())

def main():
    cmd = sys.argv[1:]
    ok = True
    for n, expected in CASES:
        got = run(cmd, n)
        status = "OK " if got == expected else "FAIL"
        if got != expected:
            ok = False
        print(f"{status} pi({n}) = {got} (expected {expected})")
    print("ALL PASS" if ok else "FAILURES PRESENT")
    sys.exit(0 if ok else 1)

if __name__ == "__main__":
    main()
