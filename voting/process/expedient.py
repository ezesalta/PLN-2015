__author__ = 'Ezequiel Medina'
import codecs

from iepy.data.models import Entity, EntityOccurrence

from voting.process.regexp_ner import RegExpNERRunner, options_re, options_file_re,\
    upperletters_re, lowerletters_re, tokenized_re


class ExpedientNERRunner(RegExpNERRunner):

    def __init__(self, override=False):
        # TODO: write this regexp!

        self.regexp = regexp = u'(?P<<expedient>><[0-9]{1,4}-[A-Z]{1,4}-[0-9]{2,4}>)'

        super(ExpedientNERRunner, self).__init__('expedient', regexp, override)

    def process_match(self, match):
        expedient = ' '.join(match.group('expedient'))

        kind = self.label
        offset, offset_end = match.span()
        entity_oc = self.build_occurrence(expedient, kind, expedient, offset, offset_end)

        return entity_oc
