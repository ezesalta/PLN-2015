from math import log
from collections import defaultdict
__author__ = 'Ezequiel Medina'


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
        self.tags = tagset
        self.words = set()
        for tag in out:
            for w in out[tag].keys():
                self.words.add(w)

    def tagset(self):
        """Returns the set of tags.
        """
        return self.tags

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
        out = 1
        yy = y.copy()
        yy.append('</s>')
        prev_tags = ['<s>'] * (self.n - 1)
        for i, tag in enumerate(yy):
            out *= self.trans_prob(tag, tuple(prev_tags))
            if len(prev_tags) > 0:
                prev_tags.pop(0)
                prev_tags.append(tag)

        return out

    def prob(self, x, y):
        """
        Joint probability of a sentence and its tagging.
        Warning: subject to underflow problems.

        x -- sentence.
        y -- tagging.
        """
        """out = 1
        for x in [self.out_prob(word, tag) for word, tag in zip(x, y)]:
            out *= x
        return out"""
        out_prob = 1
        for x in [self.out_prob(word, tag) for word, tag in zip(x, y)]:
            out_prob *= x
        trans_prob = self.tag_prob(y)

        return out_prob * trans_prob

    def tag_log_prob(self, y):
        """
        Log-probability of a tagging.

        y -- tagging.
        """
        return log(self.tag_prob(y), 2)

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
        tagger = ViterbiTagger(self)
        return tagger.tag(sent)


class ViterbiTagger:

    def __init__(self, hmm):
        """
        hmm -- the HMM.
        """
        self.hmm = hmm
        self._pi = defaultdict(dict)

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.

        sent -- the sentence.
        """
        # Init
        tagging = []
        init = ['<s>'] * (self.hmm.n - 1)
        prev_tags = init.copy()
        self._pi[0][tuple(init)] = (1.0, tagging.copy())
        # Recursive
        for i in range(len(sent)):
            word = sent[i]
            i += 1
            next_tags = []
            for v in self.hmm.tagset():
                #print('prev_tags', prev_tags, v, i - 1)
                #print('pi anterior', self._pi[i - 1])
                p = self._pi[i - 1][tuple(prev_tags)]
                q = self.hmm.trans_prob(v, tuple(prev_tags))
                e = self.hmm.out_prob(word, v)
                val = p[0] * q * e
                #print('prev_tags', prev_tags, v, val)
                if val > 0:
                    next_tags.append((v, val))
                else:
                    # CONSULTAR QUE HACER CON ESTOS
                    pass
            mv = float('-inf')
            tg = []
            pt = []
            prev = prev_tags.copy()
            if len(next_tags) == 0:
                next_tags.append(('nc', 1.0))
                #self._pi[i][tuple(prev)] = (1.0, tagging.copy())
                #print('ENTROOOOOOOOO', prev, i, tagging)
                #print(self._pi[i][tuple(prev)])
            #else:
            for t, val in next_tags:
                # Set next prev_tags
                if len(prev) > 0:
                    prev.pop(0)
                prev.append(t)
                #print(t, val, prev)
                new_tagging = tagging.copy() + [t]
                self._pi[i][tuple(prev)] = (val, new_tagging.copy())
                if val > mv:
                    mv = val
                    tg = new_tagging.copy()
                    pt = prev.copy()
                prev = prev_tags.copy()
            prev_tags = pt.copy()
            tagging = tg.copy()

            #print(dict(self._pi))

        self._pi = dict(self._pi)
        #print(*self._pi.items(), sep='\n')
        # CONSULTAR PORQUE TENGO QUE HACER ESTO
        for i in self._pi:
            for t in self._pi[i]:
                v, tg = self._pi[i][t]
                if v > 0:
                    self._pi[i][t] = (log(v, 2), tg)
                else:
                    self._pi[i][t] = (float('-inf'), tg)
        # --------------------------------------

        #print('n:', self.hmm.n)
        #print(*self._pi.items(), sep='\n')

        return tagging


class ViterbiTaggerCorregido:

    def __init__(self, hmm):
        """
        hmm -- the HMM.
        """
        self.hmm = hmm
        self._pi = defaultdict(dict)

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.

        sent -- the sentence.
        """
        # Init
        tagging = []
        init = ['<s>'] * (self.hmm.n - 1)
        prev_tags = init.copy()
        self._pi[0][tuple(init)] = (0.0, tagging.copy())
        # Recursive
        for i in range(len(sent)):
            word = sent[i]
            i += 1
            next_tags = []
            tagset = [(tag, self.hmm.out_prob(word, tag)) for tag in self.hmm.tagset()]
            for v, e in [(v, e) for v, e in tagset if e > 0.0]:
                for prev, (p, tagging) in self._pi[i - 1].items():
                    q = self.hmm.trans_prob(v, prev)
                    if q > 0.0:
                        val = p * q * e
                        new_prev = (prev + (v,))[1:]
                        new_p = p + log(e, 2) + log(q, 2)
                        if new_prev not in self._pi[i] or new_p > self._pi[i][new_prev][0]:
                            self._pi[i][new_prev] = (new_p, tagging + [v])
            #print(dict(self._pi))

        self._pi = dict(self._pi)
        #print('n:', self.hmm.n)
        #print(*self._pi.items(), sep='\n')

        max_val = float('-inf')
        last = list(self._pi.keys())[-1]
        for prev, (p, tagg) in self._pi[last].items():
            if p > max_val:
                max_val = p
                tagging = tagg
        #print(tagging, max_val)

        return result


log2 = lambda x: log(x, 2)


class ViterbiTaggerDeFranco:

    def __init__(self, hmm):
        """
        hmm -- the HMM.
        """
        self._hmm = hmm
        self._pi = {}

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.

        sent -- the sentence.
        """
        m = len(sent)
        hmm = self._hmm
        n = hmm.n
        tagset = hmm.tagset()

        pi = self._pi
        pi[0] = {
            ('<s>',) * (n - 1): (0.0, [])
        }

        for i, w in zip(range(1, m + 1), sent):
            pi[i] = {}

            # iterate over tags that can follow with out_prob > 0.0
            tag_out_probs = [(t, hmm.out_prob(w, t)) for t in tagset]
            for t, out_p in [(t, p) for t, p in tag_out_probs if p > 0.0]:
                # iterate over non-zeros in the previous column
                for prev, (lp, tag_sent) in pi[i - 1].items():
                    trans_p = hmm.trans_prob(t, prev)
                    if trans_p > 0.0:
                        new_prev = (prev + (t,))[1:]
                        new_lp = lp + log2(out_p) + log2(trans_p)
                        # is it the max?
                        if new_prev not in pi[i] or new_lp > pi[i][new_prev][0]:
                            # XXX: what if equal?
                            pi[i][new_prev] = (new_lp, tag_sent + [t])

        # last step: generate STOP
        max_lp = float('-inf')
        result = None
        for prev, (lp, tag_sent) in pi[m].items():
            p = hmm.trans_prob('</s>', prev)
            if p > 0.0:
                new_lp = lp + log2(p)
                if new_lp > max_lp:
                    max_lp = new_lp
                    result = tag_sent

        return result


class MLHMM(HMM):

    def __init__(self, n, tagged_sents, addone=True):
        """
        n -- order of the model.
        tagged_sents -- training sentences, each one being a list of pairs.
        addone -- whether to use addone smoothing (default: True).
        """
        self.counts = defaultdict(int)
        self.counts_tag = defaultdict(int)
        self.words = set()
        self.tags = set()
        self.addone = addone
        self.n = n

        my_counts = defaultdict(int)
        m = 1
        while m <= n:
            for sent in tagged_sents:
                sent_tags = []
                for x in sent:
                    if m == 1:
                        self.words.add(x[0])
                        self.tags.add(x[1])
                        self.counts[x] += 1
                    sent_tags.append(x[1])
                if m > 1:
                    sent_tags.insert(0, '<s>')
                sent_tags.append('</s>')

                for i in range(len(sent_tags) - m + 1):
                    ngram = tuple(sent_tags[i: i + m])
                    my_counts[ngram] += 1
                    my_counts[ngram[:-1]] += 1
            self.counts_tag.update(my_counts)
            my_counts.clear()
            m += 1
        #print(*self.counts_tag.items(), sep='\n')

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

    def count(self, tokens):
        out = 0
        if tokens in self.counts:
            out = self.counts[tokens]
        return out

    def trans_prob(self, tag, prev_tags):
        """Probability of a tag.

        tag -- the tag.
        prev_tags -- tuple with the previous n-1 tags (optional only if n = 1).
        """
        out = 0
        if prev_tags is None:
            prev_tags = ()

        tk = list(prev_tags) + [tag]
        Ci = self.tcount(tuple(tk))
        N = self.tcount(prev_tags)
        if self.addone:
            V = len(self.tags)
            out = (Ci + 1) / float(N + V)
        else:
            if N > 0:
                out = Ci / float(N)

        #print('trans_prob', out, tag, prev_tags, self.addone)
        return out

    def out_prob(self, word, tag):
        """Probability of a word given a tag.

        word -- the word.
        tag -- the tag.
        """
        out = 0
        c1 = self.count((word, tag))
        c2 = self.tcount((tag,))
        if c2 > 0:
            out = c1 / float(c2)

        return out


