from nltk.grammar import Production, ProbabilisticProduction
from collections import defaultdict
from nltk.tree import Tree
from nltk.grammar import PCFG, Nonterminal
from parsing.cky_parser import CKYParser
import time
__author__ = 'Ezequiel Medina'


class UPCFG:
    """Unlexicalized PCFG.
    """

    def __init__(self, n, parsed_sents, start='sentence'):
        """
        parsed_sents -- list of training trees.
        """
        self.nonterm = []
        self.start = Nonterminal(start)
        self.prods = []
        self.prods_lex = []
        pcount = defaultdict(int)
        lcount = defaultdict(int)
        for tree in parsed_sents:
            tree.collapse_unary(collapsePOS=False)
            tree.chomsky_normal_form(horzMarkov=n)
            for x in tree.productions():
                if x.is_lexical():
                    p = Production(x.lhs(), [str(x.lhs())])
                    lcount[p.lhs()] += 1
                    pcount[p] += 1
                else:
                    p = Production(x.lhs(), x.rhs())
                    #p = Production(x.lhs(), tuple([str(y) for y in x.rhs()]))
                    lcount[p.lhs()] += 1
                    pcount[p] += 1
        pcount = dict(pcount)
        lcount = dict(lcount)
        for x in pcount:
            #if str(x.lhs()) == 'sentence|<fc-sn+grup.nom>':
                #print(x, pcount[x], lcount[x.lhs()])
            prob = float(pcount[x]) / lcount[x.lhs()]
            p = ProbabilisticProduction(x.lhs(), x.rhs(), prob=prob)
            self.prods.append(p)

        self.grammar = PCFG(self.start, self.prods)
        self.parser = CKYParser(self.grammar)

    def productions(self):
        """Returns the list of UPCFG probabilistic productions.
        """

        return self.prods

    def parse(self, tagged_sent):
        """Parse a tagged sentence.

        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        init_time_cky = time.clock()
        tup = self.parser.parse([x[1] for x in tagged_sent])
        final_time_cky = time.clock()
        # Para evitar el init del CKY, lo reseteo
        self.parser.reset()
        if tup is not None:
            lp, t = tup
        else:
            t = Tree(str(self.start), [Tree(x[1], [x[1]]) for x in tagged_sent])
        #t.draw()
        #tt = Tree('S', [Tree('Det', ['Det']), Tree('Noun', ['Noun'])])
        #self.deslex(tt, [('el', 'Det'), ('gato', 'Noun')])
        init_time_deslex = time.clock()
        tree = self.deslex(t, tagged_sent.copy())
        final_time_deslex = time.clock()
        #tree.draw()
        print('')
        print('Time CKY Parser: {:.2f}'.format(final_time_cky - init_time_cky))
        print('Time Deslex: {:.2f}'.format(final_time_deslex - init_time_deslex))

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
