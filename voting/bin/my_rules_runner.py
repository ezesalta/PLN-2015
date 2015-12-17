"""
Run IEPY rule-based extractor

Usage:
    my_rules_runner.py
    my_rules_runner.py -h | --help | --version

Picks from rules.py the relation to work with, and the rules definitions and
proceeds with the extraction.

Options:
  -h --help             Show this screen
  --version             Version number
"""
import sys
import logging
from django.core.exceptions import ObjectDoesNotExist
import iepy
iepy.setup(__file__)
from iepy.extraction.rules import load_rules
from iepy.extraction.rules_core import RuleBasedCore
from iepy.data import models, output
from iepy.data.db import CandidateEvidenceManager

from voting.webapp.models import Label
__author__ = 'Ezequiel Medina'


def run_from_command_line():
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    try:
        #relation_name = iepy.instance.rules.RELATION
        pass
    except AttributeError:
        logging.error("RELATION not defined in rules file")
        sys.exit(1)

    try:
        #relation = models.Relation.objects.get(name=relation_name)
        relations = models.Relation.objects.all()
    except ObjectDoesNotExist:
        #logging.error("Relation {!r} not found".format(relation_name))
        sys.exit(1)

    # Load rules
    #rules = load_rules()
    for relation in relations:
        rules = [getattr(iepy.instance.rules, relation.name)]
        if len(rules) == 0:
            continue

        # Load evidences
        evidences = CandidateEvidenceManager.candidates_for_relation(relation)

        # Run the pipeline
        iextractor = RuleBasedCore(relation, rules)
        iextractor.start()
        iextractor.process()
        predictions = iextractor.predict(evidences)
        # Save labeling
        print('Saving labels...')
        for pred in predictions:
            if len(Label.objects.filter(evidence=pred, relation=relation)) == 0:
                l = Label()
                l.evidence = pred
                l.label = predictions[pred]
                l.relation = relation
                l.save()
    #output.dump_output_loop(predictions)


if __name__ == u'__main__':
    run_from_command_line()
