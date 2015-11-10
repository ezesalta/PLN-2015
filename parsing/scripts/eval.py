"""Evaulate a parser.

Usage:
  eval.py -i <file> [-m <m>] [-n <n>]
  eval.py -h | --help

Options:
  -i <file>     Parsing model file.
  -m <m>        Parse only sentences of length <= <m>.
  -n <n>        Parse only <n> sentences (useful for profiling).
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
import sys
import time
from corpus.ancora import SimpleAncoraCorpusReader

from parsing.util import spans


def progress(msg, width=None):
    """Ouput the progress of something on the same line."""
    if not width:
        width = len(msg)
    print('\b' * width + msg, end='')
    sys.stdout.flush()


if __name__ == '__main__':
    opts = docopt(__doc__)

    print('Loading model...')
    filename = opts['-i']
    f = open(filename, 'rb')
    model = pickle.load(f)
    f.close()

    print('Loading corpus...')
    files = '3LB-CAST/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)
    parsed_sents = list(corpus.parsed_sents())

    print('Parsing...')
    hits, total_gold, total_model = 0, 0, 0
    hits_un = 0
    diff = 0
    n = opts['-n']
    if n is None:
        n = len(parsed_sents)
    else:
        n = int(n)
    m = opts['-m']
    if m is None:
        m = 20
    else:
        m = int(m)
    """gold_parsed_sents = []
    for gold_parsed_sent in parsed_sents:
        tagged_sent = gold_parsed_sent.pos()
        if len(tagged_sent) > m:
            gold_parsed_sents.append(gold_parsed_sent)"""
    init_time = time.clock()
    prec, rec, f1 = 0.0, 0.0, 0.0
    cky = 0.0
    format_str = '{:3.1f}% ({}/{}) (P={:2.2f}%, R={:2.2f}%, F1={:2.2f}%)'
    progress(format_str.format(0.0, 0, n, 0.0, 0.0, 0.0))
    for i, gold_parsed_sent in enumerate(parsed_sents):
        tagged_sent = gold_parsed_sent.pos()
        if len(tagged_sent) > m:
            diff += 1
        else:
            # parse
            init_time_cky = time.clock()
            model_parsed_sent = model.parse(tagged_sent)
            final_time_cky = time.clock()
            cky += final_time_cky - init_time_cky

            # compute labeled scores
            gold_spans = spans(gold_parsed_sent, unary=False)
            model_spans = spans(model_parsed_sent, unary=False)
            hits += len(gold_spans & model_spans)
            total_gold += len(gold_spans)
            total_model += len(model_spans)

            # compute unlabeled scores
            #print([x[1:] == y[1:] for x, y in zip(gold_spans, model_spans)])
            gold_spans_unlabeled = set([x[1:] for x in gold_spans])
            model_spans_unlabeled = set([x[1:] for x in model_spans])
            hits_un += len(gold_spans_unlabeled & model_spans_unlabeled)
            prec_un = float(hits_un) / total_model * 100
            rec_un = float(hits_un) / total_gold * 100
            if prec_un + rec_un > 0:
                f1_un = 2 * prec_un * rec_un / (prec_un + rec_un)

            # compute labeled partial results
            prec = float(hits) / total_model * 100
            rec = float(hits) / total_gold * 100
            f1 = 2 * prec * rec / (prec + rec)

        #progress(format_str.format(float(i+1-diff) * 100 / n, i+1-diff, n, prec, rec, f1))
        progress(format_str.format(float(i) * 100 / n, i, n, prec, rec, f1))
        if i >= n:
            break

    final_time = time.clock()
    print('')
    print('Parsed {} sentences'.format(n-diff))
    print('Discarded {} sentences'.format(diff))
    print('Labeled')
    print('    Precision: {:2.2f}% '.format(prec))
    print('    Recall: {:2.2f}% '.format(rec))
    print('    F1: {:2.2f}% '.format(f1))
    print('Unlabeled')
    print('    Precision: {:2.2f}% '.format(prec_un))
    print('    Recall: {:2.2f}% '.format(rec_un))
    print('    F1: {:2.2f}% '.format(f1_un))
    print('Time: {:.2f}s'.format(final_time - init_time))
    print('Averge time CKY parser: {:.2f}'.format(float(cky) / (n-diff+1)))
