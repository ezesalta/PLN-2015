__author__ = 'Ezequiel Medina'
from nltk.grammar import Production, ProbabilisticProduction
from collections import defaultdict
from nltk.tree import Tree
from nltk.grammar import PCFG, Nonterminal
from parsing.cky_parser import CKYParser


class UPCFG:
    """Unlexicalized PCFG.
    """

    def __init__(self, parsed_sents, start='sentence'):
        """
        parsed_sents -- list of training trees.
        """
        self.nonterm = []
        self.start = Nonterminal(start)
        self.prods = []
        self.prods_lex = []
        for tree in parsed_sents:
            tree.collapse_unary(collapsePOS=False)
            tree.chomsky_normal_form(horzMarkov=2)
            pcount = defaultdict(int)
            lcount = defaultdict(int)
            for x in tree.productions():
                if x.is_lexical():
                    p = Production(x.lhs(), [str(x.lhs())])
                    lcount[p.lhs()] += 1
                    pcount[p] += 1
                else:
                    p = Production(x.lhs(), x.rhs())
                    lcount[p.lhs()] += 1
                    pcount[p] += 1
            pcount = dict(pcount)
            lcount = dict(lcount)
            for x in pcount:
                prob = float(pcount[x]) / lcount[x.lhs()]
                p = ProbabilisticProduction(x.lhs(), x.rhs(), prob=prob)
                self.prods.append(p)

    def productions(self):
        """Returns the list of UPCFG probabilistic productions.
        """
        #print(*self.prods, sep='\n')

        return self.prods

    def parse(self, tagged_sent):
        """Parse a tagged sentence.

        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        grammar = PCFG(self.start, self.productions())
        parser = CKYParser(grammar)
        tup = parser.parse([x[1] for x in tagged_sent])
        if tup is not None:
            lp, t = tup
        else:
            t = Tree(str(self.start), [Tree(x[1], [x[1]]) for x in tagged_sent])
        #t.draw()
        #tt = Tree('S', [Tree('Det', ['Det']), Tree('Noun', ['Noun'])])
        #self.deslex(tt, [('el', 'Det'), ('gato', 'Noun')])
        tree = self.deslex(t, tagged_sent.copy())
        #tree.draw()

        return tree

    def deslex(self, tree, tagged_sent):
        new_tree = Tree(tree.label(), [])
        if tree.height() <= 3:
            for prod in tree.productions():
                if prod.is_lexical():
                    for word, tag in tagged_sent:
                        if prod.rhs()[0] == tag:
                            t = Tree(str(prod.lhs()), [word])
                            if tree.height() == 2:
                                new_tree.extend(t)
                            else:
                                new_tree.append(t)
                            tagged_sent.remove((word, tag))
                            break
                else:
                    pass
        elif tree.height() > 3:
            for st in tree:
                t = self.deslex(st, tagged_sent)
                new_tree.append(t)

        return new_tree
