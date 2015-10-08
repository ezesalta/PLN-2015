__author__ = 'Ezequiel Medina'
from math import log


class HMM:

    def __init__(self, n, tagset, trans, out):
        """
        n -- n-gram size.
        tagset -- set of tags.
        trans -- transition probabilities dictionary.
        out -- output probabilities dictionary.
        """
        self.n = n
        self.set_tags = tagset
        self.dict_trans = trans
        self.dict_out = out

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

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.

        sent -- the sentence.
        """
