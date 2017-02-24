import sklearn
from sklearn.datasets import fetch_20newsgroups
from sklearn.datasets import load_files
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import os

def main():
    categories = ['misc.forsale', 'sci.crypt', 'sci.space']

    dir_path = './training_data/dataset'
    find_incompatible_files(dir_path)

    text_clf = Pipeline([('vect', CountVectorizer()),
                         ('tfidf', TfidfTransformer()),
                         ('clf', MultinomialNB()),
                         ])

    twenty_train = load_files(dir_path, shuffle=True, categories=categories, random_state=42)

    text_clf = text_clf.fit(twenty_train.data, twenty_train.target)


def find_incompatible_files(path):
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

if __name__ == '__main__':
    main()
