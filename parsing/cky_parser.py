from collections import defaultdict
from math import log2
from nltk.tree import Tree
__author__ = 'Ezequiel Medina'


class CKYParser:

    def __init__(self, grammar):
        """
        grammar -- a binarised NLTK PCFG.
        """
        self.pcfg = grammar
        self.terminals = [x for x in grammar.productions()]
        self.S = str(self.pcfg.start())
        self._pi = defaultdict(dict)
        self._pi_lp = defaultdict(dict)
        self._bp = defaultdict(dict)
        self.N = set()
        for x in grammar.productions():
            self.N.add(str(x.lhs()))

    def parse(self, sent):
        """Parse a sequence of terminals.

        sent -- the sequence of terminals.
        """
        n = len(sent)
        # Init
        for i in range(1, n + 1):
            wi = sent[i - 1]
            for x in self.N:
                prob = self.q(x, [wi])
                if prob is not None:
                    self._pi[(i, i)][str(x)] = prob
                    self._pi_lp[(i, i)][str(x)] = log2(prob)
                    self._bp[(i, i)][str(x)] = Tree(str(x), [wi])

        # Recursive
        for l in range(1, n):
            for i in range(1, n - l + 1):
                wi = sent[i - 1]
                j = i + l
                maxs = {'x': '', 'y': (), 'q': float('-inf'), 's': 0,
                        'val': float('-inf')}
                for x in self.N:
                    for y in self.get_prod(x):
                        q = self.q(x, y)
                        for s in range(i, j):
                            pi1, pi2 = 0.0, 0.0
                            if y[0] in self._pi[i, s]:
                                pi1 = self._pi[i, s][y[0]]
                            if y[1] in self._pi[s + 1, j]:
                                pi2 = self._pi[s + 1, j][y[1]]
                            # Create empty sets on _bp
                            if y[0] in self._bp[i, s] and y[1] in self._bp[s + 1, j]:
                                bp1 = self._bp[i, s][y[0]]
                                bp2 = self._bp[s + 1, j][y[1]]

                            val = q * pi1 * pi2

                            if val > maxs['val']:
                                maxs = {'x': x, 'y': y, 'q': q,
                                        's': s, 'val': val}
                if maxs['val'] > 0.0:
                    node = str(maxs['x'])
                    self._pi[(i, j)][node] = maxs['val']
                    self._pi_lp[(i, j)][node] = log2(maxs['val'])
                    tree = []
                    tree.extend([bp1])
                    tree.extend([bp2])
                    self._bp[(i, j)][node] = Tree(node, tree)

        """print('Pi')
        print(*self._pi.items(), sep='\n')
        print('Pi_lp')
        print(*self._pi_lp.items(), sep='\n')
        print('\nPi(1, 5, S):', self._pi[(1, 5)][self.S], 'log2:', log2(self._pi[(1, 5)][self.S]))
        print('\nPi_lp(1, 5, S):', self._pi_lp[(1, 5)][self.S])
        print('\nBack Pointers')
        print(*self._bp.items(), sep='\n')"""

        self._pi.update(self._pi_lp)
        self._pi = dict(self._pi)
        self._bp = dict(self._bp)

        t = self._bp[(1, n)][self.S]
        lp = self._pi[(1, n)][self.S]
        return lp, t

    def get_prod(self, x):
        out = []
        for prod in self.pcfg.productions():
            if str(prod.lhs()) == x:
                y = prod.rhs()
                if len(y) == 2:
                    out.append(tuple([str(x) for x in y]))

        return out

    def q(self, x, y):
        # x -> y
        # y is a list
        out = None
        for prod in self.pcfg.productions():
            if str(prod.lhs()) == x:
                rhs = tuple([str(x) for x in prod.rhs()])
                if rhs == tuple(y):
                    out = prod.prob()
                    break

        return out
