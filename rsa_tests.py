# external imports
import sys
import os
from math import gcd as mgcd
from math import sqrt
from random import randint

# internal imports
from util import Util
from rsa import dec, enc, gcd as rgcd, printKeys
from rsa import genKeys, getPrimes, eea
from test import Test

def testEEA():

    phin = 72
    e = 31
    n = 91
    d = eea(phin, e)
    print(d)
    msg = randint(1, n)

    ciphertext = pow(msg, e, n)
    dmsg = pow(ciphertext, d, n)
    print(f"{msg} : {ciphertext},{dmsg}")

def testKeys():
    test = Test()
    START = 1000
    LIMIT = 10000
    pthPrime = 10
    qthPrime = 19
    keytests = 25
    msgtests = 10
    p,q = getPrimes(START, LIMIT, pthPrime, qthPrime)

    for i in range(1, keytests+1):
        print(f"\nTesting key pair: {i}")
        keys = genKeys(p,q)
        printKeys(keys)
        p = keys["priv"]["p"]
        q = keys["priv"]["q"]
        d = keys["priv"]["d"]
        e = keys["pub"]["e"]
        n = keys["pub"]["n"]
        phin = (p - 1)*(q - 1)
        cgcd1,qs = rgcd(phin, e)
        cgcd2,qs = rgcd(phin, n)

        print(f"\n1 < e < phi(n)? {(1 < e) and (e < phin)}")
        print(f"gcd(phi(n),e):{cgcd1}")
        print(f"gcd(phi(n),n):{cgcd2}\n")

        for j in range(1, msgtests+1):
            msg = randint(1, n)

            ciphertext = enc(msg, keys["pub"])
            dmsg = dec(ciphertext, keys["priv"])

            print(f"msg:{msg},ct:{ciphertext},dt:{dmsg}")

            try:
                assert dmsg == msg
                print("success")
                test.succ()
            except AssertionError:
                print("failure")
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
    testKeys()
    # testEEA()