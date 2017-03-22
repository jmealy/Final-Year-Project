# gensim example.
import os
from strip_20news_data import strip_dataset
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import CountVectorizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim


def remove_incompatible(path):
    """"""
    tokenizer = RegexpTokenizer(r'\w+')
    # create English stop words list
    en_stop = get_stop_words('en')
    # Create p_stemmer of class PorterStemmer
    p_stemmer = PorterStemmer()
    incompatible_files = []

    for fil in os.listdir(path):
        with file(data_path + fil) as f:
            data = f.read()
        raw = data.lower()
        tokens = tokenizer.tokenize(raw)
        try:
            tokens = [p_stemmer.stem(i) for i in tokens]
        except UnicodeDecodeError:
            print "incompatible file found"
            incompatible_files.append(path + fil)

    for f in incompatible_files:
        print 'deleting incompatible file'
        os.remove(f)


data_path = "/home/james/PycharmProjects/final-year-project/working_data/20news_4topics/"
remove_incompatible(data_path)


