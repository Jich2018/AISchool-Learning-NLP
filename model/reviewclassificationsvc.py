import nltk
import pickle
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


# helper functions
def cleanupwords(words) :
        mystopwords = {":", ",", ":", "{", "}", "[", "]", "\\", "\\r\\n\\", "''", ";"}
        stopset = set(stopwords.words('english')) | mystopwords
        cleanedup = [word.lower() for word in words if word not in stopset and word.isalpha()]
        return cleanedup

def getwords(review) :
        reviewwords = word_tokenize(review)
        reviewwords = cleanupwords(reviewwords)
        return reviewwords

# load presaved model
modelfile = "naivebayes_classifier.pickle"
classifier = pickle.load(open(modelfile, 'rb'))

# predict using model built
print("predict review score")
filetoclassify = input("enter the review file:")
with open(filetoclassify, 'r', encoding='utf-8') as f:
    review = f.read()
    reviewwords = getwords(review)
    print(" actual prediction is " )
    wordsfreq = nltk.FreqDist(reviewwords)
    print(classifier.prob_classify(wordsfreq).max())


