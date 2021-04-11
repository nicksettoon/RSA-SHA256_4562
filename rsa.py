from math import ceil, floor
from random import randint
from util import Util, PrimeNotFound
import re

def main():
    ## establish range for prime search
    START = 1000
    LIMIT = 10000
    pthPrime = 10
    qthPrime = 19

    try:
        p,q = getPrimes(START, LIMIT, pthPrime, qthPrime)
        n = p * q
    except PrimeNotFound:
        exit(0)
    
def enc(_msg, _key):
    return pow(_msg, _key["e"], _key["n"])

def dec(_msg, _key):
    return pow(_msg, _key["d"], _key["n"])

def eea(_phin, e):
    """Calulates inverse of e given phi(n). i.e. t in the Extended Euclidean Algorithm when gcd(phi(n),e)=1

    Args:
        _qs ([type]): [description]
        _ts ([type]): [description]
        _nthT ([type]): [description]
    """
    calcedgcd, quotients = gcd(_phin, e)

    t = [0,1]
    i = 2
    # print(f"quotients: {quotients}")

    while len(t) <= len(quotients):
        t_2 = t[i - 2]
        q_1 = quotients[i - 2]
        t_1 = t[i - 1]
        ti = t_2 - q_1*t_1
        t.append(ti)
        i += 1
    
    # print(f"ts: {t}")
    return t[i-1]

def printKeys(key):
    n = key["pub"]["n"]
    e = key["pub"]["e"]
    d = key["priv"]["d"]
    p = key["priv"]["p"]
    q = key["priv"]["q"]
    phin = (p-1)*(q-1)

    print(f"p={p}\tq={q}\tn={n}\tphi(n)={phin}\ne={e}\td={d}")
    
def genKeys(p,q):
    """Generates public private key pair using Extended Euclidean Algorithm

    Args:
        p ([int]): first prime
        q ([int]): second prime
    """
    keys = emptyKeyPair()
    phin = (p - 1)*(q - 1)
    n = p * q
    e = chooseE(phin)

    d = abs(eea(phin, e))

    keys["pub"]["n"] = n
    keys["pub"]["e"] = e

    keys["priv"]["d"] = d
    keys["priv"]["p"] = p
    keys["priv"]["q"] = q
    keys["priv"]["n"] = n

    return keys

def chooseE(_phin):
    e = None
    while e is None:
        candidate = randint(2,_phin)
        # print(f"Finding {randomi}th e for phi(n) = {_phin}")
        calcedgcd, quotients = gcd(_phin, candidate)
        if calcedgcd == 1:
            e = candidate

    return e

def gcd(_divisor, _dividend):
    """Finds the greatest common divisor of a and b. Returns quotient array as well. Wrapper for recursive implementation of Euclidean Algorithm in gcdr()

    Args:
        _divisor ([int]): number being divided
        _dividend ([int]): number being divided by

    Returns:
        gcd ([int]): gcd of _divisor and _dividend
        quotients ([list]): list of quotients found in the gcd recursion tree
    """
    quotients = []
    return gcdr(abs(_divisor), abs(_dividend), quotients)

def gcdr(_a, _b, _quotients):
    """Recursive part of gcd() for use after initial setup.

    Args:
        _a ([type]): divisor of current recursive call
        _b ([type]): dividend of current recursive call
        _quotients ([type]): running list of previous quotients in recursive tree

    Returns:
        _b ([int]): if _b is returned, it is the gcd of this recursion tree
        _quotient ([list]): list of all quotients found in the recursion tree
        otherwise recurses further down with the quotient and remainder as new _a and _b
    """
    quotient = str(_a / _b)
    regex = re.search("([\d]*)([.][\d]*)", quotient)
    # print(f"quotient: {regex.group(1)}")
    # print(f"remainder: {regex.group(2)}")
    intquotient = int(regex.group(1))
    remainder = _a % _b
    _quotients.append(intquotient)

    if remainder == 0:
        return _b, _quotients
    else:
        return gcdr(_b, remainder, _quotients)

def getPrimes(_start, _limit, _pth, _qth):
    """Function that searches a range for the p^th and q^th prime

    Args:
        _start ([int]): starting number for prime search
        _limit ([int]): ending number for prime search
        _pth ([int]): find the nth prime inbetween start and limit for p
        _qth ([int]):  find the nth prime inbetween start and limit for 
    """
    primecount = 0

    if _start > _limit:
        print(f"Please use a smaller number for start than for limit. Reversing start and limit for prime generation.")
        _start, _limit = _limit, _start

    for i in range(_start, _limit):
        if Util.isPrime(i):
            primecount += 1
            if primecount == _pth:
                p_ = i
            elif primecount == _qth:
                q_ = i

    try: # try to return p,q 
        print(f"\nPrime Selection Complete.\np={p_}\tq={q_}")
        return p_,q_
    except NameError or UnboundLocalError: # if either isn't initialized, we didn't find it
        error = f"Could not find {_pth}th or {_qth}th prime within range({_start},{_limit})."
        msg ="\n Terminating key generation.\n Please try a larger range of numbers."
        raise PrimeNotFound(msg, error)

def emptyKeyPair():
    """Simply generates empty key pair nested dictionary

    Returns:
        pair ([dict]): dict containing two nested dicts, one for the public key and one for the private key
    """

    pubKey = {"e":None, "n":None}
    privKey = {"d":None, "p":None, "q":None, "n":None}
    pair = {"pub":pubKey, "priv":privKey}

    return pair

if __name__ == "__main__":
    main()