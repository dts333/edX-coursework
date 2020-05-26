import os
import pandas as pd

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier

train_path = (
    "../resource/lib/publicdata/aclImdb/train/"  # use terminal to ls files under this directory
)
test_path = "../resource/lib/publicdata/imdb_te.csv"  # test data for grade evaluation


def imdb_data_preprocess(inpath, outpath="./", name="imdb_tr.csv", mix=False):
    pos = os.listdir(train_path + "pos/")
    neg = os.listdir(train_path + "neg/")
    df = pd.DataFrame(columns=["row number", "text", "polarity"])
    for fname in pos:
        with open(train_path + "pos/" + fname) as f:
            df = df.append({"text": f.read(), "polarity": 1}, ignore_index=True)
    for fname in neg:
        with open(train_path + "neg/" + fname) as f:
            df = df.append({"text": f.read(), "polarity": 0}, ignore_index=True)

    df.to_csv("imdb_tr.csv")
    return df


if __name__ == "__main__":
    imdb = imdb_data_preprocess(train_path)
    with open("stopwords.en.txt") as f:
        stops = f.read().split()
    unigramizer = CountVectorizer(stop_words=stops)
    bigramizer = CountVectorizer(analyzer="word", ngram_range=(2, 2), stop_words=stops)
    tfidf_unigramizer = TfidfVectorizer(stop_words=stops)
    tfidf_bigramizer = TfidfVectorizer(stop_words=stops, ngram_range=(2, 2), norm="l1")
    test = pd.read_csv(test_path, encoding="ISO-8859-1")
    trainX = unigramizer.fit_transform(imdb.text)
    testX = unigramizer.transform(test.text)
    clf = SGDClassifier(loss="hinge", penalty="l1")
    clf.fit(trainX, imdb["polarity"].astype("int"))
    preds = clf.predict(testX)
    s = ""
    for y in preds:
        s += str(y)
        s += os.linesep
    with open("unigram.output.txt", "w") as f:
        f.write(s)
    trainX = bigramizer.fit_transform(imdb.text)
    testX = bigramizer.transform(test.text)
    clf = SGDClassifier(loss="hinge", penalty="l1")
    clf.fit(trainX, imdb["polarity"].astype("int"))
    preds = clf.predict(testX)
    s = ""
    for y in preds:
        s += str(y)
        s += os.linesep
    with open("bigram.output.txt", "w") as f:
        f.write(s)
    trainX = tfidf_unigramizer.fit_transform(imdb.text)
    testX = tfidf_unigramizer.transform(test.text)
    clf = SGDClassifier(loss="hinge", penalty="l1")
    clf.fit(trainX, imdb["polarity"].astype("int"))
    preds = clf.predict(testX)
    s = ""
    for y in preds:
        s += str(y)
        s += os.linesep
    with open("unigramtfidf.output.txt", "w") as f:
        f.write(s)
    trainX = tfidf_bigramizer.fit_transform(imdb.text)
    testX = tfidf_bigramizer.transform(test.text)
    clf = SGDClassifier(loss="hinge", penalty="l1")
    clf.fit(trainX, imdb["polarity"].astype("int"))
    preds = clf.predict(testX)
    s = ""
    for y in preds:
        s += str(y)
        s += os.linesep
    with open("bigramtfidf.output.txt", "w") as f:
        f.write(s)

