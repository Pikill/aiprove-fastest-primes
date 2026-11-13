CC      ?= gcc
CFLAGS  ?= -O3 -march=native

all: primes

primes: primes.c
	$(CC) $(CFLAGS) -o $@ $<

# Build (if needed) and run:  echo 5000000 | make run
run: primes
	./primes

verify: primes
	python3 verify.py ./primes
	python3 verify.py python3 solution.py

bench: primes
	python3 benchmark.py ./primes

clean:
	rm -f primes

.PHONY: all run verify bench clean
