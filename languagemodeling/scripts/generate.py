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

def generate(filename, n):
    f = open(filename, 'r')
    #data = f.readlines()
    sents = [
        'el gato come pescado .'.split(),
        'la gata come salmón .'.split(),
    ]
    corpus = MyCorpus()
    sents = corpus.sents()
    gen_sents = []
    ngram = NGram(1, sents)
    #ngram = NGram(1, data)
    generator = NGramGenerator(ngram)
    for i in range(n):
        gen_sents.append(generator.generate_sent())

    print (gen_sents)
    f.close()


if __name__=='__main__':
    opts = docopt(__doc__)
    file = opts['-i']
    n = int(opts['-n'])

    generate(file, n)

