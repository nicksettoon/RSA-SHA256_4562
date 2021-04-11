
class Test():

    def __init__(self):
        self.failures = 0
        self.successes = 0

    def fail(self):
        self.failures += 1
    
    def succ(self):
        self.successes += 1
    
    def tally(self):
        print(f"\n\nfailures: {self.failures}\nsuccesses: {self.successes}")