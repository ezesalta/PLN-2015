from nltk.tree import Tree
from nltk.grammar import Nonterminal, induce_pcfg
from parsing.cky_parser import CKYParser
from parsing.util import lexicalize, unlexicalize
__author__ = 'Ezequiel Medina'


class UPCFG:
    """Unlexicalized PCFG.
    """

    def __init__(self, parsed_sents, horzMarkov=None, start='sentence'):
        """
        parsed_sents -- list of training trees.
        """
        self.nonterm = []
        self.start = Nonterminal(start)
        self.prods = []

        prods = []
        for tree in parsed_sents:
            t = tree.copy(deep=True)
            # Unlexicalize productions
            t = unlexicalize(t)
            # Convert to CNF
            if horzMarkov is None:
                t.chomsky_normal_form()
            else:
                t.chomsky_normal_form(horzMarkov=horzMarkov)
            t.collapse_unary(collapsePOS=True)

            prods.extend(t.productions())

        self.grammar = induce_pcfg(self.start, prods)
        self.prods = self.grammar.productions()
        self.parser = CKYParser(self.grammar)

    def productions(self):
        """Returns the list of UPCFG probabilistic productions.
        """

        return self.prods

    def parse(self, tagged_sent):
        """Parse a tagged sentence.

        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        words, tags = [], []
        for word, tag in tagged_sent:
            words.append(word)
            tags.append(tag)
        tup = self.parser.parse(tags)
        # Para evitar el init del CKY, lo reseteo
        self.parser.reset()
        if tup is not None:
            lp, t = tup
        else:
            t = Tree(str(self.start), [Tree(x, [x]) for x in tags])
        tree = t.copy(deep=True)
        tree.un_chomsky_normal_form()
        tree = lexicalize(tree, words)
        # tree.draw()

        return tree
