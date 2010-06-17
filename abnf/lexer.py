
import ply.lex


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


def Lexer():

    t_IDENT = r"[A-Za-z][A-Za-z0-9-]*"

    t_NEWLINE = r"\n"

    t_INTEGER = r"[0-9]+"

    t_STRING = r"\"[^"]*\""

    t_VALUE = r"%[bdx][A-Z0-9.-]+"

    t_MINUS = r"-"
    
    t_EQ = r"="

    t_EQSLASH = r"=/"

    t_SEMI = r";"

    t_SLASH = r"/"

    t_STAR = r"\*"

    t_LPAREN = r"("

    t_RPAREN = r")"

    t_LBRACKET = r"["

    t_RBRACKET = r"]"

