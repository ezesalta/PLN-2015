import codecs

from iepy.data.models import Entity, EntityOccurrence

from voting.process.regexp_ner import RegExpNERRunner, options_re, options_file_re,\
    upperletters_re, lowerletters_re, tokenized_re
from voting.process.vote import VoteNERRunner
from voting.process.group import GroupNERRunner


class PersonNERRunner(RegExpNERRunner):

    def __init__(self, override=False):
        # TODO: write this regexp!

        #surname_re = upperletters_re('surname')
        #surnames_re = u'(?P<<surname>><{}*\s{}*>)'.format(upperletter, upperletter)

        vote = VoteNERRunner()
        take_votes = u'(?!' + vote.regexp + u')'
        #take_votes = u'(?P<<votes>>(?!<AFIRMATIVO>|<NEGATIVO>|<ABSTENCION>|<AUSENTE>))'

        group = GroupNERRunner()
        group_words = set()
        for g in group.groups:
            x = g.split(' ')[0]
            group_words.add('<' + x + '>')
        #take_groups = u'(?!' + group.regexp + u')'
        take_groups = u'(?!' + '|'.join(group_words) + u')'

        take_extras = u'(?!<Presentes>|<Ausentes>|<Identificados>)'

        surname_re = take_votes + u'(?P<<surname>><[A-ZÁÉÍÓÚÑ]*>{1,3})'
        #surname_re = u'(?P<<surname>><[A-ZÁÉÍÓÚÑ]*>{1,3})'
        #surname_re = u'<[A-ZÁÉÍÓÚÑ]*>{1,3}'

        #name_re = lowerletters_re('name')
        #name_re = u'(?P<<name>><[A-ZÁÉÍÓÚÑ][a-záéíóúñ]*>{1,3})'
        #name_re = u'(?!<Frente>)' + u'(?P<<name>><[A-ZÁÉÍÓÚÑ][a-záéíóúñ]*>{1,3})'
        #name_re = take_groups + u'(?P<<name>><[A-ZÁÉÍÓÚÑ][a-záéíóúñ]*>{1,3})'
        #name_re = u'<[A-ZÁÉÍÓÚÑ][a-záéíóúñ]*>{1,3}'
        #name_re = u'((?!<Frente>)<[A-ZÁÉÍÓÚÑ][a-záéíóúñ]*>){1,3}'

        name_re = u'(' + take_groups + take_extras + '<[A-ZÁÉÍÓÚÑ][a-záéíóúñ]*>){1,3}'

        self.regexp = regexp = u'(?P<<fullname>>' + surname_re + u'<,>' + name_re + ')'
        #regexp = surname_re + u'<,>' + name_re
        #regexp = u'(?P<<name>><DOMINGUEZ>)'

        super(PersonNERRunner, self).__init__('person', regexp, override)

    def process_match(self, match):
        #surname = ' '.join(match.group('surname'))
        #name = ' '.join(match.group('name'))
        full_name = ' '.join(match.group('fullname'))
        #full_name = full_name.split('\\n')[-1]

        #full_name = surname + ',' + name
        kind = self.label
        offset, offset_end = match.span()
        #entity_oc = self.build_occurrence(name, kind, name, offset, offset_end)
        entity_oc = self.build_occurrence(full_name, kind, full_name, offset, offset_end)

        return entity_oc
