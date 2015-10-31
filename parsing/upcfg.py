__author__ = 'Ezequiel Medina'


class UPCFG:
    """Unlexicalized PCFG.
    """

    def __init__(self, parsed_sents, start='sentence'):
        """
        parsed_sents -- list of training trees.
        """
        self.nonterminals = []
        self.start = ''
        self.prods = []
        for tree in parsed_sents:
            tree.collapse_unary(collapsePOS=False)
            tree.chomsky_normal_form(horzMarkov=2)
            self.prods += tree.productions()

    def productions(self):
        """Returns the list of UPCFG probabilistic productions.
        """
        print(*self.prods, sep='\n')
        #return self.prods

    def parse(self, tagged_sent):
        """Parse a tagged sentence.

        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """