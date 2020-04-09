import csv
import os
import sys


class Perceptron:
    def __init__(self):
        self.w1 = 0
        self.w2 = 0
        self.b = 0

    def predict(self, x1, x2):
        val = self.w1 * x1 + self.w2 * x2 + self.b
        if val > 0:
            return 1
        else:
            return -1

    def train(self, ar):
        for example in ar:
            pred = self.predict(example[0], example[1])
            if example[2] * pred < 0:
                self.b += example[2]
                self.w1 += example[2] * example[0]
                self.w2 += example[2] * example[1]


if __name__ == "__main__":
    data = []
    with open(sys.argv[1]) as f:
        reader = csv.reader(f)
        for row in reader:
            data.append([int(i) for i in row])
    s = ""
    perceptron = Perceptron()
    for i in range(20):
        perceptron.train(data)
        s += f"{perceptron.w1},{perceptron.w2},{perceptron.b}"
        s += os.linesep
    with open(sys.argv[2], "w") as f:
        f.write(s)
