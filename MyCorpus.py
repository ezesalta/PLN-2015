__author__ = 'Ezequiel Medina'

from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import RegexpTokenizer
import re

class MyCorpus:

    def __init__(self):
        self.sentsList = []
        self.reader = ''
        self.pattern = r'''(?ix)           # set flag to allow verbose regexps
                  (sr\.|sra\.)
                  | ([A-Z]\.)+        # abbreviations, e.g. U.S.A.
                  | \w+(-\w+)*        # words with optional internal hyphens
                  | \$?\d+(\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
                  | \.\.\.            # ellipsis
                  | [][.,;"'?():-_`]  # these are separate tokens; includes ], [
                  '''
        my_sent_tokenizer = RegexpTokenizer(self.pattern, discard_empty=True)
        self.corpus = PlaintextCorpusReader('./CORPUS_ESP', 'ADM/ADM.txt',sent_tokenizer=my_sent_tokenizer)
        self.reader = self.corpus.raw().split('\n')

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


    def sents2(self):
        pattern = r'''(?ix)           # set flag to allow verbose regexps
                  (sr\.|sra\.)
                  | ([A-Z]\.)+        # abbreviations, e.g. U.S.A.
                  | \w+(-\w+)*        # words with optional internal hyphens
                  | \$?\d+(\.\d+)?%?  # currency and percentages, e.g. $12.40, 82%
                  | \.\.\.            # ellipsis
                  | [][.,;"'?():-_`]  # these are separate tokens; includes ], [
                  '''
        my_sent_tokenizer = RegexpTokenizer(pattern, discard_empty=True)
        # Create the new corpus reader object.
        corpus = PlaintextCorpusReader('./CORPUS_ESP', 'ADM/ADM.txt',sent_tokenizer=my_sent_tokenizer)
        # Use the new corpus reader object.
        return corpus.sents()