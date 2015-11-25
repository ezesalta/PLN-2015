__author__ = 'Ezequiel Medina'
import codecs

from iepy.data.models import Entity, EntityOccurrence

from voting.process.regexp_ner import RegExpNERRunner, options_re, options_file_re,\
    upperletters_re, lowerletters_re, tokenized_re


class GroupNERRunner(RegExpNERRunner):

    def __init__(self, override=False):
        # TODO: write this regexp!
        groups = ['Frente Cívico por Santiago',
                  'Frente para la Victoria - PJ',
                  'Unión Cívica Radical',
                  'Compromiso Federal',
                  'Unión PRO',
                  'U.De.So. Salta',
                  'Partido Socialista',
                  'Movimiento Popular Fueguino',
                  'Fte. Cívico y Social de Catamarca',
                  'Frente Renovador',
                  'Coalición Cívica - ARI - UNEN',
                  'SUMA \+ UNEN',
                  'Unión por Córdoba',
                  'Movimiento Popular Neuquino',
                  'Unión por Entre Ríos',
                  'Unión Celeste y Blanco',
                  'Conservador Popular',
                  'Partido Justicialista La Pampa',
                  'Fte. Renov. de la Conc. Misiones - FPV-PJ',
                  'Frente Nuevo Encuentro',
                  'Coalición Cívica - ARI - UNEN',
                  'Trabajo y Dignidad',
                  'Movimiento Solidario Popular',
                  'Cultura, Educación y Trabajo',
                  'Demócrata de Mendoza',
                  'Frente por la Inclusión Social',
                  'Unidad Popular',
                  'Movimiento Nacional Alfonsinista',
                  'Peronismo mas al Sur',
                  'PTS - Frente de Izquierda',
                  'Libres del Sur',
                  'Fte. de Izquierda y de los Trabajadores',
                  'Proyecto Sur',
                  'GEN',
                  'UNIR',
                  'Fe',
                  'Frente Cívico - Córdoba'
                 ]
        self.groups = groups
        tagged_groups = ['<' + x.replace(' ', '><') + '>' for x in groups]
        self.regexp = regexp = u'(?P<<group>>' + '|'.join(tagged_groups) + ')'

        super(GroupNERRunner, self).__init__('group', regexp, override)

    def process_match(self, match):
        group = ' '.join(match.group('group'))

        kind = self.label
        offset, offset_end = match.span()
        entity_oc = self.build_occurrence(group, kind, group, offset, offset_end)

        return entity_oc
