"""Convert file to single line.

Usage:
  reader.py -i <folder>
  reader.py -h | --help

Options:
  -i <file>     Input data file.
  -h --help     Show this screen.
"""
from docopt import docopt
import glob
from os import listdir, walk, chdir
from os.path import isfile, join
__author__ = 'Ezequiel Medina'

if __name__ == '__main__':
    opts = docopt(__doc__)
    in_folder = opts['-i']
    out = open(join(in_folder, 'data.csv'), 'w')
    out.write('document_id,document_text\n')

    for dir in listdir(in_folder):
        path = join(in_folder, dir)
        for (dirpath, dirnames, filenames) in walk(path):
            for file in filenames:
                if isfile(join(path, file)):
                    name, ext = file.split('.')
                    if ext == 'txt' and 'BAT' not in name:
                        p = join(dirpath, name + '.' + ext)
                        f = open(p, 'r')
                        data = f.readlines()
                        plain_data = ''.join(data)
                        plain_data = plain_data.replace('\n', ' ')
                        out.write('"' + name + '",' + repr(plain_data) + '\n')
                        f.close()
    out.close()
