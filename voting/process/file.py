__author__ = 'Ezequiel Medina'
import codecs

from iepy.data.models import Entity, EntityOccurrence

from voting.process.regexp_ner import RegExpNERRunner, options_re, options_file_re,\
    upperletters_re, lowerletters_re, tokenized_re


class FileNERRunner(RegExpNERRunner):

    def __init__(self, override=False):
        # TODO: write this regexp!

        self.regexp = regexp = u'(?P<<file>><[0-9]{1,4}-[A-Z]{1,4}-[0-9]{2,4}>)'

        super(FileNERRunner, self).__init__('file', regexp, override)

    def process_match(self, match):
        votes = ' '.join(match.group('file'))

        kind = self.label
        offset, offset_end = match.span()
        entity_oc = self.build_occurrence(votes, kind, votes, offset, offset_end)

        return entity_oc
