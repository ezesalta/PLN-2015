"""Train an n-gram model.

Usage:
  train.py -n <n> [-m <model>] -o <file>
  train.py -h | --help

Options:
  -n <n>        Order of the model.
  -m <model>    Model to use [default: ngram]:
                  ngram: Unsmoothed n-grams.
                  addone: N-grams with add-one smoothing.
                  interpolated: N-grams with interpolated smoothing.
                  backoff: N-grams with backoff smoothing.
  -o <file>     Output model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
import time
from nltk.corpus import gutenberg
from languagemodeling.ngram import NGram, AddOneNGram, InterpolatedNGram, BackOffNGram
from languagemodeling.MyCorpus import MyCorpus


if __name__ == '__main__':
    opts = docopt(__doc__)

    init_time = time.clock()
    # load the data
    # sents = gutenberg.sents('austen-emma.txt')
    corpus = MyCorpus()
    sents = corpus.sents_train()

    # train the model
    n = int(opts['-n'])
    typeModel = opts['-m']
    if typeModel == 'addone':
        model = AddOneNGram(n, sents)
    elif typeModel == 'interpolated':
        model = InterpolatedNGram(n, sents)
    elif typeModel == 'backoff':
        model = BackOffNGram(n, sents)
    else:
        model = NGram(n, sents)

    # save it
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
    final_time = time.clock()
    print('Time: {:.2f}m'.format((final_time - init_time) / 60.0))
