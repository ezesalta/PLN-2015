# https://docs.python.org/3/library/collections.html
from collections import defaultdict
from math import log
import random
import math


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
        self.nonzero_words = defaultdict(set)

        for sent in sents:
            for s in sent:
                if s not in self.words:
                    self.words.append(s)
            if n > 1:
                sent.insert(0, '<s>')
            sent.append('</s>')
            for i in range(len(sent) - n + 1):
                ngram = tuple(sent[i: i + n])
                counts[ngram] += 1
                counts[ngram[:-1]] += 1
                if ngram[:-1] != ():
                    self.nonzero_words[ngram[:-1]].add(ngram[-1])
                if '<s>' in ngram:
                    self.init_words.append(tuple(sent[i+1: i+n]))
        self.words.append('</s>')
        self.nonzero_words = dict(self.nonzero_words)

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
        if tokens in self.counts:
            out = self.counts[tokens]
        return out

    def q_ml(self, token, prev_tokens=None):
        out = 0
        if prev_tokens is None:
            prev_tokens = []
        if len(prev_tokens) > 0:
            token_n_1 = prev_tokens + [token]
            c1 = self.count(tuple(token_n_1))
            c2 = self.count(tuple(prev_tokens))
            if c2 != 0:
                out = c1 / float(c2)
        else:
            out = self.count(tuple([token])) / float(self.count(()))

        return out

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.

        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        if self.n == 1:
            out = self.q_ml(token)
        elif self.n > 1:
            out = self.q_ml(token, prev_tokens)
        return out

    def sent_prob(self, sent):
        """Probability of a sentence. Warning: subject to underflow problems.

        sent -- the sentence as a list of tokens.
        """
        out = 1
        sent.append('</s>')
        i = 0
        while i < len(sent):
            l1 = sent[:i]
            if len(l1) >= self.n - 1:
                out *= self.cond_prob(sent[i], l1[-self.n+1:])
            else:
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
            sent.insert(0, '<s>')
        sent.append('</s>')
        i = 0
        while i < len(sent):
            if sent[i] != '<s>':
                l1 = sent[:i]
                if len(l1) >= self.n - 1:
                    if self.cond_prob(sent[i], l1[-self.n+1:]) > 0:
                        out += log2(self.cond_prob(sent[i], l1[-self.n+1:]))
                    else:
                        # sent unseen
                        out = float('-inf')
                        #print(sent[i], l1[-self.n+1:], self.cond_prob(sent[i], l1[-self.n+1:]))
                        #exit()
                else:
                    aux = ['<s>'] * ((self.n-1)-len(l1))
                    value = self.cond_prob(sent[i], aux+l1)
                    if value > 0:
                        out += log2(value)
                    else:
                        out = float('-inf')
            i += 1
        return out

    def perplexity(self, test):
        out = 0
        log_prob = sum([self.sent_log_prob(sent) for sent in test])
        m = sum([len(x) for x in test]) + len(test)
        cross_entropy = log_prob * (-1.0 / m)
        out = 2.0 ** cross_entropy
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
            for prev in self.model.nonzero_words:
                set_probs = {}
                for token in self.model.nonzero_words[prev]:
                    prob = model.cond_prob(token, list(prev))
                    if prob > 0:
                        set_probs[token] = model.cond_prob(token, list(prev))
                self.probs[prev] = set_probs
                self.sorted_probs[prev] = sorted(list(set_probs.items()))
        else:
            set_probs = {}
            for token in model.words:
                set_probs[token] = model.cond_prob(token)
            self.probs[()] = set_probs

    def generate_sent(self):
        """Randomly generate a sentence."""
        sent = []
        if self.model.n > 1:
            prev_tokens = ['<s>'] * (self.model.n - 1)
        else:
            prev_tokens = None
        i = 0
        token = self.generate_token(prev_tokens)
        if self.model.n > 1:
            prev_tokens.pop(0)
            prev_tokens.append(token)
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
        if self.model.n > 1 and prev_tokens is not None:
            if tuple(prev_tokens) in self.sorted_probs:
                probs = self.sorted_probs[tuple(prev_tokens)]
                if len(probs) > 0:
                    max_probs = []
                    for p in probs:
                        if p[1] >= probs[-1][1]:
                            max_probs.append(p)
                    if len(max_probs) > 1:
                        rand = random.randint(0, len(max_probs)-1)
                        selected = max_probs[rand]
                        token = selected[0]
                    elif len(max_probs) == 1:
                        token = max_probs[0][0]
                else:
                    # print('random word :(')
                    rand = random.randint(0, len(self.model.words)-1)
                    token = self.model.words[rand]
            else:
                if prev_tokens[-1] == '<s>':
                    rand = random.randint(0, len(self.model.init_words)-1)
                    selected = self.model.init_words[rand]
                    token = selected[0]
                else:
                    # print('random word :(')
                    rand = random.randint(0, len(self.model.words)-1)
                    token = self.model.words[rand]
        else:
            rand = random.randint(0, len(self.model.words)-1)
            token = self.model.words[rand]

        return token


class AddOneNGram(NGram):

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.

        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        out = 0
        if prev_tokens is None:
            prev_tokens = []
        if self.n > 1 and len(prev_tokens) > 0:
            token_n_1 = prev_tokens + [token]
            Ci = float(self.count(tuple(token_n_1)))
            N = float(self.count(tuple(prev_tokens)))
            V = float(self.V())
            # out = (Ci + 1) * (N / float(N + V))
            out = (Ci + 1) / (N + V)
        else:
            Ci = float(self.count((token,)))
            N = float(self.count(()))
            V = float(self.V())
            # out = ((Ci + 1) * N) / float(N + V)
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
        self.counts = defaultdict(int)
        self.words = []
        self.lambdas = {}
        self.addone = addone
        self.sents_addone = sents.copy()
        self.addone_ngram = None
        self.nonzero_words = defaultdict(set)

        if gamma is not None:
            self.gamma = gamma
        if gamma is None:
            # Split sents
            p = math.floor(len(sents) * 0.9)
            held_out = sents[p:].copy()
            sents = sents[:p]
            self.sents_addone = sents.copy()
            if addone and self.addone_ngram is None:
                self.addone_ngram = AddOneNGram(1, self.sents_addone)
            # Calculate gamma
            self.gamma = self.calculate_gamma(held_out)
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
                    if m == n and ngram[:-1] != ():
                        self.nonzero_words[ngram[:-1]].add(ngram[-1])
            self.counts.update(my_counts)
            my_counts.clear()
            m += 1
        self.nonzero_words = dict(self.nonzero_words)
        if addone and self.addone_ngram is None:
            self.addone_ngram = AddOneNGram(1, self.sents_addone)

    def calculate_gamma(self, held_out):
        best_gamma = 1.0
        val = float('inf')
        for g in range(50):
            self.gamma = float(g+1)
            p = self.perplexity(held_out)
            if p < val:
                best_gamma = float(g+1)
                val = p
        return best_gamma

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
        if prev_tokens is None:
            prev_tokens = []
        out = 0
        if self.n == 1:
            if self.addone:
                out = self.addone_ngram.cond_prob(token, prev_tokens)
            else:
                out = self.q_ml(token)
        elif self.n > 1 and len(prev_tokens) > 0:
            for i in range(self.n):
                c = 0
                c1 = self.count(tuple(prev_tokens + [token]))
                c2 = self.count(tuple(prev_tokens))
                if len(prev_tokens) > 0 and i > 0:
                    prev_tokens.pop(0)
                if c2 != 0:
                    c = c1 / float(c2)
                sum_lambdas = 0.0
                for j in range(i):
                    sum_lambdas += self.lambdas[j]
                self.lambdas[i] = (1.0 - sum_lambdas) * (c2 / float(c2 + self.gamma))
                if i+1 == self.n:
                    self.lambdas[i] = 1.0 - sum([x for x in list(self.lambdas.values())[0:-1]])
                    if self.addone:
                        c = self.addone_ngram.cond_prob(token, prev_tokens)
                    else:
                        c = self.q_ml(token)
                out += self.lambdas[i] * c

        if self.n > 1 and len(prev_tokens) > 0:
            assert sum([x for x in self.lambdas.values()]) == 1.0

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
        self.counts = defaultdict(int)
        self.words = []
        self.nonzero_words = defaultdict(set)
        #self.nonzero_words = {}
        self.alpha_dict = {}
        self.denom_dict = {}
        self.addone = addone
        self.addone_ngram = None
        self.sents_addone = []

        if beta is not None:
            self.beta = beta
        elif beta is None:
            p = math.floor(len(sents) * 0.9)
            held_out = sents[p:]
            sents = sents[:p]
            self.sents_addone = sents.copy()
            if addone and self.addone_ngram is None:
                self.addone_ngram = AddOneNGram(1, self.sents_addone)
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
                    if ngram[:-1] != ():
                        self.nonzero_words[ngram[:-1]].add(ngram[-1])
                if m == n:
                    # Count words
                    for s in sent:
                        if s not in self.words:
                            self.words.append(s)
            self.counts.update(my_counts)
            my_counts.clear()
            m += 1
        # Add empty set for eol
        self.nonzero_words[('</s>',)] = set()
        self.nonzero_words = dict(self.nonzero_words)
        if beta is None:
            self.beta = self.calculate_beta(held_out)
        if addone and self.addone_ngram is None:
            self.addone_ngram = AddOneNGram(1, sents)

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.

        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        out = 0
        if prev_tokens is None:
            prev_tokens = []
        if self.n == 1:
            if self.addone:
                out = self.addone_ngram.cond_prob(token, prev_tokens)
            else:
                out = self.q_ml(token)
        elif self.n > 1:
            A = self.A(tuple(prev_tokens))
            if A is None:
                A = []
            if token in A:
                c_star = self.count(tuple(prev_tokens + [token])) - self.beta
                p_star = float(c_star) / self.count(tuple(prev_tokens))
                out = p_star
            else:
                if len(prev_tokens) > 0:
                    a = self.alpha(tuple(prev_tokens))
                    prev = prev_tokens.copy()
                    prev.pop(0)
                    q_d = self.cond_prob(token, prev)
                    denom = self.denom(tuple(prev_tokens))
                    if denom != 0:
                        p_katz = float(q_d) / denom
                    else:
                        p_katz = float(q_d)
                    out = a * p_katz
                else:
                    # prev_tokens = []
                    out = self.q_ml(token)
        if out < 0:
            # print('cond_prob', token, prev_tokens, out)
            out = 10**-3

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
        if tokens in self.alpha_dict:
            out = self.alpha_dict[tokens]
        else:
            self.calculate_alpha(tokens)
            out = self.alpha_dict[tokens]

        return out

    def denom(self, tokens):
        """Normalization factor for a k-gram with 0 < k < n.

        tokens -- the k-gram tuple.
        """
        out = 0
        if tokens in self.denom_dict:
            out = self.denom_dict[tokens]
        else:
            self.calculate_denom(tokens)
            out = self.denom_dict[tokens]

        return out

    def calculate_alpha(self, tokens):
        out = 0
        for w in self.nonzero_words:
            c = self.count(tuple(list(tokens) + list(w)))
            cc = self.count(tokens)
            if c > 0 and cc > 0:
                val = (c - self.beta) / float(cc)
                out += val
        self.alpha_dict[tokens] = 1.0 - out

    def calculate_denom(self, tokens):
        out = 0
        if tokens in self.nonzero_words:
            for x in self.nonzero_words[tokens]:
                l = list(tokens)
                l.pop(0)
                out += self.cond_prob(x, l)
        self.denom_dict[tokens] = 1.0 - out

    def calculate_beta(self, held_out):
        best_beta = 0.8
        val = float('inf')
        for b in [x/10.0 for x in range(11)]:
            self.beta = b
            p = self.perplexity(held_out)
            if p < val:
                best_beta = b
                val = p

        return best_beta
