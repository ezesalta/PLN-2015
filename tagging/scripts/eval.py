"""Evaulate a tagger.

Usage:
  eval.py -i <file>
  eval.py -h | --help

Options:
  -i <file>     Tagging model file.
  -h --help     Show this screen.
"""
import matplotlib.pyplot as plt
import numpy as np
from docopt import docopt
from collections import defaultdict
import pickle
import sys
from corpus.ancora import SimpleAncoraCorpusReader
import time


def progress(msg, width=None):
    """Ouput the progress of something on the same line."""
    if not width:
        width = len(msg)
    print('\b' * width + msg, end='')
    sys.stdout.flush()


if __name__ == '__main__':
    opts = docopt(__doc__)

    # Init clock
    init_time = time.clock()

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
    gold_tags = list(confusion_matrix.keys())
    cant_gold = len(confusion_matrix.keys())
    keys = list(confusion_matrix.keys())
    cm = []

    # Stop clock
    final_time = time.clock()
    print('Time lapsed: {:.2f}s'.format(final_time - init_time))

    # Print Confusion Matrix in console
    for gold_tag in confusion_matrix:
        positions = [0] * len(gold_tags)
        for t, v in confusion_matrix[gold_tag].items():
            pos = 0
            if t in gold_tags:
                pos = gold_tags.index(t)
            positions.remove(positions[pos])
            positions.insert(pos, v)
        #print(gold_tag, positions)
        cm.append(positions)
    # Show confusion matrix in a separate window
    gold_tags_str = ' '.join([str(x) for x in gold_tags])
    #plt.matshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    plt.matshow(cm)
    #plt.matshow(list(conf_matrix.values()))
    plt.xticks(np.arange(len(gold_tags)), tuple(gold_tags), rotation=90)
    plt.yticks(np.arange(len(gold_tags)), tuple(gold_tags))
    plt.title('Confusion matrix')
    plt.colorbar()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')

    plt.show()
