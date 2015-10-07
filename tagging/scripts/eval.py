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
    sents = list(corpus.tagged_sents())

    # tag
    hits, total = 0, 0
    hits_known, hits_unknown = 0, 0
    total_known, total_unknown = 0, 0
    confusion_matrix = defaultdict(dict)
    n = len(sents)
    for i, sent in enumerate(sents):
        word_sent, gold_tag_sent = zip(*sent)

        model_tag_sent = model.tag(word_sent)
        assert len(model_tag_sent) == len(gold_tag_sent), i

        # known and unknown score
        total_errors = 0
        for m, g, w in zip(model_tag_sent, gold_tag_sent, word_sent):
            if model.unknown(w):
                hits_unknown += (m == g)
                total_unknown += 1
            else:
                hits_known += (m == g)
                total_known += 1
            # Confusion Matrix
            if m != g:
                if m not in confusion_matrix[g]:
                    confusion_matrix[g][m] = 0
                confusion_matrix[g][m] += 1
                total_errors += 1

        # global score
        hits_sent = [m == g for m, g in zip(model_tag_sent, gold_tag_sent)]
        hits += sum(hits_sent)
        total += len(sent)
        acc = float(hits) / total

        progress('{:3.1f}% ({:2.2f}%)'.format(float(i) * 100 / n, acc * 100))

    acc = float(hits) / total
    acc_known = float(hits_known) / total_known
    acc_unknown = float(hits_unknown) / total_unknown

    print('')
    print('Accuracy: {:2.2f}%'.format(acc * 100))
    print('Accuracy known: {:2.2f}%'.format(acc_known * 100))
    print('Accuracy unknown: {:2.2f}%'.format(acc_unknown * 100))
    print('Confusion Matrix:')
    print('  ', *confusion_matrix.keys())
    cant_gold = len(confusion_matrix.keys())
    #txt = ' '.join(['{'+str(x)+'}' for x in range(3)])
    #txt = ' {}'*cant_gold
    keys = list(confusion_matrix.keys())
    for gold_tag in confusion_matrix:
        print(gold_tag, list(confusion_matrix[gold_tag].items()))
        """out_cm = gold_tag
        for tag, val in confusion_matrix[gold_tag].items():
            pos = 1
            if tag in keys:
                pos = keys.index(tag)
            out_cm += ' {}{}:{}'.format((' '*pos), tag, val)

        print(out_cm)"""
