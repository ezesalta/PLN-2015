from collections import namedtuple

from featureforge.feature import Feature


# sent -- the whole sentence.
# prev_tags -- a tuple with the n previous tags.
# i -- the position to be tagged.
History = namedtuple('History', 'sent prev_tags i')


def word_lower(h):
    """Feature: current lowercased word.

    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].lower()


def word_istitle(h):
    """Feature: is the current word titlecased?

    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].istitle()


def word_isupper(h):
    """Feature: is the current word uppercased?

    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].isupper()


def word_isdigit(h):
    """Feature: is the current word only numbers?

    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].isdigit()


def word_isdate(h):
    """Feature: is the current word a date?

    h -- a history.
    """
    out = True
    sent, i = h.sent, h.i
    w = sent[i]
    if '/' in w:
        w = w.split('/')
    elif '-' in w:
        w = w.split('-')
    else:
        w = [w]
    for x in w:
        out *= x.isdigit()

    return out == 1


def prev_tags(h):
    return h.prev_tags


class NPrevTags(Feature):

    def __init__(self, n):
        """Feature: n previous tags tuple.

        n -- number of previous tags to consider.
        """
        self.n = n

    def _evaluate(self, h):
        """n previous tags tuple.

        h -- a history.
        """
        n = self.n
        prev_tags = list(h.prev_tags)
        out = prev_tags[-n:]

        return tuple(out)


class PrevWord(Feature):

    def __init__(self, f):
        """Feature: the feature f applied to the previous word.

        f -- the feature.
        """
        self.f = f

    def _evaluate(self, h):
        """Apply the feature to the previous word in the history.

        h -- the history.
        """
        out = 'BOS'
        sent, prev_tags, i = h.sent, h.prev_tags, h.i
        if i >= 1:
            prev_h = History(sent, prev_tags, i - 1)
            out = self.f(prev_h)

        return str(out)
