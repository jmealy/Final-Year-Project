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


def create_classifier(classifier_name, traindata_path):
    """
    Create and save a classifier object using given name and training data
    """

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
    cls = Classifier(pipeline.fit(docs_train, y_train), dict(enumerate(train_data.target_names)))

    # save classifier to classifiers folder using name given by user
    path_clf = 'classifiers/' + classifier_name + '.pkl'
    with open(path_clf, 'wb') as output:
        pickle.dump(cls, output, pickle.HIGHEST_PROTOCOL)


def classify(files, classifier_name):
    """"""
    # CHECKING if classifier exists is redundant. name came from list of existing classifiers. Maybe get rid, depending.
    path_clf = 'classifiers/' + classifier_name + '.pkl'
    # Load classifier object. Create and save if it does not already exist.
    if os.path.isfile(path_clf):
        with open(path_clf, 'rb') as fil:
            sentiment_clf = pickle.load(fil)
    else:
        print "classifier does not exist :("

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
