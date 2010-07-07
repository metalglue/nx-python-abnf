
import abnf.parser

def normalize_defined_as(ast):
    def merge(a, b):
        return abnf.parser.Rule( a.rulename,
                                 abnf.parser.DefinedAs.EQ,
                                 reduce( lambda x, y: x + y, b.alternation, a.alternation ) )
    name_to_rule = {}
    for x in ast:
        if x.rulename not in name_to_rule:
            if x.defined_as == abnf.parser.DefinedAs.EQSLASH:
                raise Exception( "Syntax Error at line %d." % ( x.alternation._list[0].lineno ) )
            name_to_rule[ x.rulename ] = x
        else:
            if x.defined_as == abnf.parser.DefinedAs.EQ:
                raise Exception( "Syntax Error at line %d." % ( x.alternation._list[0].lineno ) )
            name_to_rule[ x.rulename ] = merge( name_to_rule[ x.rulename ], x )
    return reduce( lambda x, y: x + y, name_to_rule.itervalues(), abnf.parser.Rulelist([]) )


class Rulelist(object):
    def __init__(self, rulelist):
        self.rulelist = rulelist
        self._list = []
    def __iter__(self):
        return iter(self._list)

class Rule(object):
    def __init__(self, rule):
        self.rule = rule
        self._list = []
    def __str__(self):
        return str( self.rule )
    def __iter__(self):
        return iter(self._list)

class Definition(object):
    def __init__(self, concatenation):
        self.concatenation = concatenation
        self.refs = []
    def __str__(self):
        return "%s" % ( self.concatenation )
    def __iter__(self):
        return iter( self.refs )

class Reference(object):
    def __init__(self, rulename, rule):
        self.rulename = rulename
        self.rule = rule
    def __str__(self):
        if self.rule:
            return "Reference %s" % ( self.rulename )
        else:
            return "Unresolved Reference %s" % ( self.rulename )
    def __iter__(self):
        return
        yield


def show(rulelist):
    def visit(x, indent=0):
        print "%s%s" % ( "  " * indent, x )
        for i in x:
            visit(i, indent + 1)
    for rule in rulelist:
        visit(rule)

def f(ast, rulename_rule_map):
    def visit_xxx(x, definition):
        if isinstance( x, abnf.parser.RulenameElement ):
            definition.refs = definition.refs + [ Reference( x.rulename, rulename_rule_map.get( x.rulename, None ) ) ]
        for xx in x:
            visit_xxx(xx, definition)
    def visit_concatenation(concatenation):
        definition = Definition(concatenation)
        for repetition in concatenation:
            visit_xxx(repetition, definition)
        return definition
    def visit_rule(rule):
        definitions = [ visit_concatenation(concatenation) for concatenation in rule.alternation ]
        r = Rule(rule)
        r._list = definitions
        return r
    rulelist = Rulelist(ast)
    rulelist._list = [ visit_rule(rule) for rule in rulename_rule_map.itervalues() ]
    show(rulelist)

def analyze(ast):
    ast = normalize_defined_as(ast)
    rulename_rule_map = dict( ( ( x.rulename, x ) for x in ast ) )
    f(ast, rulename_rule_map)
    return ast

