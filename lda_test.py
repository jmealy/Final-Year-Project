# gensim with 20newsgroups.

import os
import gensim
from nltk.tokenize import RegexpTokenizer
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
from strip_20news_data import strip_dataset


tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()

# temp load 20news
data = fetch_20newsgroups(subset='train', remove=('headers', 'footers', 'quotes'))

# create sample documents
direc = "/home/james/PycharmProjects/final-year-project/working_data/topics_short/"
doc_set = []
for fil in os.listdir(direc):
    with file(direc + fil) as f:
        doc_set.append(f.read())

doc_set = strip_dataset(doc_set)

# list for tokenized documents in loop
texts = []

# loop through document list
for i in doc_set:
    # clean and tokenize document string
    raw = i.lower()
    tokens = tokenizer.tokenize(raw)

    # remove stop words from tokens
    tokens = [i for i in tokens if not i in en_stop]

    # stem tokens
    tokens = [p_stemmer.stem(i) for i in tokens]

    # remove small words

    # add tokens to list
    texts.append(tokens)

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)

# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=3, id2word=dictionary, passes=20)

print(ldamodel.show_topics(num_topics=3, num_words=5))

tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

print corpus_tfidf

corpus_lda = ldamodel[corpus_tfidf]
lista = []
for item in corpus_lda:
    lista.append(item)
    print item