# Write here your rules
# RELATION = 'your relation here'

from refo import Question, Star, Any, Plus
from iepy.extraction.rules import rule, Token, Pos, Kind

RELATION = ""

@rule(True)
def person_vote(Subject, Object):
    anything = Star(Any())
    #return Subject + anything + Object
    #return anything + Subject + anything + Object + anything
    return Subject + Kind("PARTY") + anything + Object


@rule(True)
def person_party(Subject, Object):
    anything = Star(Any())
    return Subject + Object
