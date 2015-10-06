"""Evaulate a tagger.

Usage:
  eval.py -i <file>
  eval.py -h | --help

Options:
  -i <file>     Tagging model file.
  -h --help     Show this screen.
"""
from docopt import docopt
from collections import defaultdict
import pickle
import sys
from corpus.ancora import SimpleAncoraCorpusReader


def progress(msg, width=None):
    """Ouput the progress of something on the same line."""
    if not width:
        width = len(msg)
    print('\b' * width + msg, end='')
    sys.stdout.flush()


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the model
    filename = opts['-i']
    f = open(filename, 'rb')
    model = pickle.load(f)
    f.close()

    # load the data
    files = '3LB-CAST/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)
    sents = corpus.tagged_sents()

    # tag
    hits, total = 0, 0
    hits_known, hits_unknown = 0, 0
    confusion_matrix = defaultdict(dict)
    n = len(sents)
    for i, sent in enumerate(sents):
        word_sent, gold_tag_sent = zip(*sent)

        model_tag_sent = model.tag(word_sent)
        assert len(model_tag_sent) == len(gold_tag_sent), i

        # known and unknown score
        for m, g, w in zip(model_tag_sent, gold_tag_sent, word_sent):
            if model.unknown(w):
                hits_unknown += (m == g)
            else:
                hits_known += (m == g)
            # Confusion Matrix
            if m != g:
                if m not in confusion_matrix[g]:
                    confusion_matrix[g][m] = 0
                confusion_matrix[g][m] += 1

        # global score
        hits_sent = [m == g for m, g in zip(model_tag_sent, gold_tag_sent)]
        hits += sum(hits_sent)
        total += len(sent)
        acc = float(hits) / total

        progress('{:3.1f}% ({:2.2f}%)'.format(float(i) * 100 / n, acc * 100))

    acc = float(hits) / total
    acc_known = float(hits_known) / total
    acc_unknown = float(hits_unknown) / total

    print('')
    print('Accuracy: {:2.2f}%'.format(acc * 100))
    print('Accuracy known: {:2.2f}%'.format(acc_known * 100))
    print('Accuracy unknown: {:2.2f}%'.format(acc_unknown * 100))
    print('Confusion Matrix:')
    # print(' ', *confusion_matrix.keys())
    for gold_tag in confusion_matrix:
        for tag, val in confusion_matrix[gold_tag].items():
            print(gold_tag, tag, val)
            exit()
