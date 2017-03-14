from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import CountVectorizer

text1 = "This is the first document"
text2 = "This is document two"
dataset=[]
dataset.append(text1)
dataset.append(text2)

count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(dataset)

print count_vect.get_feature_names()

print X_train_counts.toarray()


