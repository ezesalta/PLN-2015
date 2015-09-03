# https://docs.python.org/3/library/collections.html
from collections import defaultdict
from math import log

class NGram(object):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
        assert n > 0
        self.n = n
        self.counts = counts = defaultdict(int)

        for sent in sents:
            if n > 1:
                sent.insert(0,'<s>')
            sent.append('</s>')
            #print (sent)
            for i in range(len(sent) - n + 1):
                ngram = tuple(sent[i: i + n])
                counts[ngram] += 1
                counts[ngram[:-1]] += 1

    def prob(self, token, prev_tokens=None):
        n = self.n
        if not prev_tokens:
            prev_tokens = []
        assert len(prev_tokens) == n - 1

        tokens = prev_tokens + [token]
        return float(self.counts[tuple(tokens)]) / self.counts[tuple(prev_tokens)]

    def count(self, tokens):
        """Count for an n-gram or (n-1)-gram.

        tokens -- the n-gram or (n-1)-gram tuple.
        """
        #t = (tokens,)
        return self.counts[tokens]


    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.

        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        out = 1
        if self.n > 1:
            if prev_tokens == [] or prev_tokens == None:
                # It can not happen theoretically
                out = self.count( (token,) ) / float(sum(self.counts.values()))
                print ('Omg happen!')
            else:
                token_n_1 = prev_tokens[-1]
                c1 = self.count( (token_n_1,token,) )
                c2 = self.count( (token_n_1,) )
                if c2!=0:
                    out = c1/float(c2)
        else:
            out = self.count( (token,) ) / self.count(())
        return float(out)

    def sent_prob(self, sent):
        """Probability of a sentence. Warning: subject to underflow problems.

        sent -- the sentence as a list of tokens.
        """
        out = 1
        if self.n > 1:
            sent.insert(0,'<s>')
        sent.append('</s>')
        i = 0
        while i < len(sent):
            #out *= self.cond_prob(sent[i],sent[i - self.n + 1 : i])
            if sent[i] != '<s>':
                prev_tokens = sent[i - self.n + 1: i]
                out *= self.cond_prob(sent[i],prev_tokens)
            i += 1

        return out

    def sent_log_prob(self, sent):
        """Log-probability of a sentence.

        sent -- the sentence as a list of tokens.
        """
        log2 = lambda x: log(x, 2)
        out = 0
        if self.n > 1:
            sent.insert(0,'<s>')
        sent.append('</s>')
        i = 0
        while i < len(sent):
            if sent[i] != '<s>':
                prev_tokens = sent[i - self.n + 1: i]
                if self.cond_prob(sent[i], prev_tokens) > 0:
                    out += log2( self.cond_prob(sent[i], prev_tokens) )
                else:
                    # sent unseen
                    out = float('-inf')

            i += 1
        return out