
import ply.yacc

from lexer import tokens


def p_rulelist(p):
    "rulelist : rule"

def p_rulelist_(p):
    "rulelist : rulelist rule"

def p_rule(p):
    "rule : rulename defined-as alternation NEWLINE"

def p_rulename(p):
    "rulename : IDENT"

def p_defined_as(p):
    "defined-as : EQ"

def p_defined_as_(p):
    "defined-as : EQSLASH"

def p_alternation(p):
    "alternation : concatenation"

def p_alternation_(p):
    "alternation : alternation SLASH concatenation"

def p_concatenation(p):
    "concatenation : repetition"

def p_concatenation_(p):
    "concatenation : concatenation repetition"

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
    return ply.yacc.yacc()

