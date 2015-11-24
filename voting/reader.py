"""Convert file to single line.

Usage:
  reader.py -i <file> [-o <file>]
  reader.py -h | --help

Options:
  -i <file>     Input data file.
  -o <file>     Output plain data file.
  -h --help     Show this screen.
"""
from docopt import docopt
import sys
__author__ = 'Ezequiel Medina'

if __name__ == '__main__':
    opts = docopt(__doc__)
    in_file = opts['-i']
    out_file = opts['-o']
    if out_file is None:
        out_file = in_file + '_plain'
    f = open(in_file, 'r')
    data = f.readlines()
    f.close()

    plain_data = ''.join(data)
    plain_data = plain_data.replace('\n', ' ')
    f = open(out_file, 'w')
    f.write(repr(plain_data))
    f.close()