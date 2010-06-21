
import ply.yacc

from lexer import tokens


class ABNF(object):
    pass


class ABNFSyntax(object):
    pass


class RuleList(ABNFSyntax):

    def __init__(self, rule):
        if rule != Terminal.NEWLINE:
            self.list = [ rule ]
        else:
            self.list = []

    def __str__(self):
        s = "RuleList: "
        for child in self.list:
            s += "["
            s += str(child)
            s += "] "
        return s

    def append(self, rule):
        if rule != Terminal.NEWLINE:
            self.list += [ rule ]


class Terminal(ABNFSyntax):
    pass
Terminal.NEWLINE = Terminal()


def p_rulelist(p):
    "rulelist : rule_or_newline"
    p[0] = RuleList( p[1] )

def p_rulelist_(p):
    "rulelist : rulelist rule_or_newline "
    p[1].append( p[2] )
    p[0] = p[1]

def p_rule_or_newline(p):
    "rule_or_newline : rule"
    p[0] = p[1]

def p_rule_or_newline_(p):
    "rule_or_newline : NEWLINE"
    p[0] = Terminal.NEWLINE

def p_rule(p):
    "rule : rulename defined-as elements NEWLINE"
    p[0] = ( 'rule', p[1], p[2], p[3] )

def p_rulename(p):
    "rulename : IDENT"
    p[0] = p[1]

def p_defined_as(p):
    """defined-as : EQ
                  | EQSLASH"""
    p[0] = p[1]

def p_elements(p):
    "elements : IDENT"
    p[0] = p[1]

def parser():
    return ply.yacc.yacc()

