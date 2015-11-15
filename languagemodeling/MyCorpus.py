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
        self.reader = self.corpus.raw().split('.')
        self.n = len(self.reader)
        n1 = math.floor(self.n*0.9)
        # n2 = self.n-n1
        self.train = self.reader[:n1]
        self.test = self.reader[n1:]

    def sents(self):
        out = []
        tokenizer = RegexpTokenizer(self.pattern, discard_empty=True)
        for s in self.reader:
            if len(s) > 0:
                if s[0] != '#':
                    s = s[3:]
                    if s.find('[') != -1:
                        rep = re.sub('\[.+\]','',s)
                        s = rep
                    out.append(tokenizer.tokenize(s))
                    #yield tokenizer.tokenize(s)
        return out

    def sents_train(self):
        out = []
        tokenizer = RegexpTokenizer(self.pattern, discard_empty=True)
        for s in self.train:
            if len(s) > 0:
                if s[0] != '#':
                    s = s[3:]
                    if s.find('[') != -1:
                        rep = re.sub('\[.+\]','',s)
                        s = rep
                    out.append(tokenizer.tokenize(s))
        return out

    def sents_test(self):
        out = []
        tokenizer = RegexpTokenizer(self.pattern, discard_empty=True)
        for s in self.test:
            if len(s) > 0:
                if s[0] != '#':
                    s = s[3:]
                    if s.find('[') != -1:
                        rep = re.sub('\[.+\]','',s)
                        s = rep
                    out.append(tokenizer.tokenize(s))
        return out
