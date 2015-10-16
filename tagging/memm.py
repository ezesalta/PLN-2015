from collections import namedtuple, defaultdict
__author__ = 'Ezequiel Medina'

# sent -- the whole sentence.
# prev_tags -- a tuple with the n previous tags.
# i -- the position to be tagged.
History = namedtuple('History', 'sent prev_tags i')


class MEMM:

    def __init__(self, n, tagged_sents):
        """
        n -- order of the model.
        tagged_sents -- list of sentences, each one being a list of pairs.
        """
        self.n = n
        self.tags = {'</s>'}
        self.words = set()
        self.tag_counts = defaultdict(int)
        if n > 1:
            self.tags.add('<s>')
        for sent in tagged_sents:
            for x in sent:
                self.words.add(x[0])
                self.tags.add(x[1])

    def sents_histories(self, tagged_sents):
        """
        Iterator over the histories of a corpus.

        tagged_sents -- the corpus (a list of sentences)
        """
        histories = []
        for sent in tagged_sents:
            histories.extend(self.sent_histories(sent))

        return histories

    def sent_histories(self, tagged_sent):
        """
        Iterator over the histories of a tagged sentence.

        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        n = self.n
        prev_tags = ['<s>'] * (n - 1)
        histories = []
        sent = []
        for i, (word, tag) in enumerate(tagged_sent):
            sent.append(word)
            h = History(sent, tuple(prev_tags), i)
            histories.append(h)
            # Recalculate prev_tags
            if len(prev_tags) > 0:
                prev_tags.pop(0)
                prev_tags.append(tag)

        return histories

    def sents_tags(self, tagged_sents):
        """
        Iterator over the tags of a corpus.

        tagged_sents -- the corpus (a list of sentences)
        """
        tags = []
        for sent in tagged_sents:
            tags.extend(self.sent_tags(sent))

        return tags

    def sent_tags(self, tagged_sent):
        """
        Iterator over the tags of a tagged sentence.

        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        tags = [tag for word, tag in tagged_sent]

        return tags

    def tag(self, sent):
        """Tag a sentence.

        sent -- the sentence.
        """

    def tag_history(self, h):
        """Tag a history.

        h -- the history.
        """

    def unknown(self, w):
        """Check if a word is unknown for the model.

        w -- the word.
        """
