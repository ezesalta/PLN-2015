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
        self.S = str(self.pcfg.start())
        self._pi = defaultdict(dict)
        self._pi_lp = defaultdict(dict)
        self._bp = defaultdict(dict)
        self.prods = defaultdict(list)
        self.prods_inv = defaultdict(list)
        self.probs = defaultdict(dict)
        self.N = set()
        for x in grammar.productions():
            # Nonterminals
            self.N.add(str(x.lhs()))
            # Productions
            elems = []
            for y in x.rhs():
                if type(y) == tuple:
                    e = tuple([str(z) for z in y])
                    elems.append(e)
                    self.probs[str(x.lhs())][e] = x.prob()
                else:
                    e = tuple([str(z) for z in x.rhs()])
                    elems.append(e)
                    self.probs[str(x.lhs())][e] = x.prob()
                    break
            self.prods[str(x.lhs())].extend(elems)
            # Productions indexed by rhs
            e = (str(x.lhs()), x.prob())
            self.prods_inv[tuple([str(z) for z in x.rhs()])].append(e)

    def reset(self):
        self._pi = defaultdict(dict)
        self._pi_lp = defaultdict(dict)
        self._bp = defaultdict(dict)

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
                j = i + l
                # fill pi[i, j]
                for s in range(i, j):
                    # consider split pi[i, s] + pi[s+1, j]
                    for a in self._pi[(i, s)]:
                        pi1 = self._pi[(i, s)][a]
                        for b in self._pi[(s + 1, j)]:
                            pi2 = self._pi[(s + 1, j)][b]
                            if (a, b) in self.prods_inv:
                                for c, q in self.prods_inv[(a, b)]:
                                    val = pi1 * pi2 * q
                                    val_lp = log2(q) + log2(pi1) + log2(pi2)
                                    bp1 = self._bp[(i, s)][a]
                                    bp2 = self._bp[(s + 1, j)][b]
                                    tree = [bp1] + [bp2]
                                    if c in self._pi[(i, j)]:
                                        prev_val = self._pi[(i, j)][c]
                                        if prev_val < val:
                                            self._pi[(i, j)][c] = val
                                            self._pi_lp[(i, j)][c] = val_lp
                                            self._bp[(i, j)][c] = Tree(c, tree)
                                    else:
                                        self._pi[(i, j)][c] = val
                                        self._pi_lp[(i, j)][c] = val_lp
                                        self._bp[(i, j)][c] = Tree(c, tree)

        # add empty dicts to back pointers dict
        l = [self._bp[x] for x, y in self._pi.items() if y == {}]

        self._pi.update(self._pi_lp)
        self._pi = dict(self._pi)
        self._bp = dict(self._bp)

        # Restore tree from back pointers
        tup = None
        if (1, n) in self._bp:
            if self.S in self._bp[(1, n)]:
                t = self._bp[(1, n)][self.S]
                lp = self._pi[(1, n)][self.S]
                tup = (lp, t)
        return tup

    def get_prod(self, x):
        out = []
        if x in self.prods:
            y = self.prods[str(x)]
            out = [z for z in y if len(z) >= 2]

        return out

    def q(self, x, y):
        # x -> y
        # y is a list
        out = None
        if x in self.prods:
            rhs = self.prods[str(x)]
            if tuple(y) in rhs:
                out = self.probs[str(x)][tuple(y)]

        return out
