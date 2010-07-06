
import ply.yacc

from lexer import tokens


class SyntaxNode(object):
    pass

class Rulelist(SyntaxNode):
    def __init__(self, rule_or_list):
        self._list = rule_or_list if isinstance( rule_or_list, list ) else [ rule_or_list ]
    def __str__(self):
        return "Rulelist"
    def __add__(self, right):
        return Rulelist( self._list + [ right ] )
    def __iter__(self):
        return iter( self._list )

class Rule(SyntaxNode):
    def __init__(self, rulename, defined_as, alternation):
        self.rulename = rulename
        self.defined_as = defined_as
        self.alternation = alternation
    def __str__(self):
        return "Rule %s %s" % ( self.rulename, self.defined_as )
    def __iter__(self):
        yield self.alternation

class DefinedAs(SyntaxNode):
    EQ = "="
    EQSLASH = "=/"

class Alternation(SyntaxNode):
    def __init__(self, rule_or_list):
        self._list = rule_or_list if isinstance( rule_or_list, list ) else [ rule_or_list ]
    def __str__(self):
        return "Alternation"
    def __add__(self, right):
        return Alternation( self._list + [ right ] )
    def __iter__(self):
        return iter( self._list )

class Concatenation(SyntaxNode):
    def __init__(self, lineno, rule_or_list):
        self.lineno = lineno
        self._list = rule_or_list if isinstance( rule_or_list, list ) else [ rule_or_list ]
    def __str__(self):
        return "Concatenation[%d]" % ( self.lineno )
    def __add__(self, right):
        return Concatenation( self.lineno, self._list + [ right ] )
    def __iter__(self):
        return iter( self._list )

class Repetition(SyntaxNode):
    def __init__(self, repeat, element):
        self.repeat = repeat
        self.element = element
    def __str__(self):
        return "Repetition %s" % ( self.repeat )
    def __iter__(self):
        yield self.element

class Repeat(SyntaxNode):
    def __init__(self, from_, to):
        self.from_ = from_
        self.to = to
    def __str__(self):
        if self.from_ is not None and self.from_ == self.to:
            return self.from_
        return "".join( [ ( self.from_ if self.from_ is not None else "" ),
                          "*",
                          ( self.to if self.to is not None else "" ) ] )
    def __iter__(self):
        return
        yield

class RulenameElement(SyntaxNode):
    def __init__(self, rulename):
        self.rulename = rulename
    def __str__(self):
        return "RulenameElement %s" % ( self.rulename )
    def __iter__(self):
        return
        yield

class GroupedElement(SyntaxNode):
    def __init__(self, alternation):
        self.alternation = alternation
    def __str__(self):
        return "GroupedElement" % ( self.alternation )
    def __iter__(self):
        yield self.alternation

class OptionalElement(SyntaxNode):
    def __init__(self, alternation):
        self.alternation = alternation
    def __str__(self):
        return "OptionalElement"
    def __iter__(self):
        yield self.alternation

class LiteralElement(SyntaxNode):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return "LiteralElement %s" % ( self.value )
    def __iter__(self):
        return
        yield


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
    p[0] = Concatenation( p.lineno(1), p[1] )

def p_concatenation_(p):
    "concatenation : concatenation repetition"
    p[0] = p[1] + p[2]

def p_repetition(p):
    "repetition : element"
    p[0] = Repetition( Repeat( "1", "1" ), p[1] )

def p_repetition_(p):
    "repetition : repeat element"
    p[0] = Repetition( p[1], p[2] )

def p_repeat(p):
    "repeat : INTEGER"
    p[0] = Repeat( p[1], p[1] )

def p_repeat_(p):
    "repeat : STAR"
    p[0] = Repeat( None, None )

def p_repeat__(p):
    "repeat : INTEGER STAR"
    p[0] = Repeat( p[1], None )

def p_repeat___(p):
    "repeat : INTEGER STAR INTEGER"
    p[0] = Repeat( p[1], p[3] )

def p_repeat____(p):
    "repeat : STAR INTEGER"
    p[0] = Repeat( p[2], None )

def p_element(p):
    "element : rulename"
    p[0] = RulenameElement( p[1] )

def p_element_(p):
    "element : LPAREN alternation RPAREN"
    p[0] = GroupedElement( p[2] )

def p_element__(p):
    "element : LBRACKET alternation RBRACKET"
    p[0] = OptionalElement( p[2] )

def p_element___(p):
    "element : STRING"
    p[0] = LiteralElement( p[1] )

def p_element____(p):
    "element : VALUE"
    p[0] = LiteralElement( p[1] )


def parser():
    return ply.yacc.yacc(write_tables=0, debug=0)

