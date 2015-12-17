# Write here your rules
# RELATION = 'your relation here'

from refo import Question, Star, Any, Plus
from iepy.extraction.rules import rule, Token, Pos, Kind


RELATION = "person_vote"


@rule(True)
def voted_for(Subject, Object):
    """
    Ex: Shamsher M. Chowdhury was born in 1950.
    """
    anything = Star(Any())
    #return anything
    #return anything + Subject + Token("was born") + Pos("IN") + Object + anything
    #return Subject + anything + Object
    #return anything + Subject + anything + Object + anything
    return Subject + Kind("PARTY") + anything + Object
    #return Token("AGUAD") + Token(",") + Token("Oscar") + Token("Raúl") + Token("Unión") + \
           #Token("Cívica") + Token("Radical") + Token("Córdoba") + Token("AFIRMATIVO")
