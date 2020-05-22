import os
import pandas as pd

from sklearn.feature_extraction import CountVectorizer

train_path = (
    "../resource/lib/publicdata/aclImdb/train/"  # use terminal to ls files under this directory
)
test_path = "../resource/lib/publicdata/imdb_te.csv"  # test data for grade evaluation


def imdb_data_preprocess(inpath, outpath="./", name="imdb_tr.csv", mix=False):
    pos = os.listdir(train_path + "pos/")
    neg = os.listdir(train_path + "neg/")
    df = pd.DataFrame(columns=["text", "label"])
    with open("stopwords.en.txt") as f:
        stops = f.read().split()
    for fname in pos:
        with open(train_path + "pos/" + fname) as f:
            text = f.read()
            text = [word for word in text.split() if word not in stops]
            text = " ".join(text)
            df = df.append({"text": f.read(), "label": 1})
    for fname in neg:
        with open(train_path + "neg/" + fname) as f:
            text = f.read()
            text = [word for word in text.split() if word not in stops]
            text = " ".join(text)
            df = df.append({"text": f.read(), "label": 0})

    df.to_csv("imdb_tr.csv")


def unigramify(df):
    pass


if __name__ == "__main__":
    vectorizer = CountVectorizer()
    imdb = pd.read_csv("imdb_tr.csv", headers=["text", "polarity"])
