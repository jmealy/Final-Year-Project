# gensim with 20newsgroups.

import os
import gensim
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from stop_words import get_stop_words
from strip_20newsgroups import strip_dataset


def create_lda_model(name, data_path):
    """
    [tk]
    """
    documents = []
    for fil in os.listdir(data_path):
        with file(data_path + fil) as f:
            documents.append(f.read())

    # strip documents of digits, headers, etc.
    documents = strip_dataset(documents)
    # tokenizer
    tokenizer = RegexpTokenizer(r'\w+')
    # create English stop words list
    en_stop = get_stop_words('en')
    # Create p_stemmer of class PorterStemmer
    p_stemmer = PorterStemmer()
    # list for tokenized documents in loop
    tokenized_documents = []

    # loop through document list
    for i in documents:
        # clean and tokenize document string
        raw = i.lower()
        tokens = tokenizer.tokenize(raw)
        # remove stop words from tokens
        tokens = [i for i in tokens if not i in en_stop]
        # stem tokens
        tokens = [p_stemmer.stem(i) for i in tokens]
        # remove small words
        tokens = [i for i in tokens if len(i) > 2]
        # add tokens to list
        tokenized_documents.append(tokens)

    # turn our tokenized documents into a id <-> term dictionary
    dictionary = gensim.corpora.Dictionary(tokenized_documents)
    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in tokenized_documents]

    # generate LDA model
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=3, id2word=dictionary, passes=20)

    print(ldamodel.show_topics(num_topics=3, num_words=5))

    tfidf = gensim.models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    print corpus_tfidf

    topic_distributions = ldamodel[corpus_tfidf]

    topic_classifications = []
    for i in topic_distributions:
        best_topic_index = max(i, key=lambda x:x[1])[0]
        topic_classifications.append("Topic " + str(best_topic_index))

    print topic_classifications


# create sample documents
working_data = "/home/james/PycharmProjects/final-year-project/working_data/single_doc/"
create_lda_model('', working_data)