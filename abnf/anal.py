
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
        return iter( self._list )

class Rule(object):
    def __init__(self, rule):
        self.rule = rule
        self._list = []
        self.refs = []
    def __str__(self):
        return self.rule.rulename
    def __iter__(self):
        return iter( self._list )

class Definition(object):
    def __init__(self, concatenation):
        self.concatenation = concatenation
        self.refs = []
    def __str__(self):
        return "%d" % ( self.concatenation.lineno )
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
            return "%s" % ( self.rulename )
    def __iter__(self):
        return
        yield


def show(rulelist):
    def visit(x, indent=0):
        print "%s%s" % ( "  " * indent, x )
        for i in x:
            visit( i, indent + 1 )
    for rule in rulelist:
        visit(rule)

def show_dot(rulelist):
    def visit(x):
        def escape(s):
            return s.replace( '"', '\\"' )
        print 'node%d [ label = "%s" ];' % ( id(x), escape( str(x) ) )
        if isinstance(x, Definition):
            print 'node%d [ shape=box ];' % ( id(x) )
        for i in x:
            if isinstance(i, Reference) and i.rule is not None:
                print 'node%d -> node%d;' % ( id(x), id( i.rule ) )
            else:
                print 'node%d -> node%d;' % ( id(x), id(i) )
        for i in x:
            if not isinstance(i, Reference) or i.rule is None:
                visit(i)
    print "digraph sample {"
    # print "graph [ rankdir=LR, nodesep=0.1, ranksep=0.7 ];"
    print "node [ fontsize=8, shape=ellipse, width=0, height=0 ];"
    print "edge [ arrowsize=0.5 ];"
    for x in rulelist:
        visit(x)
    # print "{ rank=same; ",
    # for x in rulelist:
    #     print "node%d " % ( id(x) ),
    # print "}"
    print "}"

def show_dot2(rulelist):
    def escape(s):
        return s.replace( '"', '\\"' )
    print "digraph sample {"
    # print "graph [ rankdir=LR, nodesep=0.1, ranksep=0.7 ];"
    print "node [ fontsize=8, shape=ellipse, width=0, height=0 ];"
    print "edge [ arrowsize=0.5 ];"
    for rule in rulelist:
        print 'node%d [ label = "%s" ];' % ( id(rule), escape( str(rule) ) )
        for ref in rule.refs:
            if ref.rule is not None:
                print 'node%d -> node%d;' % ( id(rule), id( ref.rule ) )
            else:
                print 'node%d [ label = "%s", shape=box ];' % ( id(ref), escape( str(ref) ) )
                print 'node%d -> node%d;' % ( id(rule), id(ref) )
    print "}"

def f(ast):
    def create_reference(rulename):
        if rulename in unresolved_refs_map:
            return unresolved_refs_map[rulename]
        elif rulename in rulename_rule_map:
            return Reference( rulename, rulename_rule_map[rulename] )
        else:
            r = Reference(rulename, None)
            unresolved_refs_map[rulename] = r
            return r
    def visit_xxx(x, definition):
        if isinstance( x, abnf.parser.RulenameElement ):
            if not filter( lambda i: i.rulename == x.rulename, definition.refs ):
                definition.refs = definition.refs + [ create_reference( x.rulename ) ]
        for xx in x:
            visit_xxx(xx, definition)
    def visit_concatenation(concatenation):
        definition = Definition(concatenation)
        for repetition in concatenation:
            visit_xxx(repetition, definition)
        return definition
    def visit_rule(rule):
        definitions = [ visit_concatenation(concatenation) for concatenation in rule.rule.alternation ]
        rule._list = definitions
        return rule
    unresolved_refs_map = {}
    rulename_rule_map = dict( ( ( rule.rulename, Rule(rule) ) for rule in ast ) )
    rulelist = Rulelist(ast)
    rulelist._list = [ visit_rule(rule) for rule in rulename_rule_map.itervalues() ]
    rulelist = g(rulelist)
    show_dot(rulelist)
    return rulelist

def g(rulelist):
    for rule in rulelist:
        refs = reduce( lambda x, y: x + y,
                       ( definition.refs for definition in ( definition for definition in rule ) ),
                       [] )
        for ref in refs:
            if not filter( lambda i: i.rulename == ref.rulename, rule.refs ):
                rule.refs = rule.refs + [ ref ]
    return rulelist

def analyze(ast):
    ast = normalize_defined_as(ast)
    f(ast)
    return ast

