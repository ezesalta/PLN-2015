from nltk.grammar import Production, ProbabilisticProduction
from collections import defaultdict
from nltk.tree import Tree
from nltk.grammar import PCFG, Nonterminal, induce_pcfg
from parsing.cky_parser import CKYParser
from parsing.util import lexicalize, unlexicalize
import time
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
        self.prods_lex = defaultdict(list)
        self.horzMarkov = horzMarkov
        pcount = defaultdict(int)
        lcount = defaultdict(int)

        prods = []
        for tree in parsed_sents:
            t = tree.copy(deep=True)
            # Unlexicalize productions
            t = unlexicalize(t)
            if horzMarkov is None:
                t.chomsky_normal_form()
            else:
                t.chomsky_normal_form(horzMarkov=horzMarkov)
            t.collapse_unary(collapsePOS=True)

            prods.extend(t.productions())

        self.grammar = induce_pcfg(self.start, prods)
        self.prods = self.grammar.productions()
        self.parser = CKYParser(self.grammar)
        """print(*self.prods, sep='\n')
        print('')
        print(*self.prods_lex.items(), sep='\n')"""


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
        #t.draw()
        #tt = Tree('S', [Tree('Det', ['Det']), Tree('Noun', ['Noun'])])
        #self.deslex(tt, [('el', 'Det'), ('gato', 'Noun')])
        #print(*self.prods_lex.items(), sep='\n')
        #tree = self.deslex(t, tagged_sent.copy())
        tree = t.copy(deep=True)
        tree.un_chomsky_normal_form()
        tree = lexicalize(tree, words)
        #tree.draw()

        return tree

    def my_lexicalize(self, tree, tagged_sent):
        t = tree.copy(deep=True)
        for pos in t.treepositions('leaves'):
            for word, tag in tagged_sent:
                if tag == str(t[pos]):
                    t[pos] = word
                    tagged_sent.remove((word, tag))
                    break

        return t