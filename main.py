__author__ = 'Ezequiel Medina'

from MyCorpus import MyCorpus
from languagemodeling.ngram import NGram, NGramGenerator, AddOneNGram
import pickle
import time

def main():
    initial_time = time.time()
    #corpus = MyCorpus()
    #sents = corpus.sents()
    #sents = ['el gato come pescado .'.split(),'la gata come salmón .'.split(),]
    #ngram = NGram(3,sents)

    f = open('training/addone_2', 'rb')
    ngram = pickle.load(f)
    #final_time = time.time()
    #print('time:',final_time - initial_time)
    generator = NGramGenerator(ngram)
    #print('generator ready')
    f.close()

    #print(generator.probs)
    print (generator.generate_token(['el']))
    #print (generator.generate_sent())
    #print(generator.sorted_probs)


if __name__ == '__main__':
    main()
