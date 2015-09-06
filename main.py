__author__ = 'Ezequiel Medina'

from MyCorpus import *

def main():
    corpus = MyCorpus()
    lines = corpus.sents()
    n = lines.__sizeof__()

    print (corpus.sents2())


if __name__=='__main__':
    main()
