"""Train a parser.

Usage:
  train.py [-m <model>] -o <file> [-n <horzM>]
  train.py -h | --help

Options:
  -m <model>          Model to use [default: upcfg]:
                        flat: Flat trees
                        rbranch: Right branching trees
                        lbranch: Left branching trees
                        upcfg: Unlexicalize PCFG
  -o <file>           Output model file.
  -n <horzM>          Number of horizontal Markovization
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
import time
from corpus.ancora import SimpleAncoraCorpusReader
from parsing.baselines import Flat, RBranch#, LBranch
from parsing.upcfg import UPCFG


models = {
    'upcfg': UPCFG,
    'flat': Flat,
    'rbranch': RBranch,
    #'lbranch': LBranch,
}


if __name__ == '__main__':
    opts = docopt(__doc__)

    init_time = time.clock()
    print('Loading corpus...')
    files = 'CESS-CAST-(A|AA|P)/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)

    print('Training model...')
    n = opts['-n']
    if n is None:
        n = 2
    else:
        n = int(n)
    m = opts['-m']
    if m is None or m == 'upcfg':
        model = models[m](n, corpus.parsed_sents())
    else:
        model = models[m](corpus.parsed_sents())

    print('Saving...')
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
    final_time = time.clock()
    print('Time: {:.2f}s'.format(final_time - init_time))
