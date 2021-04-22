from test import Test
from sha import SHA
import pandas as pd
from time import perf_counter
from sys import argv
from concurrent.futures import ThreadPoolExecutor

def main():
    OUTPUTPATH = "./_data/sha_puzzle_results.csv"
    WIDTH = int(argv[1])
    DEPTH = int(argv[2])
    powtest = PoWTest(WIDTH, DEPTH)
    powtest.run()
    powtest.printResults()
    powtest.export(OUTPUTPATH)

class PoWTest():

    def __init__(self, width, depth):
        """[summary]

        Args:
            width ([int]): number of bitlengths to test. Each step in bitlength is incremented by 4, starting at 4
            depth ([int]): number of puzzles to run per bitlength
        """
        self.width = width
        self.depth = depth
        self.results = pd.DataFrame(columns=["bitlength", "puzzle", "solution", "time"])
        self.elapsed = 0

    def run(self):
        starttime = perf_counter()
        puzzles = []

        for B in range(4, (self.width*4), 4):
            for i in range(1, self.depth + 1):
                print(f"Generating Puzzle: {B},{i}")
                puzzle = SHA.generateP(B)
                # append puzzle to puzzle list
                puzzles.append({(B,i):puzzle})
        
        with ThreadPoolExecutor(max_workers=12) as exe:
            results = exe.map(SHA.PoW, puzzles)

        for item in results:
            # print(item)
            for key, value in item[0].items():
                B = key[0]
                N = key[1]
                P = value.bin
            M = item[1]
            time = item[2]

            run = {"bitlength":B, "puzzle":P, "solution":M, "time":time}
            self.results = self.results.append(run, ignore_index=True)

        self.elapsed = perf_counter() - starttime

    def printResults(self):

        print("-----Printing Results-----\n")
        print(self.results)
        print(f"-----------Puzzles Complete----------\n")
        print(f"width:{self.width}\tdepth:{self.depth}\nTotal time:{self.elapsed}")

    def export(self, _path):
        self.results.to_csv(_path)

if __name__ == "__main__":
    main()