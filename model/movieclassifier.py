import nltk
import os
import pickle
import random

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.model_selection import train_test_split



# load movie reviews and its categories
taggedreviews = []
posbasepath = "d:\\nlp\\dataset\\aclImdb\\train\\pos"
negbasepath = "d:\\nlp\\dataset\\aclImdb\\train\\neg"
unsupbasepath = "d:\\nlp\\dataset\\aclImdb\\train\\unsup"


def LoadReviews(basepath):
    print("loading reviews under "+basepath+" ...")
    reviewfiles = os.listdir(basepath)
    count = 0
    for reviewfile in reviewfiles:
        basename, ext = os.path.splitext(reviewfile)
        #print(basename)
        movieid = basename.split('_')[0]
        reviewscore= basename.split('_')[1]
        #print('review score for movie {0} is {1}'.format(movieid, reviewscore)) 
        fullfilename = os.path.join(basepath, reviewfile) 
        with open(fullfilename, 'r', encoding='utf-8') as f: 
            #print("read file ", fullfilename)
            review = f.read()
            taggedreviews.append((movieid, review, reviewscore))
            count = count + 1
        if count >6000:
               break
    print("reviews loaded.")

def cleanupwords(words) :
    mystopwords = {":", ",", ":", "{", "}", "[", "]", "\\", "\\r\\n\\", "''", ";"}
    stopset = set(stopwords.words('english')) | mystopwords
    cleanedup = [word.lower() for word in words if word not in stopset and word.isalpha()]
    return cleanedup

def getwords(review) :
    reviewwords = word_tokenize(review)
    reviewwords = cleanupwords(reviewwords)
    return reviewwords

# load reviews
LoadReviews(posbasepath)
LoadReviews(negbasepath)
print("total reviews loaded:" +str(len(taggedreviews)))

# shuffle reviews order
print("shuffle data")
random.shuffle(taggedreviews)

# prepare and process reviews, and turn them into features
allpostext = ''
allnegtext = ''
wordsfreq = []

print("prepare features")
for reviewinfo in taggedreviews :
    movieid = reviewinfo[0]
    review = reviewinfo[1]
    score = reviewinfo[2]
    #print("tokenizing word for ", movieid)
    reviewwords = getwords(review)
    #print("get word frequency")
    wordsfreq.append((nltk.FreqDist(reviewwords), score))
    if int(score) > 5:
        allpostext = allpostext + review 
    elif int(score) < 5:
        allnegtext = allnegtext + review

#calculate words frequency distribution for all positive and negative reviews
print("calculate global word frequency")
allposwordsfreq = nltk.FreqDist(getwords(allpostext))
allnegwordsfreq = nltk.FreqDist(getwords(allnegtext))

featuresets = []
print("get top words from positive and negative reviews")
topposwords = allposwordsfreq.most_common(1000)
topnegwords = allnegwordsfreq.most_common(1000)

# show most common words from positive and negative reviews
print("Top 30 words from positive reviews:")
print(topposwords[1:30])
print("Top 30 words from negative reviews:")
print(topnegwords[1:30])

print("populate feature set and result data")
for reviewwordsinfo in wordsfreq :
    wordsfreq = reviewwordsinfo[0] #words frequency distribution for a movie review
    score = reviewwordsinfo[1] #review score for a movie
    # pick top N most frequent words as feature, set correponding frequency of it in a review to be value for those features
    featuresets.append((wordsfreq, "positive" if int(score) > 5 else "negative" ))

# build ML model and measure accuracy
train_set, test_set = train_test_split(featuresets, test_size=0.3)

print("sample train set: " )
print(train_set[1:5])

classifier = nltk.NaiveBayesClassifier.train(train_set)
print("Naive Bayes accuracy: ", nltk.classify.accuracy(classifier, test_set))
classifier.show_most_informative_features(15)

#save model
with open("naivebayes_classifier.pickle", "wb") as f:
    pickle.dump(classifier, f)

#classifier1 = nltk.DecisionTreeClassifier.train(train_set)
#print("Decision tree accuracy: ",  nltk.classify.accuracy(classifier1, test_set))
#classifier1.show_most_informative_features(15)


# predict using model built
print("predict review score")
entries = os.listdir(unsupbasepath)
c = 0
for entry in entries :
    if c > 5:
        break
    c = c + 1
    with open(os.path.join(unsupbasepath, entry), 'r', encoding='utf-8') as f:
        review = f.read()
        reviewwords = getwords(review)
        print(entry + " actual prediction is " )
        wordsfreq = nltk.FreqDist(reviewwords)
        print(classifier.prob_classify(wordsfreq).max())
