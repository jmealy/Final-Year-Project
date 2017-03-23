# gensim example.
import os
from strip_20newsgroups import strip_dataset
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import CountVectorizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora, models
import gensim


# def remove_incompatible(tokens):
#     """"""
#     tokens = [i for i in tokens if not i in en_stop]

tokenizer = RegexpTokenizer(r'\w+')

# create English stop words list
en_stop = get_stop_words('en')

# Create p_stemmer of class PorterStemmer
p_stemmer = PorterStemmer()


# create sample documents
doc_a = "Brocolli is good to eat. My brother likes to eat good brocolli, but not my mother."
doc_b = "My mother spends a lot of time driving my brother around to baseball practice."
doc_c = "Some health experts suggest that driving may cause increased tension and blood pressure."
doc_d = "I often feel pressure to perform well at school, but my mother never seems to drive my brother to do better."
doc_e = "Health professionals say that brocolli is good for your health."

# compile sample documents into a list
doc_set = [doc_a, doc_b, doc_c, doc_d, doc_e]

# list for tokenized documents in loop
texts = []
inc = []
# loop through document list
for i in doc_set:
    # clean and tokenize document string
    raw = i.lower()
    tokens = tokenizer.tokenize(raw)

    # stem tokens
    tokens = [p_stemmer.stem(i) for i in tokens]


    # remove stop words from tokens
    tokens = [i for i in tokens if not i in en_stop]

    # remove small words
    tokens = [i for i in tokens if len(i) > 2]

    # add tokens to list
    texts.append(tokens)

for i in inc:
    doc_set.remove(i)

count_vect = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
X = count_vect.fit_transform(doc_set)

# turn our tokenized documents into a id <-> term dictionary
dictionary = corpora.Dictionary(texts)

# convert tokenized documents into a document-term matrix
corpus = [dictionary.doc2bow(text) for text in texts]

# generate LDA model
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=2, id2word=dictionary, passes=20)

print(ldamodel.show_topics(num_topics=2, num_words=4))

tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

print corpus_tfidf

corpus_lda = ldamodel[corpus_tfidf]
lista = []
for item in corpus_lda:
    lista.append(item)
    print item