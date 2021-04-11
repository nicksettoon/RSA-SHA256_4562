from test import Test

from sys import maxsize
from random import randint
from time import perf_counter
import hashlib
from bitstring import Bits, BitArray

class SHA():

    MAXB = 256

    def PoW(_puzzle):
        starttime = perf_counter()

        for M in range(0, maxsize):
            hsh = hashlib.sha256(f"{M}".encode()).digest()
            hsh = BitArray(hsh)

            if hsh.endswith(_puzzle):
                elapsed = perf_counter() - starttime
                return M, elapsed

        elapsed = perf_counter() - starttime
        return None, elapsed


    def generateP(_length):
        randmin = 1
        randmax = maxsize
        init = f"{randint(randmin, randmax)}".encode()
        initvector = hashlib.sha256(init).digest()

        try:
            return BitArray(initvector)[0:_length]
        except IndexError:
            print(f"{_length}, longer than 265bits.capping at 256 bit puzzle.")
            return BitArray(initvector)

