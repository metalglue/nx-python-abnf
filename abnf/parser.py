
import ply.yacc

from lexer import tokens


class SyntaxNode(object):
    pass

class Rulelist(SyntaxNode):
    def __init__(self, rule_or_list):
        self._list = isinstance( rule_or_list, list ) and rule_or_list or [ rule_or_list ]
    def __str__(self):
        return "\n".join( [ "START" ] + [ str(x) for x in self._list ] + [ "END" ] )
    def __add__(self, right):
        return Rulelist( self._list + [ right ] )

class Rule(SyntaxNode):
    def __init__(self, rulename, defined_as, alternation):
        self.rulename = rulename
        self.defined_as = defined_as
        self.alternation = alternation
    def __str__(self):
        return "Rule(%s, %s, %s)" % ( str( self.rulename ), str( self.defined_as ), str( self.alternation ) )

class DefinedAs(SyntaxNode):
    EQ = "="
    EQSLASH = "=/"

class Alternation(SyntaxNode):
    def __init__(self, rule_or_list):
        self._list = isinstance( rule_or_list, list ) and rule_or_list or [ rule_or_list ]
    def __str__(self):
        return " / ".join( [ str(x) for x in self._list ] )
    def __add__(self, right):
        return Alternation( self._list + [ right ] )

class Concatenation(SyntaxNode):
    def __init__(self, rule_or_list):
        self._list = isinstance( rule_or_list, list ) and rule_or_list or [ rule_or_list ]
    def __str__(self):
        return " ".join( [ str(x) for x in self._list ] )
    def __add__(self, right):
        return Concatenation( self._list + [ right ] )


def p_rulelist(p):
    "rulelist : rule"
    p[0] = Rulelist( p[1] )

def p_rulelist_(p):
    "rulelist : rulelist rule"
    p[0] = p[1] + p[2]

def p_rule(p):
    "rule : rulename defined-as alternation NEWLINE"
    p[0] = Rule( p[1], p[2], p[3] )

def p_rulename(p):
    "rulename : IDENT"
    p[0] = p[1]

def p_defined_as(p):
    "defined-as : EQ"
    p[0] = DefinedAs.EQ

def p_defined_as_(p):
    "defined-as : EQSLASH"
    p[0] = DefinedAs.EQSLASH

def p_alternation(p):
    "alternation : concatenation"
    p[0] = Alternation( p[1] )

def p_alternation_(p):
    "alternation : alternation SLASH concatenation"
    p[0] = p[1] + p[3]

def p_concatenation(p):
    "concatenation : repetition"
    p[0] = Concatenation( p[1] )

def p_concatenation_(p):
    "concatenation : concatenation repetition"
    p[0] = p[1] + p[2]

def p_repetition(p):
    "repetition : element"

def p_repetition_(p):
    "repetition : repeat element"

def p_repeat(p):
    "repeat : INTEGER"

def p_repeat_(p):
    "repeat : STAR"

def p_repeat__(p):
    "repeat : INTEGER STAR"

def p_repeat___(p):
    "repeat : INTEGER STAR INTEGER"

def p_repeat____(p):
    "repeat : STAR INTEGER"

def p_element(p):
    "element : rulename"

def p_element_(p):
    "element : LPAREN alternation RPAREN"

def p_element__(p):
    "element : LBRACKET alternation RBRACKET"

def p_element___(p):
    "element : STRING"

def p_element____(p):
    "element : VALUE"


def parser():
    return ply.yacc.yacc(write_tables=0, debug=0)

