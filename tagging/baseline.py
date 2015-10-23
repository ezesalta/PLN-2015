from collections import defaultdict


class BaselineTagger:

    def __init__(self, tagged_sents):
        """
        tagged_sents -- training sentences, each one being a list of pairs.
        """
        self.words = defaultdict(int)
        self.tagged_words = defaultdict(dict)
        self.tags = defaultdict(int)
        self.sents = defaultdict(int)
        for sent in tagged_sents:
            words = []
            for s in sent:
                self.words[s[0]] += 1
                self.tags[s[1]] += 1
                if s[1] not in self.tagged_words[s[0]]:
                    self.tagged_words[s[0]][s[1]] = 0
                self.tagged_words[s[0]][s[1]] += 1
                words.append(s[0])
            self.sents[tuple(words)] += 1

    def tag(self, sent):
        """Tag a sentence.

        sent -- the sentence.
        """
        return [self.tag_word(w) for w in sent]

    def tag_word(self, w):
        """Tag a word.

        w -- the word.
        """
        out = 'nc'
        mft = self.max_d(self.tags)
        if mft != ():
            out = mft[0]
        tags = self.tagged_words[w]
        tup = self.max_d(tags)
        if tup != ():
            out = tup[0]
        return out

    def unknown(self, w):
        """Check if a word is unknown for the model.

        w -- the word.
        """
        out = False
        tags = self.tagged_words[w]
        tup = self.max_d(tags)
        if tup == ():
            out = True
        return out

    def max_d(self, d):
        k = -1
        m = 0
        out = ()
        for key in d:
            if d[key] > m:
                k = key
                m = d[key]
        if k != -1:
            out = tuple([k] + [m])
        return out
