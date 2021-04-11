# external imports
import sys
import os
from math import gcd as mgcd
from random import randint

# internal imports
from util import Util
from rsa import gcd as rgcd
from rsa import genKeys, getPrimes, eea
from test import Test

def testEEA():

    phin = 12
    e = 5
    n = 21
    d = eea(phin, e)
    print(d)


def testKeys():
    test = Test()
    START = 1000
    LIMIT = 10000
    pthPrime = 10
    qthPrime = 19
    p,q = getPrimes(START, LIMIT, pthPrime, qthPrime)

    for i in range(1,3):
        print(f"\nTesting key pair: {i}\n")
        keys = genKeys(p,q)

        for j in range(1,3):
            msg = randint(1, LIMIT)
            n = keys["pub"]["n"]

            ciphertext = pow(msg, keys["pub"]["e"]) % n
            dmsg = pow(ciphertext, keys["priv"]["d"]) % n

            try:
                assert dmsg == msg
                test.succ()
            except AssertionError:
                test.fail()

    test.tally()

def testGCD():
    numtests = 10000
    maxrand = 500000
    failures = 0
    successes = 0

    for i in range(1, numtests):
        a = randint(1,maxrand)
        b = randint(1,maxrand)
        print(f"\nTesting: gcd({a},{b})")
        try:
            standard = mgcd(a,b)
            mine, qs = rgcd(a,b)
            assert mine == standard
            successes += 1

        except AssertionError:
            print(f"\nFor a:{a}, b:{b}, gcd() failed.\nmath.gcd(a,b) = {standard}\nrsa.gcd(a,b) = {mine}")
            failures += 1
        
    print(f"\n\nfailures: {failures}\tsuccesses:{successes}")

def testPrimes():
    util = Util()
    print(os.getcwd())
    failures = 0
    successes = 0

    with open(util.getPath(), "r") as primes:
        for line in primes.readlines():
            # print(prime)
            prime = line.split(",")[1][1:]
            try:
                assert Util.isPrime(int(prime)) == True
                successes += 1
            except AssertionError:
                print(f"isPrime failed to detect {prime} as prime.")
                failures += 1

    print(f"\n\nfailures: {failures}\tsuccesses:{successes}")

if __name__ == "__main__":
    # testPrimes()
    # testGCD()
    # testKeys()
    testEEA()