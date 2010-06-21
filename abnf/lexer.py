
import ply.lex
import re


tokens = (
    "IDENT",
    "NEWLINE",
    "INTEGER",
    "STRING",
    "VALUE",
    "MINUS",
    "EQ",
    "EQSLASH",
    "SEMI",
    "SLASH",
    "STAR",
    "LPAREN",
    "RPAREN",
    "LBRACKET",
    "RBRACKET",
)


def lexer():

    t_IDENT = r"[A-Za-z][A-Za-z0-9-]*"

    def t_NEWLINE(t):
        r"\n+"
        t.lexer.lineno += len( t.value )
        return t

    t_INTEGER = r"[0-9]+"

    t_STRING = r"\"[^\"]*\""

    def t_VALUE(t):
        r"%[bdx][A-Z0-9.-]+"
        if t.value[1] == "b":
            base = 2
            digits = r"[01]+"
        elif t.value[1] == "d":
            base = 10
            digits = r"[0-9]+"
        elif t.value[1] == "x":
            base = 16
            digits = r"[0-9A-F]+"
        else:
            raise NotImplementedError()
        # read first figure
        mo = re.match( digits, t.value[2:] )
        if not mo:
            raise NotImplementedError()
        v = [ int( mo.group(0), base ) ]
        pos = 2 + len( mo.group(0) )
        if pos < len( t.value ):
            # read remaining figures if exist
            if t.value[pos] == "-":
                # range expression such as "%d20-30"
                mo = re.match( digits, t.value[ pos + 1 : ] )
                if not mo:
                    raise NotImplementedError()
                v = range( v[0], int( mo.group(0), base ) + 1 )  # "+ 1" means end point is inclusive
            elif t.value[pos] == ".":
                # enum expression such as "%d20.30.40"
                v += [ int(x, base) for x in t.value[ pos + 1 : ].split(".") ]
            else:
                raise NotImplementedError()
        t.value = v
        return t

    t_MINUS = r"-"
    
    t_EQ = r"="

    t_EQSLASH = r"=/"

    t_SEMI = r";"

    t_SLASH = r"/"

    t_STAR = r"\*"

    t_LPAREN = r"\("

    t_RPAREN = r"\)"

    t_LBRACKET = r"\["

    t_RBRACKET = r"\]"

    t_ignore = " \t\r"

    t_ignore_COMMENT = ";[^\n]*"

    return ply.lex.lex()

