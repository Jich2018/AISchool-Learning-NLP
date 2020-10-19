from enum import IntFlag
from nltk.tag import UnigramTagger
from nltk.corpus import treebank

class Operation(IntFlag):
    NONE = 0
    STOP_WORD = 1
    LOWERCASE = 2
    STEMMING = 4
    LEMMATIZATION = 8
    PUNCTUATION = 16
    HTML = 32


train_sents = treebank.tagged_sents()[:5000]
tagger = UnigramTagger(train_sents)

def tokenize(sentence: str, context: dict):
    tokenizer_name = "wordpunct"

    if "tokenizer" in context:
        tokenizer_name = context["tokenizer"]

    if tokenizer_name == "wordpunct":
        from nltk.tokenize import wordpunct_tokenize
        return wordpunct_tokenize(sentence)


def lemmatize(tokens, context: dict):
    from nltk.stem import WordNetLemmatizer
    from nltk.tag import pos_tag

    lemmatizer_name = "word_net"
    lemmatizer = WordNetLemmatizer()

    pos = pos_tag(tokens) #TODO: consider to change to sequential tagger

    if "lemmatization" in context:
        lemmatizer_name = context["lemmatization"]
        # lemmatizer =

    return [__lemmatize(lemmatizer, token, tag) for token, tag in pos]


def __lemmatize(lemmatizer, token, tag):
    '''
    http://www.nltk.org/_modules/nltk/corpus/reader/wordnet.html
    '''
    if tag.startswith("N"):
        return lemmatizer.lemmatize(token, 'n')
    elif tag.startswith("V"):
        return lemmatizer.lemmatize(token, 'v')
    elif tag.startswith("R"):
        return lemmatizer.lemmatize(token, 'r')
    elif tag.startswith("J"):
        return lemmatizer.lemmatize(token, 'a')
    else:
        return lemmatizer.lemmatize(token, 'n')


def cleanhtml(html):
    import re
    # to remove the tag and something like &nsbm
    cleanr = re.compile('</?.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    cleantext = re.sub(cleanr, '', html)
    return cleantext


def stem(tokens, context: dict):
    from nltk.stem import PorterStemmer
    stemming_name = "porter"

    stemmer = PorterStemmer()

    if "stemming" in context:
        stemming_name = context["stemming"]
        if stemming_name == 'lancaster':
            from nltk.stem import LancasterStemmer
            stemmer = LancasterStemmer()

    return [stemmer.stem(token) for token in tokens]


def remove_stop_word(tokens, context: dict):
    from nltk.corpus import stopwords

    stoplist = stopwords.words("english")

    return [token for token in tokens if token not in stoplist]


def process(sentence: str, opt: Operation, context: dict):

    if Operation.HTML in opt: #must happen before the pubctuation otherwise cannot match the correct pattern
        sentence = cleanhtml(sentence)

    if Operation.PUNCTUATION in opt: 
        import string
        sentence = sentence.translate(str.maketrans('', '', string.punctuation))

    tokens = tokenize(sentence, context)

    if Operation.LOWERCASE in opt:
        tokens = [token.lower() for token in tokens]

    if Operation.STOP_WORD in opt:
        tokens = remove_stop_word(tokens, context)

    if Operation.STEMMING in opt:
        tokens = stem(tokens, context)

    if Operation.LEMMATIZATION in opt:
        tokens = lemmatize(tokens, context)

    return tokens


if __name__ == '__main__':
    test_tokens = process("this </br > was an ate test, but a real case.", Operation.HTML | Operation.LOWERCASE | Operation.PUNCTUATION, {"stemming": "lancaster"})
    print(test_tokens)
    



