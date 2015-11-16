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

from languagemodeling.ngram import NGramGenerator
from docopt import docopt
import pickle


def generate(ngram, n):
    generator = NGramGenerator(ngram)
    for i in range(n):
        sent = ' '.join(generator.generate_sent())
        print('{}: {}\n'.format(i + 1, sent))

if __name__ == '__main__':
    opts = docopt(__doc__)
    file = opts['-i']
    n = int(opts['-n'])
    print('Loading model...')
    f = open(file, 'rb')
    ngram = pickle.load(f)
    f.close()
    print('Generating...')
    generate(ngram, n)
