import codecs
from iepy.data.models import Entity, EntityOccurrence
from voting.process.regexp_ner import RegExpNERRunner, options_re, options_file_re,\
    upperletters_re, lowerletters_re, tokenized_re


class PersonNERRunner(RegExpNERRunner):

    def __init__(self, override=False):
        # TODO: write this regexp!
        print('holas')

        #surname_re = upperletters_re('surname')
        surname_re = u'(?P<<surname>><[A-ZÁÉÍÓÚÑ]*>)'
        #surnames_re = u'(?P<<surname>><{}*\s{}*>)'.format(upperletter, upperletter)

        #name_re = lowerletters_re('name')
        name_re = u'(?P<<name>><[A-ZÁÉÍÓÚÑ][a-záéíóúñ]*>)'

        regexp = surname_re + u'<,>' + name_re

        super(PersonNERRunner, self).__init__('person', regexp, override)

    def process_match(self, match):
        #surname = ' '.join(match.group('surname'))
        name = ' '.join(match.group('name'))
        #complete_name = name + ' ' + surname
        kind = self.label
        entity, created = Entity.objects.get_or_create(key=name, kind=kind,
                                                       defaults={'canonical_form': name})
        offset, offset_end = match.span()
        entity_oc = EntityOccurrence(entity=entity, offset=offset, offset_end=offset_end)

        return entity_oc

    def run_ner(self, doc):
        RegExpNERRunner