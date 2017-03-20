import pickle
import os.path

import gensim
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
from nltk.tokenize import RegexpTokenizer
from stop_words import get_stop_words
from nltk.stem.porter import PorterStemmer
from gensim import corpora
from strip_20news_data import strip_dataset

# ------------------ Supervised classifier methods--------------------------------- #


def load_supervised_classifier(classifier_name, files):
    """ Load classifier object from classifier directory"""
    path_clf = 'classifiers/' + classifier_name + '.pkl'
    with open(path_clf, 'rb') as fil:
        classifier = pickle.load(fil)
    return classifier.get_predictions(files)


def create_supervised_classifier(classifier_name, traindata_path, files):

    remove_incompatible_files(traindata_path)

    # Load data and split to test/train
    train_data = load_files(traindata_path, shuffle=False)
    # test variables unused. Probably a cleaner way of doing this.
    docs_train, docs_test, y_train, y_test = train_test_split(
        train_data.data, train_data.target, test_size=0.0, random_state=True)

    # Build a vectorizer / classifier pipeline that filters out tokens
    # that are too rare or too frequent
    pipeline = Pipeline([
        ('vect', TfidfVectorizer(min_df=3, max_df=0.95,)),
        ('clf', LinearSVC(C=1000)),
    ])

    # create classifier from training data and return with target names
    classifier = SupervisedClassifier(pipeline.fit(docs_train, y_train), dict(enumerate(train_data.target_names)))
    save_classifier(classifier, classifier_name)
    return classifier.get_predictions(files)

# ------------------ UnSupervised classifier methods---------------------------------#


def classify_unsupervised_lda(data_path, num_topics):
    """
    [tk]
    """

    if not num_topics:
        num_topics = 5
        print "not num_topics"

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
    dictionary = corpora.Dictionary(tokenized_documents)
    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in tokenized_documents]

    # generate LDA model
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=20)

    tfidf = gensim.models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    topic_distributions = ldamodel[corpus_tfidf]

    print(ldamodel.show_topics(num_topics=num_topics, num_words=5))

    topic_classifications = []
    for i in topic_distributions:
        best_topic_index = max(i, key=lambda x:x[1])[0]
        topic_classifications.append("Topic " + str(best_topic_index))

    return topic_classifications


def save_classifier(classifier, classifier_name):
    """ Saves a classifier to the classifiers directory using name given by user"""
    path_clf = 'classifiers/' + classifier_name + '.pkl'
    with open(path_clf, 'wb') as output:
        pickle.dump(classifier, output, pickle.HIGHEST_PROTOCOL)


# ------------------------- Classifier Classes ----------------------------------------------#

class SupervisedClassifier:
    """
    """
    def __init__(self, cls, groups):
        self.cls = cls
        self.group_names = groups

    def get_predictions(self, files):
        """Returns list of predicted labels for the files"""
        # Use dict with target names to get back the actual class values.
        return map(self.get_groups(), self.cls.predict(files))

    def get_groups(self):
        """Returns a list of the categories form the training data"""
        return self.group_names.get


# class LdaClassifier:
#     """
#     """
#     def __init__(self, model, corpus):
#         self.model = model
#         self.corpus = corpus
#
#     def get_predictions(self, files):
#         """Returns list of predicted labels for the files"""


# MOVE TO ANOTHER MODULE
def remove_incompatible_files(path):
    """
    Finds the filenames that are incompatible with `CountVectorizer`. These files are usually not compatible with UTF8!
    parameter `path` is the absolute or relative path of the training data's root directory.
    returns a list of strings.
    """

    count_vector = sklearn.feature_extraction.text.CountVectorizer()
    files = sklearn.datasets.load_files(path)
    incompatible_files = []
    for i in range(len(files.filenames)):
        try:
            count_vector.fit_transform(files.data[i:i + 1])
        except UnicodeDecodeError:
            incompatible_files.append(files.filenames[i])
        except ValueError:
            pass

    for f in incompatible_files:
        print 'deleting incompatible files'
        os.remove(f)
