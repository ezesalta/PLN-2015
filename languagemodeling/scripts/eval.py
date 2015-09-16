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
import pickle


def log_probability(model, test):
    out = sum( [model.sent_log_prob(sent) for sent in test] )
    return out

def cross_entropy(model, test):
    n = len(test)
    m = sum([len(x) for x in test]) + len(test)
    out = log_probability(model,test) * (-1.0 / m)
    return out

def perplexity(model, test):
    out = 2.0 ** cross_entropy(model,test)
    return out

def eval(model):
    corpus = MyCorpus()
    sents = corpus.sents_test()
    print(perplexity(model,sents))

if __name__ == '__main__':
    opts = docopt(__doc__)

    file = opts['-i']
    f = open(file, 'rb')
    model = pickle.load(f)
    f.close()
    eval(model)
