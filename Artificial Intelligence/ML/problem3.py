import os
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

if __name__ == "__main__":
    s = ""
    methods = [
        "svm_linear",
        "svm_polynomial",
        "svm_rbf",
        "logistic",
        "knn",
        "decision_tree",
        "random_forest",
    ]
    df = pd.read_csv("input3.csv")
    train, test = train_test_split(df, train_size=0.6, stratify=df[["label"]])
    X_train, y_train = train[["A", "B"]], train[["label"]]
    X_test, y_test = test[["A", "B"]], test[["label"]]

    funcs = {
        "svm_linear": SVC(),
        "svm_polynomial": SVC(),
        "svm_rbf": SVC(),
        "logistic": LogisticRegression(),
        "knn": KNeighborsClassifier(),
        "decision_tree": DecisionTreeClassifier(),
        "random_forest": RandomForestClassifier(),
    }

    params = {
        "svm_linear": [{"kernel": ["linear"], "C": [0.1, 0.5, 1, 5, 10, 50, 100]}],
        "svm_polynomial": [
            {"kernel": ["poly"], "C": [0.1, 1, 3], "degree": [4, 5, 6], "gamma": [0.1, 0.5]}
        ],
        "svm_rbf": [
            {
                "kernel": ["rbf"],
                "C": [0.1, 0.5, 1, 5, 10, 50, 100],
                "gamma": [0.1, 0.5, 1, 3, 6, 10],
            }
        ],
        "logistic": [{"C": [0.1, 0.5, 1, 5, 10, 50, 100]}],
        "knn": [
            {
                "n_neighbors": [i + 1 for i in range(50)],
                "leaf_size": [5 * (i + 1) for i in range(12)],
            }
        ],
        "decision_tree": [
            {
                "max_depth": [i + 1 for i in range(50)],
                "min_samples_split": [i + 2 for i in range(9)],
            }
        ],
        "random_forest": [
            {
                "max_depth": [i + 1 for i in range(50)],
                "min_samples_split": [i + 2 for i in range(9)],
            }
        ],
    }
    for method in methods:
        clf = GridSearchCV(funcs[method], params[method], cv=5)
        clf.fit(X_train, y_train.values.ravel())
        s += f"{method},{clf.best_score_},{clf.score(X_test, y_test)}"
        s += os.linesep
        print(s)
    print(s)
    with open("output3.csv", "w") as f:
        f.write(s)
