#!/usr/bin/env python

import abnf.lexer
import abnf.parser

def test_(parser, lexer, text):
    pass

def test_lex(parser, lexer, text):
    lexer.input(text)
    while True:
        token = lexer.token()
        if not token:
            break
        print token

def test(parser, lexer, text):
    p = parser.parse(text, lexer=lexer)
    print p

def test2(p):
    def visit(p):
        def escape(s):
            return s.replace('"', '\\"')
        print 'node%d [ label = "%s" ];' % ( id(p), escape(str(p)) )
        for i in p:
            print 'node%d -> node%d;' % ( id(p), id(i) )
        for i in p:
            visit(i)
    print "digraph sample {"
    print "graph [ rankdir=LR, nodesep=0.1, ranksep=0.7 ];"
    print "node [ fontsize=8, shape=box, width=0, height=0 ];"
    for x in p:
        visit(x)
    print "}"

def test3(parse, lexer, text):
    def normalize_defined_as(p):
        def merge(a, b):
            return abnf.parser.Rule( a.rulename,
                                     abnf.parser.DefinedAs.EQ,
                                     reduce( lambda x, y: x + y, b.alternation, a.alternation ) )
        name_to_rule = {}
        for x in p:
            if x.rulename not in name_to_rule:
                if x.defined_as == abnf.parser.DefinedAs.EQSLASH:
                    raise Exception( "Syntax Error at line %d." % ( x.alternation._list[0].lineno ) )
                name_to_rule[ x.rulename ] = x
            else:
                if x.defined_as == abnf.parser.DefinedAs.EQ:
                    raise Exception( "Syntax Error at line %d." % ( x.alternation._list[0].lineno ) )
                name_to_rule[ x.rulename ] = merge( name_to_rule[ x.rulename ], x )
        return reduce( lambda x, y: x + y, name_to_rule.itervalues(), abnf.parser.Rulelist([]) )
    p = parser.parse(text, lexer=lexer, tracking=True)
    p = normalize_defined_as(p)
    test2(p)

lexer = abnf.lexer.lexer()
parser = abnf.parser.parser()
test3(parser, lexer, """
        rule = rulename
        rule =/ rulename
""")
test_(parser, lexer, """

         rule           =  rulename defined-as elements c-nl
                                ; continues if next line starts
                                ;  with white space

         rulename       =  ALPHA *(ALPHA / DIGIT / "-")

         defined-as     =  *c-wsp ("=" / "=/") *c-wsp
                                ; basic rules definition and
                                ;  incremental alternatives

         elements       =  alternation *c-wsp

         c-wsp          =  WSP / (c-nl WSP)

         c-nl           =  comment / CRLF
                                ; comment or newline

         comment        =  ";" *(WSP / VCHAR) CRLF

         alternation    =  concatenation
                           *(*c-wsp "/" *c-wsp concatenation)

         concatenation  =  repetition *(1*c-wsp repetition)

         repetition     =  [repeat] element

         repeat         =  1*DIGIT / (*DIGIT "*" *DIGIT)

         element        =  rulename / group / option /
                           char-val / num-val / prose-val

         group          =  "(" *c-wsp alternation *c-wsp ")"

         option         =  "[" *c-wsp alternation *c-wsp "]"

         char-val       =  DQUOTE *(%x20-21 / %x23-7E) DQUOTE
                                ; quoted string of SP and VCHAR
                                ;  without DQUOTE

         num-val        =  "%" (bin-val / dec-val / hex-val)

         bin-val        =  "b" 1*BIT
                           [ 1*("." 1*BIT) / ("-" 1*BIT) ]
                                ; series of concatenated bit values
                                ;  or single ONEOF range

         dec-val        =  "d" 1*DIGIT
                           [ 1*("." 1*DIGIT) / ("-" 1*DIGIT) ]

         hex-val        =  "x" 1*HEXDIG
                           [ 1*("." 1*HEXDIG) / ("-" 1*HEXDIG) ]

""")

