__author__ = 'Ezequiel Medina'

from MyCorpus import *
<<<<<<< HEAD

def main():
    corpus = MyCorpus()
    lines = corpus.sents()
    n = lines.__sizeof__()

    print (corpus.sents2())
=======
from languagemodeling.ngram import NGram, NGramGenerator

def main():
    #corpus = MyCorpus()
    #lines = corpus.sents()
    #n = lines.__sizeof__()

    #print (corpus.sents2())

    sents = [
        'el gato come pescado .'.split(),
        'la gata come salmón .'.split(),
    ]
    ngram = NGram(1, sents)
    generator = NGramGenerator(ngram)
    generator.generate_sent()
>>>>>>> 1a542e885229a9b2685d37f7b7569317587c2c99


if __name__=='__main__':
    main()
