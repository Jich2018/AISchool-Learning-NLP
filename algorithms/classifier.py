import data_clean
import os.path
from os import listdir
import pandas as pd
from nltk import tokenize
import gensim


#data loading
def read_file(f):
    with open(f, encoding="utf-8") as file:
        return file.read()

data_folder = "C:\\Users\\jich\\Data\\aclImdb_v1.tar\\aclImdb_v1\\aclImdb\\test"
neg_texts = []
pos_texts = []

neg_folder = os.path.join(data_folder, "neg")
pos_folder = os.path.join(data_folder, "pos")

neg_files = [os.path.join(neg_folder, f) for f in listdir(neg_folder)]
pos_files = [os.path.join(pos_folder, f) for f in listdir(pos_folder)]

read_file(neg_files[0])

neg_data = [read_file(file) for file in neg_files]
pos_data = [read_file(file) for file in pos_files]

neg_label = ['negative' for file in neg_files]
pos_label = ['positive' for file in pos_files]

data = []
data.extend(neg_data)
data.extend(pos_data)

label = []
label.extend(neg_label)
label.extend(pos_label)

dataframe = pd.DataFrame(
    {
        "content": data,
        "label": label
    }
)
#data clean
def train_word2vec_model(sentences, algorithm='skipgram', data_folder='C:\\Users\\jich\\Data\\model'):
    assert algorithm in ['skipgram', 'cbow']
    sg = 1 if algorithm is 'skipgram' else 0

    model = gensim.models.word2vec.Word2Vec(sentences=sentences, size=200, workers=8, window=10, min_count=5,
                                            sg=sg)

    model.init_sims(True)
    model.wv.save(os.path.join(data_folder, 'word2vec_model'))

def load_word2vec_embeddings(words, word2vec_file='C:\\Users\\jich\\Data\\model\\word2vec_model'):
    w2v = gensim.models.KeyedVectors.load(word2vec_file, mmap='r')

    print("\nEmbedding length is %d.\n" % w2v.vector_size)

    embeddings = []
    for word in words:
        if word in w2v.vocab:
            embeddings[word] = w2v[word]

    return embeddings, w2v.vector_size

print(dataframe.count)

all_sentences = []

for index, row in dataframe.iterrows():
    sentences = tokenize.sent_tokenize(row["content"])
    all_sentences.extend(sentences)

dataframe["content"] = dataframe["content"].apply(lambda d: data_clean.process(d, data_clean.Operation.STOP_WORD, {"stemming": "lancaster"}))
print(dataframe.head)
#data transform
#data model build
