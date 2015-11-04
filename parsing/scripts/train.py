"""Train a parser.

Usage:
  train.py [-m <model>] -o <file>
  train.py -h | --help

Options:
  -m <model>    Model to use [default: upcfg]:
                  flat: Flat trees
                  rbranch: Right branching trees
                  lbranch: Left branching trees
  -o <file>     Output model file.
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
    model = models[opts['-m']](corpus.parsed_sents())

    print('Saving...')
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
    final_time = time.clock()
    print('Time: {:.2f}s'.format(final_time - init_time))
