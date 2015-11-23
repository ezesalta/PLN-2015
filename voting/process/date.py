import codecs

from iepy.data.models import Entity, EntityOccurrence
from voting.process.regexp_ner import RegExpNERRunner, options_re, options_file_re, optional_re


class DateNERRunner(RegExpNERRunner):

    def __init__(self, override=False):
        day = u'<\d{1,2}>'
        of = u'<de>'
        from_ = u'(<a><partir><del> | <del> | <por><el><lapso> | <desde><el>)'
        to = u'(<al> | <aI> | <y><hasta><el> | <,><hasta><el>)'
        months = 'enero febrero marzo abril mayo junio julio agosto septiembre octubre noviembre diciembre'.split()
        month = options_re(months)
        year = u'<\d{4}>'
        date = day + of + month + optional_re(of + year)
        date_or_day = '(' + date + ' | ' + day + ')'
        regexp = optional_re(from_ + date_or_day + to) + date
        super(DateNERRunner, self).__init__('date', regexp, override)
