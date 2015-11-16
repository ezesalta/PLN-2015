__author__ = 'Ezequiel Medina'

from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import RegexpTokenizer
import re
import math


class MyCorpus:

    def __init__(self):
        self.sentsList = []
        self.pattern = r'''(?ix)           # set flag to allow verbose regexps
                  (sr\.|sra\.)
                  | ([A-Z]\.)+        # abbreviations, e.g. U.S.A.
                  | \w+(-\w+)*        # words with optional internal hyphens
                  | \$?\d+(\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
                  | \.\.\.            # ellipsis
                  | [][.,;"'?():-_`]  # these are separate tokens; includes ], [
                  '''
        my_sent_tokenizer = RegexpTokenizer(self.pattern, discard_empty=True)
        self.corpus = PlaintextCorpusReader('./CORPUS_ESP', 'corpus.txt',sent_tokenizer=my_sent_tokenizer)
        # self.corpus = PlaintextCorpusReader('./CORPUS_ESP', 'LAVOZ/lavoz.txt',sent_tokenizer=my_sent_tokenizer)
        self.reader = self.filter(self.corpus.raw())
        self.n = len(self.reader)
        n1 = math.floor(self.n*0.9)
        # n2 = self.n-n1
        self.train = self.reader[:n1]
        self.test = self.reader[n1:]

    def filter(self, raw):
        data = []
        tokenizer = RegexpTokenizer(self.pattern, discard_empty=True)
        for line in raw.split('\n'):
            if line != '':
                if line[0] != '#' and line[0] != '[':
                    line = line[3:]
                    loop = True
                    while loop:
                        init = line.find('[')
                        final = line.find(']')
                        if init != -1 and final != -1:
                            inter = line[init: final + 1]
                            line = line.replace(inter, '')
                        else:
                            loop = False
                    data.append(tokenizer.tokenize(line + '\n'))

        return data

    def sents_train(self):
        return self.train

    def sents_test(self):
        return self.test
