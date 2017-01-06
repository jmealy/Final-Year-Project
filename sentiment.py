import sys
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV
from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
from sklearn import metrics


def train():
    """
    Create a classifier object using sentiment training data
    :return: nothing
    """
    # Load data and split to test/train
    movie_reviews_data_folder = 'training_data/txt_sentoken'
    dataset = load_files(movie_reviews_data_folder, shuffle=False)
    docs_train, docs_test, y_train, y_test = train_test_split(
        dataset.data, dataset.target, test_size=0.25, random_state=None)

    # Build a vectorizer / classifier pipeline that filters out tokens
    # that are too rare or too frequent
    pipeline = Pipeline([
        ('vect', TfidfVectorizer(min_df=3, max_df=0.95,)),
        ('clf', LinearSVC(C=1000)),
    ])

    # create classifier as a global variable for use in other function
    global sentiment_clf
    sentiment_clf= pipeline.fit(docs_train, y_train)


def classify(docs):
    predicted = sentiment_clf.predict(docs)
    return predicted
