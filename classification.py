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
# ------------------ Supervised classifier methods--------------------------------- #


def load_supervised_classifier(classifier_name, files):
    """ Load classifier object from classifier directory"""
    path_clf = 'classifiers/' + classifier_name + '.pkl'
    with open(path_clf, 'rb') as fil:
        classifier = pickle.load(fil)
    return classifier.get_predictions(files)


def create_supervised_classifier(classifier_name, traindata_path, files):

    #remove_sklearn_incompatible(traindata_path)

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
    remove_nltk_incompatible(data_path)
    if not num_topics:
        num_topics = 5
        print "not num_topics"

    remove_nltk_incompatible(data_path)

    documents = []
    for fil in os.listdir(data_path):
        with file(data_path + fil) as f:
            documents.append(f.read())

    # strip documents of digits, headers, etc.
    # documents = strip_dataset(documents)

    # tokenizer
    tokenizer = RegexpTokenizer(r'\w+')
    # create English stop words list
    en_stop = get_stop_words('en')
    #en_stop.append('can')

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
        # remove digits
        tokens = [x for x in tokens if not any(c.isdigit() for c in x)]
        # add tokens to list
        tokenized_documents.append(tokens)

    # turn our tokenized documents into a id <-> term dictionary
    dictionary = corpora.Dictionary(tokenized_documents)
    # convert tokenized documents into a document-term matrix
    corpus = [dictionary.doc2bow(text) for text in tokenized_documents]

    # generate LDA model
    ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics=num_topics,
                                               id2word=dictionary, passes=20)

    tfidf = gensim.models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    topic_distributions = ldamodel[corpus_tfidf]

    topic_names = []
    for i, topic in enumerate(ldamodel.show_topics(num_topics=num_topics,
                                                   num_words=5, formatted=False)):
        # extract the topic words from the list of tuples
        topic_words = [el[0] for el in topic[1]]
        topic_names.append('Topic' + str(i) + ': ' + ' '.join(topic_words))
        print topic_names

    # print(ldamodel.show_topics(num_topics=num_topics, num_words=5, formatted=False))

    topic_classifications = []
    # For each document, record the topic that best describes it.
    for i in topic_distributions:
        best_topic_index = max(i, key=lambda x:x[1])[0]
        topic_classifications.append(topic_names[best_topic_index])

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
        self.label_names = groups

    def get_predictions(self, files):
        """Returns list of predicted labels for the files"""
        # Use dict with target names to get back the actual class values.
        return map(self.get_labels(), self.cls.predict(files))

    def get_labels(self):
        """Returns a list of the categories form the training data"""
        return self.label_names.get


# MOVE TO ANOTHER MODULE
def remove_sklearn_incompatible(path):
    """
    Finds the filenames that are incompatible with `CountVectorizer`. These files are usually not compatible with UTF8!
    parameter `path` is the absolute or relative path of the training data's root directory.
    returns a list of strings.
    """
    # First get files incompatible with sklearn.
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

    # remove the incompatible files.
    for f in incompatible_files:
        print 'deleting incompatible files'
        os.remove(f)


def remove_nltk_incompatible(path):
    """
    Finds the filenames that are incompatible with `CountVectorizer`. These files are usually not compatible with UTF8!
    parameter `path` is the absolute or relative path of the training data's root directory.
    returns a list of strings.
    """
    incompatible_files = []
    # get files incompatible with nltk
    tokenizer = RegexpTokenizer(r'\w+')
    p_stemmer = PorterStemmer()
    for fil in os.listdir(path):
        with open(path + '/' + fil) as f:
            data = f.read()
        raw = data.lower()
        tokens = tokenizer.tokenize(raw)
        try:
            #tokens = p_stemmer.stem(tokens[0])
            tokens = [p_stemmer.stem(i) for i in tokens]

        except UnicodeDecodeError:
            incompatible_files.append(path + fil)

    # remove the incompatible files.
    for f in incompatible_files:
        print 'deleting incompatible files'
        os.remove(f)
