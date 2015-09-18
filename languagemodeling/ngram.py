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
            print('model counts:', len(model.counts))
            print('words:', len(model.words))
            for t in self.model.counts:
                if len(t) == self.model.n - 1:
                    set_probs = {}
                    for tk in tokens:
                        #if tk not in t:
                        if model.cond_prob(tk,list(t)) > 0:
                            set_probs[tk] = model.cond_prob(tk,list(t))
                    self.probs[t] = set_probs
                    self.sorted_probs[t] = sorted(list(set_probs.items()))
            print('init done')
        else:
            set_probs = {}
            for token in model.words:
                set_probs[token] = model.cond_prob(token)
            self.probs[()] = set_probs

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
        self.addone = addone
        self.sents_addone = sents.copy()
        self.addone_ngram = None

        if gamma is None:
            #p = math.floor(len(sents)*0.1)
            p = math.ceil(len(sents)*0.1)
            held_out = sents[p:].copy()
            sents = sents[:p]
            self.sents_addone = sents.copy()
            if addone and n == 1:
                self.addone_ngram = AddOneNGram(1, self.sents_addone)
            self.gamma = 1.0
            # REVISAR PORQUE NO FUNCIONA LA APROXIMACION DEL MEJOR GAMMA
            """val = float('inf')
            best_gamma = self.gamma
            for g in range(10):
                self.gamma = float(g+1)
                p = self.perplexity(held_out)
                if p < val:
                    best_gamma = float(g+1)
                    val = p
            self.gamma = best_gamma"""
            # ----------------------------------------------------------
        my_counts = defaultdict(int)
        m = 1
        while m <= n:
            if m == 1:
                sents = [x+['</s>'] for x in sents]
            elif m > 1:
                sents = [['<s>']+x for x in sents]
            for sent in sents:
                if m == n:
                    for s in sent:
                        if s not in self.words:
                            self.words.append(s)
                for i in range(len(sent) - m + 1):
                    ngram = tuple(sent[i: i + m])
                    my_counts[ngram] += 1
                    my_counts[ngram[:-1]] += 1
            #print(my_counts)
            self.counts.update(my_counts)
            my_counts.clear()
            m += 1
        if addone and self.addone_ngram is None:
            self.addone_ngram = AddOneNGram(1, self.sents_addone)
        # estimar gamma usando los datos de held-out

    def count(self, tokens):
        out = 0
        if self.n == 1 and self.addone:
            out = self.addone_ngram.count(tokens)
        else:
            if tokens in self.counts:
                out = self.counts[tokens]
        return out

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.

        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        out = 0
        if self.n == 1:
            if self.addone:
                out = self.addone_ngram.cond_prob(token, prev_tokens)
            else:
                out = self.count(tuple([token])) / float(self.count(()))
        elif self.n > 1 and prev_tokens is not None:
            for i in range(self.n):
                token_n_1 = prev_tokens + [token]
                c1 = self.count( tuple(token_n_1) )
                if len(prev_tokens) > 0 and i > 0:
                    prev_tokens.pop(0)
                c2 = self.count( tuple(prev_tokens) )
                if c2 != 0:
                    c = c1 / float(c2)
                    aux = 0.0
                    for j in range(i):
                        aux += self.lambdas[j]
                    #self.lambdas[i] = ((1.0 - aux) * c3) / float(c3 + self.gamma)
                    self.lambdas[i] = (1.0 - aux) * (c2 / float(c2 + self.gamma))
                    if i+1 == self.n:
                        self.lambdas[i] = 1 - sum([x for x in list(self.lambdas.values())[0:-1]])
                        if self.addone:
                            c = self.addone_ngram.cond_prob(token,prev_tokens)

                    out += self.lambdas[i] * c
            assert sum([x for x in self.lambdas.values()]) == 1.0
            #if sum([x for x in self.lambdas.values()]) != 1.0:
                #print(self.lambdas)
                #print(sum([x for x in self.lambdas.values()]), self.gamma)
        else:
            print('no deberia pasar')
            #out = self.count(tuple([token])) / float(self.count(()))

        return out

    def perplexity(self, test):
        out = 0
        log_prob = sum( [self.sent_log_prob(sent) for sent in test] )
        m = sum([len(x) for x in test]) + len(test)
        cross_entropy = log_prob * (-1.0 / m)
        out = 2.0 ** cross_entropy
        return out

class BackOffNGram(NGram):

    def __init__(self, n, sents, beta=None, addone=True):
        """
        Back-off NGram model with discounting as described by Michael Collins.

        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        beta -- discounting hyper-parameter (if not given, estimate using
            held-out data).
        addone -- whether to use addone smoothing (default: True).
        """
        assert n > 0
        self.n = n
        self.counts = counts = defaultdict(int)
        self.words = []
        self.beta = beta
        self.nonzero_words = {}
        self.addone = addone
        self.addone_ngram = None

        if self.beta is None:
            p = math.ceil(len(sents)*0.1)
            held_out = sents[p:]
            sents = sents[:p]
            # Falta estimar beta usando los datos de held-out
            self.beta = 0.5

        # Counts
        my_counts = defaultdict(int)
        m = 1
        while m <= n:
            if m == 1:
                sents = [x+['</s>'] for x in sents]
            elif m > 1:
                sents = [['<s>']+x for x in sents]
            for sent in sents:
                # Count ngrams
                for i in range(len(sent) - m + 1):
                    ngram = tuple(sent[i: i + m])
                    my_counts[ngram] += 1
                    my_counts[ngram[:-1]] += 1
                if m == n:
                    # Count words
                    for s in sent:
                        if s not in self.words:
                            self.words.append(s)
            #print(my_counts)
            self.counts.update(my_counts)
            my_counts.clear()
            m += 1
        #print('words:',self.words)
        for sent in sents:
            # Count non-zero words
            mm = n - 1
            tokens = self.words
            for i in range(len(sent) - mm + 1):
                ngram = tuple(sent[i: i + mm])
                words = []
                for tk in tokens:
                    #print(list(ngram),tk, self.q_ml(tk,list(ngram)))
                    if self.q_ml(tk,list(ngram)) > 0:
                        #if self.cond_prob(tk,list(ngram)) > 0:
                        words.append(tk)
                self.nonzero_words[ngram] = set(words)
        #print(self.nonzero_words)
        if addone and self.addone_ngram is None:
            self.addone_ngram = AddOneNGram(n,sents)

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.

        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        out = 0
        if self.n == 1:
            if self.addone:
                out = self.addone_ngram.cond_prob(token, prev_tokens)
            else:
                out = self.count(tuple([token])) / float(self.count(()))
                #out = self.count(tuple([token])) / float(len(self.counts))
        elif self.n > 1 and prev_tokens is not None:
            if token in self.nonzero_words:
                c_star = self.count(tuple(prev_tokens + [token])) - self.beta
                p_star = float(c_star) / self.count(tuple(prev_tokens))
                out = p_star
            else:
                if len(prev_tokens) > 0:
                    a = self.alpha(tuple(prev_tokens))
                    prev = prev_tokens.copy()
                    prev.pop(0)
                    q_d = self.cond_prob(token,prev)
                    p_katz = float(q_d) / self.denom(tuple(prev_tokens))
                    #print('q_d / denom:',q_d, self.denom(tuple(prev_tokens)), p_katz)
                    out = a * p_katz
                else:
                    # prev_tokens = []
                    #out = self.count(tuple([token])) / float(self.count(()))
                    #out = self.count(tuple([token])) / float(len(self.words))
                    #out = self.count(tuple([token])) / float(len(self.counts))
                    #print(token, prev_tokens, out)
                    print('no deberia pasar2', token, prev_tokens, out)
        else:
            print('no deberia pasar1')
            #out = self.count(tuple([token])) / float(self.count(()))
            #out = self.count(tuple([token])) / float(len(self.words))
            #out = self.count(tuple([token])) / float(len(self.counts))
            #print(token, prev_tokens, out)
            #print(token, prev_tokens, self.count(tuple([token])) , float(len(self.counts)))

        return out

    def q_ml(self, token, prev_tokens=None):
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
            #out = self.count(tuple([token])) / float(len(self.words))
            #out = self.count(tuple([token])) / float(len(self.counts))
        return out

    def A(self, tokens):
        """Set of words with counts > 0 for a k-gram with 0 < k < n.

        tokens -- the k-gram tuple.
        """
        out = None
        if tokens in self.nonzero_words:
            out = self.nonzero_words[tokens]

        return out

    def alpha(self, tokens):
        """Missing probability mass for a k-gram with 0 < k < n.

        tokens -- the k-gram tuple.
        """
        out = 0
        for w in self.nonzero_words:
            c = self.count(tuple(list(tokens) + list(w)))
            cc = self.count(tokens)
            if c > 0 and cc > 0:
                val = (c - self.beta) / float(cc)
                #val = self.count(tuple(list(tokens) + list(w))) / float(self.count(tokens))
                out += val
            elif cc <= 0:
                print('cc <= 0')
            #print(tokens, w, val)
        return 1.0 - out

    def denom(self, tokens):
        """Normalization factor for a k-gram with 0 < k < n.

        tokens -- the k-gram tuple.
        """
        out = 0
        for x in self.nonzero_words[tokens]:
            l = list(tokens)
            l.pop(0)
            out += self.cond_prob(x,l)

        return 1.0 - out