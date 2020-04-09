import os
import pandas as pd
import sys


def grad_des(df, a):
    b_0, b_age, b_weight = 0, 0, 0
    n = df.shape[0]
    for i in range(100):
        preds = b_age * df["age"] + b_weight * df["weight"] + b_0
        b_0 -= a * ((preds - df["height"])).sum() / n
        b_age -= a * ((preds - df["height"]) * df["age"]).sum() / n
        b_weight -= a * ((preds - df["height"]) * df["weight"]).sum() / n
    return (b_0, b_age, b_weight)


if __name__ == "__main__":
    data = []
    names = ["age", "weight", "height"]
    df = pd.read_csv(sys.argv[1], names=names)
    df["intercept"] = 1
    for name in ["age", "weight"]:
        df[name] = (df[name] - df[name].mean()) / df[name].std()
    s = ""
    alphas = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10]
    alphas.append(0.075)
    for a in alphas:
        b_0, b_age, b_weight = grad_des(df, a)
        s += f"{a},100,{b_0},{b_age},{b_weight}"
        s += os.linesep
    with open(sys.argv[2], "w") as f:
        f.write(s)
