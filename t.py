#!/usr/bin/env python

import abnf.lexer
import abnf.parser
import abnf.anal

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

def test2(p, lexer, text):
    ast = parser.parse(text, lexer=lexer, tracking=True)
    abnf.parser.show_dot(ast)

def test3(parse, lexer, text):
    ast = parser.parse(text, lexer=lexer, tracking=True)
    ast = abnf.anal.analyze(ast)
    #abnf.parser.show(ast)

lexer = abnf.lexer.lexer()
parser = abnf.parser.parser()
test_(parser, lexer, """
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

test3(parser, lexer, """
PrimaryExpression =
      "this"
    / Identifier
    / Literal
    / ArrayLiteral
    / ObjectLiteral
    / "(" Expression ")"

ArrayLiteral =
      "[" [ Elision ] "]"
    / "[" ElementList "]"
    / "[" ElementList "," [ Elision ] "]"

ElementList =
      [ Elision ] AssignmentExpression
    / ElementList "," [ Elision ] AssignmentExpression

Elision =
      ","
    / Elision ","

ObjectLiteral =
      "{" "}"
    / "{" PropertyNameAndValueList "}"

PropertyNameAndValueList =
      PropertyName ":" AssignmentExpression
    / PropertyNameAndValueList "," PropertyName ":" AssignmentExpression

PropertyName =
      Identifier
    / StringLiteral
    / NumericLiteral

MemberExpression =
      PrimaryExpression
    / FunctionExpression
    / MemberExpression "[" Expression "]"
    / MemberExpression "." Identifier
    / "new" MemberExpression Arguments

NewExpression =
      MemberExpression
    / "new" NewExpression

CallExpression =
      MemberExpression Arguments
    / CallExpression Arguments
    / CallExpression "[" Expression "]"
    / CallExpression "." Identifier

Arguments =
      "(" ")"
    / "(" ArgumentList ")"

ArgumentList =
      AssignmentExpression
    / ArgumentList "," AssignmentExpression

LeftHandSideExpression =
      NewExpression
    / CallExpression

PostfixExpression =
      LeftHandSideExpression
    / LeftHandSideExpression "++"
    / LeftHandSideExpression "--"

UnaryExpression =
      PostfixExpression
    / "delete" UnaryExpression
    / "void" UnaryExpression
    / "typeof" UnaryExpression
    / "++" UnaryExpression
    / "--" UnaryExpression
    / "+" UnaryExpression
    / "-" UnaryExpression
    / "~" UnaryExpression
    / "!" UnaryExpression

MultiplicativeExpression =
      UnaryExpression
    / MultiplicativeExpression "*" UnaryExpression
    / MultiplicativeExpression "/" UnaryExpression
    / MultiplicativeExpression "%" UnaryExpression

AdditiveExpression =
      MultiplicativeExpression
    / AdditiveExpression "+" MultiplicativeExpression
    / AdditiveExpression "-" MultiplicativeExpression

ShiftExpression =
      AdditiveExpression
    / ShiftExpression "<<" AdditiveExpression
    / ShiftExpression ">>" AdditiveExpression
    / ShiftExpression ">>>" AdditiveExpression

RelationalExpression =
      ShiftExpression
    / RelationalExpression "<" ShiftExpression
    / RelationalExpression ">" ShiftExpression
    / RelationalExpression "<=" ShiftExpression
    / RelationalExpression ">=" ShiftExpression
    / RelationalExpression "instanceof" ShiftExpression
    / RelationalExpression "in" ShiftExpression

RelationalExpressionNoIn =
      ShiftExpression
    / RelationalExpression "<" ShiftExpression
    / RelationalExpression ">" ShiftExpression
    / RelationalExpression "<=" ShiftExpression
    / RelationalExpression ">=" ShiftExpression
    / RelationalExpression "instanceof" ShiftExpression

EqualityExpression =
      RelationalExpression
    / EqualityExpression "==" RelationalExpression
    / EqualityExpression "!=" RelationalExpression
    / EqualityExpression "===" RelationalExpression
    / EqualityExpression "!==" RelationalExpression

EqualityExpressionNoIn =
      RelationalExpressionNoIn
    / EqualityExpressionNoIn "==" RelationalExpressionNoIn
    / EqualityExpressionNoIn "!=" RelationalExpressionNoIn
    / EqualityExpressionNoIn "===" RelationalExpressionNoIn
    / EqualityExpressionNoIn "!==" RelationalExpressionNoIn

BitwiseANDExpression =
      EqualityExpression
    / BitwiseANDExpression "&" EqualityExpression

BitwiseANDExpressionNoIn =
      EqualityExpressionNoIn
    / BitwiseANDExpressionNoIn "&" EqualityExpressionNoIn

BitwiseXORExpression =
      BitwiseANDExpression
    / BitwiseXORExpression "^" BitwiseANDExpression

BitwiseXORExpressionNoIn =
      BitwiseANDExpressionNoIn
    / BitwiseXORExpressionNoIn "^" BitwiseANDExpressionNoIn

BitwiseORExpression =
      BitwiseXORExpression
    / BitwiseORExpression "|" BitwiseXORExpression

BitwiseORExpressionNoIn =
      BitwiseXORExpressionNoIn
    / BitwiseORExpressionNoIn "|" BitwiseXORExpressionNoIn

LogicalANDExpression =
      BitwiseORExpression
    / LogicalANDExpression "&&" BitwiseORExpression

LogicalANDExpressionNoIn =
      BitwiseORExpressionNoIn
    / LogicalANDExpressionNoIn "&&" BitwiseORExpressionNoIn

LogicalORExpression =
      LogicalANDExpression
    / LogicalORExpression "||" LogicalANDExpression

LogicalORExpressionNoIn =
      LogicalANDExpressionNoIn
    / LogicalORExpressionNoIn "||" LogicalANDExpressionNoIn

ConditionalExpression =
      LogicalORExpression
    / LogicalORExpression "?" AssignmentExpression ":" AssignmentExpression

ConditionalExpressionNoIn =
      LogicalORExpressionNoIn
    / LogicalORExpressionNoIn "?" AssignmentExpressionNoIn ":" AssignmentExpressionNoIn

AssignmentExpression =
      ConditionalExpression
    / LeftHandSideExpression AssignmentOperator AssignmentExpression

AssignmentExpressionNoIn =
      ConditionalExpressionNoIn
    / LeftHandSideExpression AssignmentOperator AssignmentExpressionNoIn

AssignmentOperator =
      "=" / "*=" / "/=" / "%=" / "+=" / "-=" / "<<=" / ">>=" / ">>>=" / "&=" / "^=" / "|="

Expression =
      AssignmentExpression
    / Expression "," AssignmentExpression

ExpressionNoIn =
      AssignmentExpressionNoIn
    / ExpressionNoIn "," AssignmentExpressionNoIn

Statement =
      Block
    / VariableStatement
    / EmptyStatement
    / ExpressionStatement
    / IfStatement
    / IterationStatement
    / ContinueStatement
    / BreakStatement
    / ReturnStatement
    / WithStatement
    / LabelledStatement
    / SwitchStatement
    / ThrowStatement
    / TryStatement

Block =
      "{" [ StatementList ] "}"

StatementList =
      Statement
    / StatementList Statement

VariableStatement =
      "var" VariableDeclarationList ";"

VariableDeclarationList =
      VariableDeclaration
    / VariableDeclarationList "," VariableDeclaration

VariableDeclarationListNoIn =
      VariableDeclarationNoIn
    / VariableDeclarationListNoIn "," VariableDeclarationNoIn

VariableDeclaration =
      Identifier [ Initialiser ]

VariableDeclarationNoIn =
      Identifier [ InitialiserNoIn ]

Initialiser =
      "=" AssignmentExpression

InitialiserNoIn =
      "=" AssignmentExpressionNoIn

EmptyStatement =
      ";"

ExpressionStatement =
      Expression ";"

IfStatement =
      "if" "(" Expression ")" Statement "else" Statement
    / "if" "(" Expression ")" Statement

IterationStatement =
      "do" Statement "while" "(" Expression ")" ";"
    / "while" "(" Expression ")" Statement
    / "for" "(" [ ExpressionNoIn ] ";" [ Expression ] ";" [ Expression ] ")" Statement
    / "for" "(" "var" VariableDeclarationListNoIn ";" [ Expression ] ";" [ Expression ] ")" Statement
    / "for" "(" LeftHandSideExpression "in" Expression ")" Statement
    / "for" "(" "var" VariableDeclarationListNoIn "in" Expression ")" Statement

ContinueStatement =
      "continue" [ Identifier ] ";"

BreakStatement =
      "break" [ Identifier ] ";"

ReturnStatement =
      "return" [ Expression ] ";"

WithStatement =
      "with" "(" Expression ")" Statement

SwitchStatement =
      "switch" "(" Expression ")" CaseBlock

CaseBlock =
      "{" [ CaseClauses ] "}"
    / "{" [ CaseClauses ] DefaultClause [ CaseClauses ] "}"

CaseClauses =
      CaseClause
    / CaseClauses CaseClause

CaseClause =
      "case" Expression ":" [ StatementList ]

DefaultClause =
      "default" ":" [ StatementList ]

LabelledStatement =
      Identifier ":" Statement

ThrowStatement =
      "throw" Expression ";"

TryStatement =
      "try" Block Catch
    / "try" Block Finally
    / "try" Block Catch Finally

Catch =
      "catch" "(" Identifier ")" Block

Finally =
      "finally" Block

FunctionDeclaration =
      "function" Identifier "(" [ FormalParameterList ] ")" "{" FunctionBody "}"

FunctionExpression =
      "function" [ Identifier ] "(" [ FormalParameterList ] ")" "{" FunctionBody "}"

FormalParameterList =
      Identifier
    / FormalParameterList "," Identifier

FunctionBody =
      SourceElements

Program =
      SourceElements

SourceElements =
      SourceElement
    / SourceElements SourceElement

SourceElement =
      Statement
    / FunctionDeclaration
""")
