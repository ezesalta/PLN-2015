"""Print corpus statistics.

Usage:
  stats.py
  stats.py -h | --help

Options:
  -h --help     Show this screen.
"""
from docopt import docopt
from corpus.ancora import SimpleAncoraCorpusReader
from collections import defaultdict
import time


def max_d(d):
    k = 0
    m = 0
    for key in d:
        if d[key] >= m:
            k = key
            m = d[key]
    return tuple([k] + [m])

def find(val, l):
    out = -1
    try:
        out = l.index(val)
    except:
        pass

    return out

if __name__ == '__main__':
    opts = docopt(__doc__)

    init_time = time.clock()
    # load the data
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/')
    sents = corpus.tagged_sents()

    # compute the statistics
    cant_sents = len(sents)
    words = defaultdict(int)
    tags = defaultdict(int)
    ambiguity = defaultdict(set)
    cant_occ_words = 0
    for sent in sents:
        cant_occ_words += len(sent)
        for s in sent:
            words[s[0]] += 1
            tags[s[1]] += 1
            ambiguity[s[0]].add(s[1])
    cant_words = len(words)
    cant_tags = len(tags)
    cant_occ_tags = cant_occ_words
    tags_most_frec = {}
    tmf = []
    aux = tags.copy()
    for x in range(10):
        k, m = max_d(aux)
        t = tuple([k] + [m])
        tags_most_frec[x + 1] = t
        tmf.append(k)
        aux.pop(k)
    words_most_frec = defaultdict(dict)
    for sent in sents:
        for s in sent:
            index = find(s[1], tmf)
            if index != -1:
                if s[0] not in words_most_frec[tmf[index]]:
                    words_most_frec[tmf[index]][s[0]] = 0
                words_most_frec[tmf[index]][s[0]] += 1
    print('sents:', cant_sents)
    print('occ words:', cant_occ_words)
    print('words:', cant_words)
    print('tags:', cant_tags)
    print('#|tag| frec | total percentage | most freccuent words for tag')
    for pos in tags_most_frec:
        tag, frec = tags_most_frec[pos]
        aux = words_most_frec[tag].copy()
        wmf = []
        for x in range(5):
            k, m = max_d(aux)
            if k in aux:
                wmf.append(k)
                # Aqui se podria guardar estas palabras que se pierden
                # despues del print
                aux.pop(k)
        print(pos, tag, frec, float(frec) / cant_occ_tags, wmf)
    ambiguous = defaultdict(int)
    for x in ambiguity.values():
        cant = len(x)
        if cant == 1:
            ambiguous[1] += 1
        elif cant == 2:
            ambiguous[2] += 1
        elif cant == 3:
            ambiguous[3] += 1
        elif cant == 4:
            ambiguous[4] += 1
        elif cant == 5:
            ambiguous[5] += 1
        elif cant == 6:
            ambiguous[6] += 1
        elif cant == 7:
            ambiguous[7] += 1
        elif cant == 8:
            ambiguous[8] += 1
        elif cant == 9:
            ambiguous[9] += 1
    ambiguous_list = list(ambiguous.values())
    print('unambiguous', ambiguous[1])
    print('ambiguous 2-9', sum(ambiguous_list[1:]))
    for i, x in enumerate(ambiguous_list[1:]):
        print('\t{} tags: {}'.format(i + 1, x))

    final_time = time.clock()
    print('time lapsed:', final_time - init_time)
