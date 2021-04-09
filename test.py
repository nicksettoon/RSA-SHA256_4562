import sys
import os
from main import Util

def testPrimes():
    util = Util()
    print(os.getcwd())

    with open(util.getPath(), "r") as primes:
        for line in primes.readlines():
            # print(prime)
            prime = line.split(",")[1][1:]
            try:
                assert Util.isPrime(int(prime)) == True
            except AssertionError:
                print(f"isPrime failed to detect {prime} as prime.")

if __name__ == "__main__":
    testPrimes()
