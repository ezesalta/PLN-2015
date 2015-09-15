# https://docs.python.org/3/library/collections.html
from collections import defaultdict
from math import log
import random, math


class NGram(object):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
        assert n > 0
        self.n = n
        self.counts = counts = defaultdict(int)
        self.words = []
        self.init_words = []

        for sent in sents:
            for s in sent:
                if s not in self.words:
                    self.words.append(s)
            if n > 1:
                sent.insert(0,'<s>')
            sent.append('</s>')
            #print (sent)
            for i in range(len(sent) - n + 1):
                ngram = tuple(sent[i: i + n])
                counts[ngram] += 1
                counts[ngram[:-1]] += 1
                if '<s>' in ngram:
                    self.init_words.append(tuple(sent[i+1: i+n]))
        self.words.append('</s>')

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
        out = 0
        #self.counts.has_key(tokens)
        if tokens in self.counts:
            out = self.counts[tokens]
        return out

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.

        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        out = 0
        if self.n > 1:
            assert prev_tokens != [] and prev_tokens is not None
            token_n_1 = prev_tokens + [token]
            c1 = self.count( tuple(token_n_1) )
            c2 = self.count( tuple(prev_tokens) )
            if c2 != 0:
                out = c1/float(c2)
        else:
            out = self.count( (token,) ) / self.count(())
        return float(out)

    def sent_prob(self, sent):
        """Probability of a sentence. Warning: subject to underflow problems.

        sent -- the sentence as a list of tokens.
        """
        out = 1
        sent.append('</s>')
        i = 0
        default = ['<s>']*(self.n-1)
        while i < len(sent):
            l1 = sent[:i]
            l2 = sent[i+1:]
            if len(l1) >= self.n - 1:
                #out *= self.cond_prob(sent[i],sent[i - self.n + 1 : i])
                out *= self.cond_prob(sent[i], l1[-self.n+1:])
            else:
                #print(sent[i],default)
                aux = ['<s>']*((self.n-1)-len(l1))
                out *= self.cond_prob(sent[i], aux+l1)
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
        default = ['<s>']*(self.n-1)
        i = 0
        while i < len(sent):
            if sent[i] != '<s>':
                #assert len(prev_tokens) == self.n - 1
                l1 = sent[:i]
                l2 = sent[i+1:]
                if len(l1) >= self.n - 1:
                    if self.cond_prob(sent[i], l1[-self.n+1:]) > 0:
                        out += log2(self.cond_prob(sent[i], l1[-self.n+1:]))
                    else:
                        # sent unseen
                        out = float('-inf')
                else:
                    #print(sent[i],default)
                    #out += log2(self.cond_prob(sent[i], default))
                    aux = ['<s>']*((self.n-1)-len(l1))
                    value = self.cond_prob(sent[i], aux+l1)
                    if value > 0:
                        out += log2(value)
                    else:
                        out = float('-inf')
            i += 1
        return out


class NGramGenerator:

    def __init__(self, model):
        """
        model -- n-gram model.
        """
        self.model = model
        self.probs = {}
        self.sorted_probs = {}
        if model.n > 1:
            tokens = model.words
            print('model counts:',len(self.model.counts))
            print('words:', len(self.model.words))
            for t in self.model.counts:
                if len(t) == self.model.n - 1:
                    set_probs = {}
                    for tk in tokens:
                        #if tk not in t:
                        if model.cond_prob(tk,list(t)) > 0:
                            set_probs[tk] = model.cond_prob(tk,list(t))
                    self.probs[t] = set_probs
                    self.sorted_probs[t] = sorted(list(set_probs.items()))
        else:
            set_probs = {}
            for token in model.words:
                set_probs[token] = model.cond_prob(token)
            self.probs[()] = set_probs
        """
                    exit()
            tokens = model.words
            tokens.insert(0,'<s>')
            for token in tokens:
                if token != '</s>':
                    tokens_aux = list(tokens)
                    tokens_aux.remove(token)
                    for word in tokens_aux:
                        if model.cond_prob(word,[token]) > 0:
                            set_probs[word] = model.cond_prob(word,[token])
                    self.probs[tuple([token])] = set_probs
                    self.sorted_probs[tuple([token])] = sorted(list(set_probs.items()))
                    set_probs = {}"""

    def generate_sent(self):
        """Randomly generate a sentence."""
        sent = []
        if self.model.n > 1:
            prev_tokens = ['<s>']*(self.model.n - 1)
            #prev_tokens = ['<s>']
        else:
            prev_tokens = None
        i = 0
        token = self.generate_token(prev_tokens)
        if self.model.n > 1:
            prev_tokens.pop(0)
            prev_tokens.append(token)
            #prev_tokens.pop()
            #prev_tokens.insert(0,token)
        while token != '</s>' and i < 100:
            sent.append(token)
            token = self.generate_token(prev_tokens)
            if self.model.n > 1:
                prev_tokens.pop(0)
                prev_tokens.append(token)
            i += 1
        return sent

    def generate_token(self, prev_tokens=None):
        """Randomly generate a token, given prev_tokens.


        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        token = ''
        #if self.model.n == 1:
        if self.model.n > 1 and prev_tokens is not None:
            if tuple(prev_tokens) in self.sorted_probs:
                probs = self.sorted_probs[tuple(prev_tokens)]
                if len(probs) > 0:
                    max_probs = []
                    for p in probs:
                        if p[1] >= probs[-1][1]:
                            max_probs.append(p)
                    if len(max_probs) > 1:
                        rand = random.randint(0,len(max_probs)-1)
                        selected = max_probs[rand]
                        token = selected[0]
                    elif len(max_probs) == 1:
                        token = max_probs[0][0]
                else:
                    #token = tk
                    print('random word :(')
                    rand = random.randint(0,len(self.model.words)-1)
                    token = self.model.words[rand]
            else:
                #print(prev_tokens, self.sorted_probs)
                if prev_tokens[-1] == '<s>':
                    rand = random.randint(0,len(self.model.init_words)-1)
                    selected = self.model.init_words[rand]
                    token = selected[0]
                else:
                    print('random word :(')
                    rand = random.randint(0,len(self.model.words)-1)
                    token = self.model.words[rand]
        else:
            rand = random.randint(0,len(self.model.words)-1)
            token = self.model.words[rand]

        return token


class AddOneNGram(NGram):

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.

        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        out = 0
        if self.n > 1:
            assert prev_tokens != [] and prev_tokens is not None
            token_n_1 = prev_tokens + [token]
            Ci = float(self.count( tuple(token_n_1) ))
            N = float(self.count( tuple(prev_tokens) ))
            V = float(self.V())
            #out = (Ci + 1) * (N / float(N + V))
            out = (Ci + 1) / (N + V)
        else:
            Ci = float(self.count( (token,) ))
            N = float(self.count(()))
            V = float(self.V())
            #out = ((Ci + 1) * N) / float(N + V)
            out = (Ci + 1) / (N + V)
        return out

    def V(self):
        """Size of the vocabulary.
        """
        V = len(self.words)

        return V

class InterpolatedNGram(NGram):

    def __init__(self, n, sents, gamma=None, addone=True):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        gamma -- interpolation hyper-parameter (if not given, estimate using
            held-out data).
        addone -- whether to use addone smoothing (default: True).
        """
        assert n > 0
        self.n = n
        self.counts = counts = defaultdict(int)
        self.words = []
        self.gamma = gamma
        self.lambdas = {}

        if self.gamma is None:
            #p = math.floor(len(sents)*0.1)
            p = math.ceil(len(sents)*0.1)
            sents = sents[:p]
            held_out = sents[p:]
            # Falta estimar gamma usando los datos de held-out y ponerlo en self.gamma
            self.gamma = 1.0
        if n == 1:
            # usar add-one
            #self = AddOneNGram(n,sents)
            #print('entrooooo addone')
            addone_ngram = AddOneNGram(n,sents)
            self.counts = addone_ngram.counts
            self.words = addone_ngram.words
        elif n > 1:
            my_counts = defaultdict(int)
            m = 1
            while m <= n:
                for sent in sents:
                    if m == 1:
                        for s in sent:
                            if s not in self.words:
                                self.words.append(s)
                        self.words.append('</s>')
                    if m > 1:
                        sent.insert(0,'<s>')
                    sent.append('</s>')

                    for i in range(len(sent) - m + 1):
                        ngram = tuple(sent[i: i + m])
                        my_counts[ngram] += 1
                        my_counts[ngram[:-1]] += 1
                counts.update(my_counts)
                my_counts.clear()
                m += 1

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.

        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        out = 0
        if self.n > 1 and prev_tokens is not None:
            for i in range(self.n):
                token_n_1 = prev_tokens + [token]
                c1 = self.count( tuple(token_n_1) )
                c2 = self.count( tuple(prev_tokens) )
                if len(prev_tokens) > 0 and i > 0:
                    prev_tokens.pop(0)
                c3 = self.count( tuple(prev_tokens) )
                if c2 != 0:
                    c = c1 / float(c3)
                    aux = 0.0
                    for j in range(i):
                        aux += self.lambdas[j]
                    #self.lambdas[i] = ((1.0 - aux) * c3) / float(c3 + self.gamma)
                    self.lambdas[i] = (1.0 - aux) * (c3 / float(c3 + self.gamma))
                    if i+1 == self.n:
                        #self.lambdas[i] = 1 - sum([x for x in self.lambdas.values()])
                        self.lambdas[i] = 1 - sum([x for x in list(self.lambdas.values())[0:-1]])

                    out += self.lambdas[i] * c
            assert sum([x for x in self.lambdas.values()]) == 1.0
        else:
            out = self.count( (token,) ) / self.count(())
        #print(self.lambdas)
        #print(list(self.lambdas.values())[-1], 1 - sum([x for x in list(self.lambdas.values())[0:-1]]))
        #print(sum([float(x) for x in self.lambdas.values()]))
        return out