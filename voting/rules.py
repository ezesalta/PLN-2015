# Write here your rules
# RELATION = 'your relation here'

from refo import Question, Star, Any, Plus
from iepy.extraction.rules import rule, Token, Pos, Kind

RELATION = "person_vote"

@rule(True)
def begin_with_person(Subject, Object):
    anything = Star(Any())
    #return Subject + anything + Object
    #return anything + Subject + anything + Object + anything
    return Subject + Kind("PARTY") + anything + Object

@rule(True)
def in_the_middle(Subject, Object):
    anything = Star(Any())
    return anything + Subject + Kind("PARTY") + anything + Object



"""RELATION = "person_party"

@rule(True)
def from_party(Subject, Object):
    anything = Star(Any())
    return Subject + Object"""
