import sys
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pickle
import os.path

def train():
    """
    Create a classifier object using sentiment training data
    :return: classifier object
    """
    # Load data and split to test/train
    movie_reviews_data_folder = 'training_data/txt_sentoken'
    dataset = load_files(movie_reviews_data_folder, shuffle=False)
    # test variables unused. Probably a cleaner way of doing this.
    docs_train, docs_test, y_train, y_test = train_test_split(
        dataset.data, dataset.target, test_size=0.0, random_state=True)
    temp = docs_train[0]

    # Build a vectorizer / classifier pipeline that filters out tokens
    # that are too rare or too frequent
    pipeline = Pipeline([
        ('vect', TfidfVectorizer(min_df=3, max_df=0.95,)),
        ('clf', LinearSVC(C=1000)),
    ])

    # create classifier from training data and return with target names
    return Classifier(pipeline.fit(docs_train, y_train), dict(enumerate(dataset.target_names)))


def classify(files, classifier_name):
    """"""
    # CHECKING if classifier exists is redundant. name came from list of existing classifiers. Maybe get rid, depending.
    path_clf = 'classifiers/' + classifier_name + '.pkl'
    # Load classifier object. Create and save if it does not already exist.
    if os.path.isfile(path_clf):
        with open(path_clf, 'rb') as fil:
            sentiment_clf = pickle.load(fil)
    else:
        sentiment_clf = train()
        with open(path_clf, 'wb') as output:
            pickle.dump(sentiment_clf, output, pickle.HIGHEST_PROTOCOL)

    # Use classifier to get classification values.
    predicted = sentiment_clf.get_predictions(files)

    # Use dict with target names to get back the actual class values.
    return map(sentiment_clf.get_groups(), predicted)


class Classifier:
    def __init__(self, cls, groups):
        self.cls = cls
        self.group_names = groups

    def get_predictions(self, files):
        return self.cls.predict(files)

    def get_groups(self):
        return self.group_names.get
