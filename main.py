__author__ = 'Ezequiel Medina'

from MyCorpus import *

def main():
    corpus = MyCorpus()
    #lines = corpus.sents()
    #n = lines.__sizeof__()

    print (corpus.sents2())
    """try:
        for s in corpus.sents():
            print (s)
    except IndexError:
        #print ('no hay mas elementos')
        pass"""


if __name__=='__main__':
    main()
