__author__ = 'Ezequiel Medina'

from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import RegexpTokenizer

def main():
    #print ('\n'*5)
    # Create our custom sentence tokenizer.
    #^#.|\w\d: .
    reg_exp = '\w+|[.¿?¡!;$%"]+'
    #reg_exp = '\\n$'
    my_sent_tokenizer = RegexpTokenizer(reg_exp, discard_empty=True)
    # Create the new corpus reader object.
    corpus = PlaintextCorpusReader('./CORPUS_ESP', 'ADM/ADM.txt',sent_tokenizer=my_sent_tokenizer)
    # Use the new corpus reader object.
    #print(corpus.sents())
    for s in corpus.sents():
        print (s)

if __name__=='__main__':
    main()
