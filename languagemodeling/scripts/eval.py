"""Evaulate a language model using the test set.

Usage:
  eval.py -i <file>
  eval.py -h | --help

Options:
  -i <file>     Language model file.
  -h --help     Show this screen.
"""
__author__ = 'Ezequiel Medina'
from docopt import docopt
from MyCorpus import MyCorpus
from languagemodeling.ngram import NGram, AddOneNGram
import math
import pickle


def log_probability(model, test):
    out = sum( [model.sent_log_prob(sent) for sent in test] )
    return out

def cross_entropy(model, test):
    n = len(test)
    out = log_probability(model,test) * (-1.0 / n)
    return out

def perplexity(model, test):
    out = 2.0 ** cross_entropy(model,test)
    return out

def split_corpus():
    corpus = MyCorpus()
    sents = corpus.sents()
    n = len(sents)
    n1 = math.floor(n*0.9)
    n2 = n-n1
    train = sents[0:n1]
    test = sents[n1:]
    return (train,test)

def eval(model):
    (train,test) = split_corpus()
    print(perplexity(model,test))

if __name__ == '__main__':
    opts = docopt(__doc__)

    file = opts['-i']
    f = open(file, 'rb')
    model = pickle.load(f)
    f.close()
    eval(model)
