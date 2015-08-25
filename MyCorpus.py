__author__ = 'Ezequiel Medina'

from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import RegexpTokenizer
import re

class MyCorpus:

    def __init__(self):
        self.sentsList = []
        self.reader = ''
        # Create our custom sentence tokenizer.
        reg_exp = '.+'
        my_sent_tokenizer = RegexpTokenizer(reg_exp, discard_empty=True)
        # Create the new corpus reader object.
        corpus = PlaintextCorpusReader('.', 'prueba.txt',sent_tokenizer=my_sent_tokenizer)
        # Use the new corpus reader object.
        self.reader = corpus.raw().split('\n')

    def sents(self):
        for s in self.reader:
            if s[0] != '#':
                s = s[3:]
                if s.find('[') != -1:
                    rep = re.sub('\[.+\]','',s)
                    s = rep
                reg_exp = '\w+|[.¿?¡!;$%"]+'
                tokenizer = RegexpTokenizer(reg_exp, discard_empty=True)
                yield tokenizer.tokenize(s)
