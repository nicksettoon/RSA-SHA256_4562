from math import ceil, floor
from random import randint
from util import Util, PrimeNotFound
import re
    
def enc(_msg, _key):
    return pow(_msg, _key["e"], _key["n"])

def dec(_msg, _key):
    return pow(_msg, _key["d"], _key["n"])

def getModInverse(_divisor, _dividend):
    """Calulates inverse of e given phi(n). i.e. t in the Extended Euclidean Algorithm when gcd(phi(n),e)=1

    Args:
        _divisor ([int]): divisor of gcd calculation
        _dividend ([int]): dividend of gcd calculation, modulus of this calculation
    """
    g, x, y = egcd(_divisor, _dividend)

    if g != 1:
        print(f"getModInverse args ({_divisor},{_dividend}) are not coprime!")
    
    return x % _dividend

def divmod(_divisor, _dividend):
    quotient = str(_dividend / _divisor)
    regex = re.search("([\d]*)([.][\d]*)", quotient)
    intquotient = int(regex.group(1))
    
    return intquotient, _dividend % _divisor

def egcd(_divisor, _dividend):
    """Finds greatest common divisor of _divisor and _dividend. Returns gcd, remainder, and quotient

    Args:
        _divisor ([type]) 
        _dividend ([type]) 
    """
    if _divisor == 0:
        return _dividend, 0, 1
    else:
        div, mod = divmod(_divisor, _dividend)
        g, x, y = egcd(mod, _divisor)
        return g, y - (div * x), x

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

    d = getModInverse(e, phin)

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
        cgcd, x, y = egcd(_phin, candidate)
        if cgcd == 1:
            e = candidate

    return e

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
    print("Don't run this file directly. Import into other modules.")