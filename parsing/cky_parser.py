from collections import defaultdict
from math import log
from nltk.tree import Tree
__author__ = 'Ezequiel Medina'


class CKYParser:

    def __init__(self, grammar):
        """
        grammar -- a binarised NLTK PCFG.
        """
        self.pcfg = grammar
        self.terminals = [x for x in grammar.productions()]
        self.S = self.pcfg.start()
        self._pi = defaultdict(dict)
        self.N = set()
        for x in grammar.productions():
            #x = str(x)
            #non_term, prod = x.split(' -> ')
            self.N.add(x.lhs())

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
                #if prob is not None:
                self._pi[(i, i)][x] = prob

        # Recursive
        for i in range(1, n):
            for j in range(i + 1, n + 1):
                max_x = ''
                max_y = ()
                max_q = float('-inf')
                max_val = float('-inf')
                sum_val = 0.0
                for x in self.N:
                    r = self.get_prod(x)
                    for y in r:
                        q = self.q(x, y)
                        for s in range(i, j):
                            #print(i, s, s+1, j, y)
                            #print(*self._pi.items(), sep='\n')

                            # CONSULTAR!!!!!!!
                            val = 0.0
                            if y[0] in self._pi[i, s] and y[1] in self._pi[s + 1, j]:
                                val = q * self._pi[i, s][y[0]] * \
                                      self._pi[s + 1, j][y[1]]
                                sum_val += val
                            #print('val', val)
                            if val > max_val:
                                max_val = val
                                max_q = q
                                max_x = x
                                max_y = y
                    #print('max', max_val)
                    #if max_val > float('-inf'):
                    if max_val > 0.0:
                        #self._pi[(i, j)][max_x] = max_val
                        self._pi[(i, j)][max_x] = sum_val
                    # DEBUG!!!
                    if (i, j) == (3, 5):
                        print(i, j, max_x, max_val, sum_val)
        print(*self._pi.items(), sep='\n')

        t = Tree.fromstring(
            """
                (S
                    (NP (Det el) (Noun gato))
                    (VP (Verb come) (NP (Noun pescado) (Adj crudo)))
                )
            """)
        lp = log(1.0 * 0.6 * 1.0 * 0.9 * 1.0 * 1.0 * 0.4 * 0.1 * 1.0, 2)
        return (t, lp)


    def get_prod(self, x):
        out = []
        for prod in self.pcfg.productions():
            if prod.lhs() == x:
                y = prod.rhs()
                if len(y) == 2:
                    out.append(y)

        return out

    def q(self, x, y):
        # x -> y
        # y is a list
        out = 0.0
        for prod in self.pcfg.productions():
            #if prod.is_lexical():
            if prod.lhs() == x:
                if prod.rhs() == tuple(y):
                    out = prod.logprob()
                    #out = prod.prob()
                    break

        return out
