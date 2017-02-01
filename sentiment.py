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
    return pipeline.fit(docs_train, y_train), dict(enumerate(dataset.target_names))


def classify(files):
    path_clf = 'classifiers/sentiment.pkl'
    path_names = 'classifiers/sentiment_groups.pkl'

    # Load classifier object and dict for mapping class names.
    # Create and save if it does not already exist.
    if os.path.isfile(path_clf) and os.path.isfile(path_names):
        with open(path_clf, 'rb') as fil:
            sentiment_clf = pickle.load(fil)
        with open(path_names, 'rb') as fil:
            target_names = pickle.load(fil)
    else:
        sentiment_clf, target_names = train()
        with open(path_clf, 'wb') as output:
            pickle.dump(sentiment_clf, output, pickle.HIGHEST_PROTOCOL)
        with open(path_names, 'wb') as output:
            pickle.dump(target_names, output, pickle.HIGHEST_PROTOCOL)

    # Use classifier to get classification values.
    predicted = sentiment_clf.predict(files)

    # Use dict with target names to get back the actual class values.
    return map(target_names.get, predicted)
