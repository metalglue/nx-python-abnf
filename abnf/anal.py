
import abnf.parser

def show(ast):
    def visit(x, indent=0):
        print "%s%s" % ( "  " * indent, x )
        for xx in x:
            visit( xx, indent + 1 )
    for rule in ast:
        visit(rule)

def show_dot(ast):
    def visit(x):
        def escape(s):
            return s.replace('"', '\\"')
        print 'node%d [ label = "%s" ];' % ( id(x), escape(str(x)) )
        for i in x:
            print 'node%d -> node%d;' % ( id(x), id(i) )
        for i in x:
            visit(i)
    print "digraph sample {"
    print "graph [ rankdir=LR, nodesep=0.1, ranksep=0.7 ];"
    print "node [ fontsize=8, shape=box, width=0, height=0 ];"
    for x in ast:
        visit(x)
    print "}"

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

def analyze(ast):
    ast = normalize_defined_as(ast)
    return ast

