"""Build a sentiment analysis / polarity model

Sentiment analysis can be casted as a binary text classification problem,
that is fitting a linear classifier on features extracted from the text
of the user messages so as to guess whether the opinion of the author is
positive or negative.

In this examples we will use a movie review dataset.

"""
# Author: Olivier Grisel <olivier.grisel@ensta.org>
# License: Simplified BSD

import sys

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
from sklearn import metrics
from classification import remove_sklearn_incompatible


def classify():

    # Load data and split to test/train
    path = '/home/james/Documents/text_analytics/data/twenty_newsgroups/20news-bydate-test'
    remove_sklearn_incompatible(path)
    dataset = load_files(path, shuffle=False)

    # Build a vectorizer / classifier pipeline that filters out tokens
    # that are too rare or too frequent
    pipeline = Pipeline([
        ('vect', TfidfVectorizer(min_df=3, max_df=0.95,)),
        # ('clf', LinearSVC(C=1000)),
        # ('clf', MultinomialNB()),
        # ('clf', Perceptron()),
        ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5, random_state=42)),
    ])
    avg = 0
    runs = 10
    for i in range(0, runs):
        docs_train, docs_test, y_train, y_test = train_test_split(
            dataset.data, dataset.target, test_size=0.25)

        # create classifier and predict
        clf = pipeline.fit(docs_train, y_train)
        y_predicted = clf.predict(docs_test)

        # mean accuracy and classification report.
        accuracy = np.mean(y_predicted == y_test)
        print i, accuracy
        avg += accuracy

    print avg/runs


if __name__ == "__main__":
    classify()
