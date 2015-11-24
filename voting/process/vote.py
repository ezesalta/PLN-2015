__author__ = 'Ezequiel Medina'
import codecs

from iepy.data.models import Entity, EntityOccurrence

from voting.process.regexp_ner import RegExpNERRunner, options_re, options_file_re,\
    upperletters_re, lowerletters_re, tokenized_re


class VoteNERRunner(RegExpNERRunner):

    def __init__(self, override=False):
        # TODO: write this regexp!

        #extras = u'(?P<<extras>>\\n\\n)'
        extras = u'(?P<<extras>>.*|\\n*)'

        regexp = u'(?P<<votes>><AFIRMATIVO>|<NEGATIVO>|<ABSTENCION>|<AUSENTE>)'

        super(VoteNERRunner, self).__init__('vote', regexp, override)

    def process_match(self, match):
        votes = ' '.join(match.group('votes'))

        kind = self.label
        offset, offset_end = match.span()
        entity_oc = self.build_occurrence(votes, kind, votes, offset, offset_end)

        return entity_oc
