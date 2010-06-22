
import ply.lex
import re


tokens = (
    "IDENT",
    "NEWLINE",
    "INTEGER",
    "STRING",
    "VALUE",
    "EQ",
    "EQSLASH",
    "SLASH",
    "STAR",
    "LPAREN",
    "RPAREN",
    "LBRACKET",
    "RBRACKET",
)


def lexer_inner():

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

    t_EQ = r"="

    t_EQSLASH = r"=/"

    t_SLASH = r"/"

    t_STAR = r"\*"

    t_LPAREN = r"\("

    t_RPAREN = r"\)"

    t_LBRACKET = r"\["

    t_RBRACKET = r"\]"

    t_ignore = " \t\r"

    t_ignore_COMMENT = ";[^\n]*"

    return ply.lex.lex()


class lexer(object):
    
    def __init__(self):
        self.lexer_inner = lexer_inner()

    def token(self):
        if len( self.list ) > 0:
            return self.list.pop(0)
        if self.state == 2:
            return None
        # Search EQ then search backword NEWLINE IDENT from there
        # In initial state, read until second EQ
        # In intermediate state, self.buf holds "IDENT ... EQ". So read until first EQ
        # After read: i points to the first EQ and j points to the second EQ
        i = len( self.buf )
        if self.state == 0:
            self.state = 1
            while True:
                t = self.lexer_inner.token()
                if not t:
                    raise Exception
                i += 1
                self.buf += [ t ]
                if t.type == "EQ" or t.type == "EQSLASH":
                    break
        j = i
        while True:
            t = self.lexer_inner.token()
            if not t:
                self.state = 2
                break
            j += 1
            self.buf += [ t ]
            if t.type == "EQ" or t.type == "EQSLASH":
                break
        if self.state == 1:
            k = j - 2
            while True:
                if k <= i + 1:
                    raise Exception
                if self.buf[k].type == "IDENT" and self.buf[ k - 1 ].type == "NEWLINE":
                    break
                k -= 1
            self.list = [ x for x in self.buf[ 0 : k - 1 ] if x.type != "NEWLINE" ] + [ self.buf[ k - 1 ] ]
            self.buf[0:k] = []
        else:
            self.list = [ x for x in self.buf[0:-1] if x.type != "NEWLINE" ] + [ self.buf[-1] ]
        return self.list.pop(0)

    def input(self, text):
        self.list = []
        self.state = 0
        self.buf = []
        return self.lexer_inner.input(text)

