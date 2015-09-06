__author__ = 'Ezequiel Medina'

from MyCorpus import *
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


if __name__=='__main__':
    main()
