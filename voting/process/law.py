__author__ = 'Ezequiel Medina'
import codecs

from iepy.data.models import Entity, EntityOccurrence

from voting.process.regexp_ner import RegExpNERRunner, options_re, options_file_re,\
    upperletters_re, lowerletters_re, tokenized_re


class LawNERRunner(RegExpNERRunner):

    def __init__(self, override=False):
        # TODO: write this regexp!
        #law = u'<Observaciones><:>(<[^(\.)].*>)*<\.>(?P<<law>><.*>+)'

        law = u'<LEY>(?P<<law>><[^-].*>+)<->'
        #law = u'(?<=<LEY>)(?P<<law>><.*>+)(?=<->)'

        #law = u'<LEY>(?P<<law>><.*>+)(<APROBADO>|<DESAPROBADO>|<SANCIONADO>)'
        self.regexp = regexp = law

        super(LawNERRunner, self).__init__('law', regexp, override)

    def process_match(self, match):
        law = ' '.join(match.group('law'))

        kind = self.label
        offset, offset_end = match.span()
        entity_oc = self.build_occurrence(law, kind, law, offset, offset_end)

        return entity_oc
