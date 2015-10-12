__author__ = 'Ezequiel Medina'
from math import log
from collections import defaultdict


class HMM:

    def __init__(self, n, tagset, trans, out):
        """
        n -- n-gram size.
        tagset -- set of tags.
        trans -- transition probabilities dictionary.
        out -- output probabilities dictionary.
        """
        self.n = n
        self.dict_trans = trans
        self.dict_out = out
        self.set_tags = tagset
        self.set_words = set()
        for tag in out:
            for w in out[tag].keys():
                self.set_words.add(w)

    def tagset(self):
        """Returns the set of tags.
        """
        return self.set_tags

    def trans_prob(self, tag, prev_tags):
        """Probability of a tag.

        tag -- the tag.
        prev_tags -- tuple with the previous n-1 tags (optional only if n = 1).
        """
        out = 0
        if prev_tags in self.dict_trans:
            prob_tags = self.dict_trans[prev_tags]
            if tag in prob_tags:
                out = prob_tags[tag]
        return out

    def out_prob(self, word, tag):
        """Probability of a word given a tag.

        word -- the word.
        tag -- the tag.
        """
        out = 0
        if tag in self.dict_out:
            prob_words = self.dict_out[tag]
            if word in prob_words:
                out = prob_words[word]

        return out

    def tag_prob(self, y):
        """
        Probability of a tagging.
        Warning: subject to underflow problems.

        y -- tagging.
        """
        out = 0
        y_r = y.copy()
        y_r.reverse()
        for i, tag in enumerate(y_r):
            prev_tags = ()
            if i + 1 < len(y_r):
                prev_tags = y_r[i + 1:]
                prev_tags.reverse()
            out += self.trans_prob(tag, tuple(prev_tags))

        return out

    def prob(self, x, y):
        """
        Joint probability of a sentence and its tagging.
        Warning: subject to underflow problems.

        x -- sentence.
        y -- tagging.
        """
        out = 1
        for x in [self.out_prob(word, tag) for word, tag in zip(x, y)]:
            out *= x
        return out

    def tag_log_prob(self, y):
        """
        Log-probability of a tagging.

        y -- tagging.
        """
        out = 0
        y_r = y.copy()
        y_r.reverse()
        for i, tag in enumerate(y_r):
            prev_tags = []
            if i + 1 < len(y_r):
                prev_tags = y_r[i + 1:]
                prev_tags.reverse()
            prob = self.trans_prob(tag, tuple(prev_tags))
            if prob > 0:
                out += log(prob, 2)

        return out

    def log_prob(self, x, y):
        """
        Joint log-probability of a sentence and its tagging.

        x -- sentence.
        y -- tagging.
        """
        out = log(self.prob(x, y), 2)

        return out

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.

        sent -- the sentence.
        """
        tagging = []
        for word in sent:
            max = 0
            t = ''
            for tag in self.set_tags:
                prob = self.out_prob(word, tag)
                if prob > max:
                    max = prob
                    t = tag
            tagging.append(t)

        # CONSULTAR !!!

        return tagging


class ViterbiTagger:

    def __init__(self, hmm):
        """
        hmm -- the HMM.
        """
        self.hmm = hmm
        self._pi = defaultdict(dict)
        # self.backpointer = defaultdict(dict)
        #self.prev_tags = ['<s>', '<s>']
        #self._pi[0][tuple(self.prev_tags)] = 1
        """self.tags_prob = defaultdict(dict)
        tags = list(self.hmm.set_tags) + ['<s>']
        for tag1 in tags:
            for tag2 in self.hmm.set_tags:
                print(tag2, tuple([tag1]))
                self.tags_prob[tag1][tag2] = self.hmm.trans_prob(tag2, tuple([tag1]))
        print(*self.tags_prob.items(), sep='\n')"""

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.

        sent -- the sentence.
        """
        # Init
        tagging = []
        init = ['<s>', '<s>']
        prev_tags = init.copy()
        self._pi[0][tuple(init)] = (1.0, tagging.copy())
        # Recursive
        #i = 0
        #cant_trans = len(self.hmm.dict_trans)
        #for word in sent:
        for i in range(len(self.hmm.dict_trans)):
            word = 'pepe'
            if i < len(sent):
                word = sent[i]
            i += 1
            # Asumo que siempre me da un tag
            u = prev_tags[-1]
            if u == '</s>':
                break
            aux = list(self.hmm.dict_trans[tuple(prev_tags)])
            v = aux.pop(0)
            if v == '</s>':
                break
            tagging.append(v)
            p = [1.0]
            if tuple(prev_tags) in self._pi[i - 1]:
                p = self._pi[i - 1][tuple(prev_tags)]
            # log?
            q = self.hmm.trans_prob(v, tuple(prev_tags))
            e = self.hmm.out_prob(word, v)
            t = tuple([u] + [v])
            #val = log(p[0] * q * e, 2)
            val = p[0] * q * e
            #print(i, 'p:', p, 'q:', q, 'e:', e, 't:', t, word, 'val:', val)
            #tup = (val, tagging.copy())
            #print(tup)
            self._pi[i][t] = (val, tagging.copy())

            # Set next prev_tags
            if len(prev_tags) == 2:
                prev_tags.pop(0)
            prev_tags.append(v)

        self._pi = dict(self._pi)
        print(self._pi)

        return tagging


class MLHMM:

    def __init__(self, n, tagged_sents, addone=True):
        """
        n -- order of the model.
        tagged_sents -- training sentences, each one being a list of pairs.
        addone -- whether to use addone smoothing (default: True).
        """
        self.counts_tag = defaultdict(int)
        self.words = set()

        for sent in tagged_sents:
            sent_tags = []
            for x in sent:
                self.words.add(x[0])
                sent_tags.append(x[1])

            if n > 1:
                sent_tags.insert(0, '<s>')
            sent_tags.append('</s>')

            for i in range(len(sent_tags) - n + 1):
                ngram = tuple(sent_tags[i: i + n])
                self.counts_tag[ngram] += 1
                self.counts_tag[ngram[:-1]] += 1

    def tcount(self, tokens):
        """Count for an k-gram for k <= n.

        tokens -- the k-gram tuple.
        """
        out = 0
        if tokens in self.counts_tag:
            out = self.counts_tag[tokens]
        return out

    def unknown(self, w):
        """Check if a word is unknown for the model.

        w -- the word.
        """
        return not (w in self.words)

