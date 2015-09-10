"""
Generate natural language sentences using a language model.

Usage:
  generate.py -i <file> -n <n>
  generate.py -h | --help

Options:
  -i <file>     Language model file.
  -n <n>        Number of sentences to generate.
  -h --help     Show this screen.
"""

__author__ = 'Ezequiel Medina'

from languagemodeling.ngram import NGram, NGramGenerator
from docopt import docopt
from MyCorpus import MyCorpus
import pickle

def generate(ngram, n):
    #sents = ['el gato come pescado .'.split(),'la gata come salmón .'.split(),]
    #corpus = MyCorpus()
    #sents = corpus.sents()

    #ngram = NGram(2, sents)
    #ngram = NGram(1, data)

    generator = NGramGenerator(ngram)
    out = [generator.generate_sent() for x in range(n)]
    print (out)


if __name__=='__main__':
    opts = docopt(__doc__)
    file = opts['-i']
    n = int(opts['-n'])
    f = open(file, 'rb')
    ngram = pickle.load(f)
    f.close()
    generate(ngram, n)

