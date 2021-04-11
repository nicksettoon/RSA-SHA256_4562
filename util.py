import math


class PrimeNotFound(Exception):

    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors
        print(errors)

class Util():

    primePath = "./_data/P-10000.txt"

    def Util():
        pass

    def getPath(self):
        return self.primePath

    def isPrime(num):
        # print(num)
        if num <= 1: return False
        if num <= 3: return True
        if num % 2 == 0 or num % 3 == 0: return False

        for i in range(5, int(math.sqrt(num)), 6):
            if num % i == 0 or num % (i + 2) == 0:
                return False

        return True

if __name__ == "__main__":
    print("Don't run this directly pls. kthxbye")