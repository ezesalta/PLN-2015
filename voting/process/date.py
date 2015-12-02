__author__ = 'Ezequiel Medina'
import codecs

from iepy.data.models import Entity, EntityOccurrence

from voting.process.regexp_ner import RegExpNERRunner, options_re, options_file_re,\
    upperletters_re, lowerletters_re, tokenized_re


class DateNERRunner(RegExpNERRunner):

    def __init__(self, override=False):
        # TODO: write this regexp!

        self.regexp = regexp = u'(?P<<date>><[0-9]{1,2}/[0-9]{1,2}/[0-9]{2,4}>)'

        super(DateNERRunner, self).__init__('date', regexp, override)

    def process_match(self, match):
        votes = ' '.join(match.group('date'))

        kind = self.label
        offset, offset_end = match.span()
        entity_oc = self.build_occurrence(votes, kind, votes, offset, offset_end)

        return entity_oc
