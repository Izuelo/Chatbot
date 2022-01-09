import nltk
import numpy as np
from nltk.stem.porter import PorterStemmer
from nltk.tag import pos_tag
from word2number import w2n

# download when first run
# nltk.download("punkt")
# nltk.download('averaged_perceptron_tagger')

stemmer = PorterStemmer()


def tokenize(sentence):
    return nltk.word_tokenize(sentence)


def stem(word):
    return stemmer.stem(word.lower())


def bag_of_words(tokenized_sentence, all_words):
    tokenized_sentence = [stem(w) for w in tokenized_sentence]
    bag = np.zeros(len(all_words), dtype=np.float32)
    for idx, w in enumerate(all_words):
        if w in tokenized_sentence:
            bag[idx] = 1.0

    return bag


def nltk_tagger(sentence):
    nltk_tag = pos_tag([w.lower() for w in sentence])
    numbers = [w2n.word_to_num(tag) for tag, token in nltk_tag if token == "CD"]
    return numbers
# MANUAL TESTS
# tokenization
# a = "How long does shipping take?"
# print(a)
# a = tokenize(a)
# print(a)
# # stemming
# words = ["Organize", "organized", "organizing"]
# stemmed_words = [stem(w) for w in words]
# print(stemmed_words)
# # bag of words
# sentence = ["hello", "how", "are", "you"]
# words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
# bag = bag_of_words(sentence, words)
# print(bag)
