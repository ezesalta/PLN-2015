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

def generate(file, n):
    sents = [
        'el gato come pescado .'.split(),
        'la gata come salmón .'.split(),
    ]
    gen_sents = []
    ngram = NGram(1, sents)
    generator = NGramGenerator(ngram)
    for i in range(n):
        gen_sents.append(generator.generate_sent())

    print (gen_sents)


if __name__=='__main__':
    opts = docopt(__doc__)
    file = opts['-i']
    n = int(opts['-n'])

    generate(file, n)

