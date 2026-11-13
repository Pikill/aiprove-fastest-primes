#!/usr/bin/env python3
"""
Benchmark: end-to-end wall-clock latency (process spawn -> exit) at the
worst case N = 5,000,000, plus a couple of smaller sizes for context.
Usage: python3 benchmark.py <command...> [--runs K]
"""
import statistics
import subprocess
import sys
import time

SIZES = [100000, 1000000, 5000000]


def bench(cmd, n, runs):
    times = []
    for _ in range(runs):
        t0 = time.perf_counter()
        out = subprocess.run(cmd, input=f"{n}\n", capture_output=True, text=True, timeout=300)
        t1 = time.perf_counter()
        assert out.returncode == 0, out.stderr
        times.append((t1 - t0) * 1000.0)
    return times


def main():
    args = sys.argv[1:]
    runs = 15
    if "--runs" in args:
        i = args.index("--runs")
        runs = int(args[i + 1])
        del args[i:i + 2]
    cmd = args
    print(f"command: {' '.join(cmd)}   runs per size: {runs}")
    for n in SIZES:
        times = bench(cmd, n, runs)
        print(
            f"N={n:>8}: min {min(times):8.3f} ms | median {statistics.median(times):8.3f} ms | "
            f"mean {statistics.mean(times):8.3f} ms | max {max(times):8.3f} ms"
        )


if __name__ == "__main__":
    main()
