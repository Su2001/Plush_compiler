
from ply import lex as lex


tokens = (
    'NUMBER', 'VAL', 'VAR', 'DEF', 'REAL',
    'MINUS','TIMES','DIVIDE','EQ', 'ASSIGN',
    'LPAREN','RPAREN', 'END', 'PLUS',
    'INT', 'STRING', 'FLOAT', 'BOOL', 'AND', 
    'OR', 'NEQ', 'GTEQ', 'GT',
    'LT', 'LTEQ', 'MOD', 'VOID',
    'LSQBRAC','RSQBRAC','LCBRAC','RCBRAC',
    'NEG', 'BOOLV', 'FUNCTION','STRINGV', 'COMMA',
    'MUL', 'ID', 'IF', 'ELSE', 'WHILE', 'NEWARRAY', 'CHARV', 'CHAR'
    )

# Tokens
t_COMMA             = r','
t_NEG               = r'!'
t_MUL               = r'\^'
t_AND               = r'&&'
t_OR                = r'\|\|'
t_NEQ               = r'!='
t_GTEQ              = r'>='
t_GT                = r'>'
t_LT                = r'<'
t_LTEQ              = r'<='
t_MOD              = r'%'
t_DEF               = r':'
t_ASSIGN            = r':='
t_MINUS             = r'-'
t_TIMES             = r'\*'
t_PLUS              = r'\+'
t_DIVIDE            = r'/'
t_EQ                = r'=='
t_LPAREN            = r'\('
t_RPAREN            = r'\)'
t_LSQBRAC           = r'\['
t_RSQBRAC           = r'\]'
t_LCBRAC            = r'\{'
t_RCBRAC            = r'\}'
t_END               = r'\;'

reservedKeywords = (
    "if",
    "else",
    "while",
    "val",
    "var",
    "function",
    "void",
    "int",
    "float",
    "bool",
    "string",
    "char",
    "newarray"
)

states = (
    ("comment", "exclusive"),
    ("string", "exclusive"),
    ("escapeString", "exclusive"),  

)

def t_BOOLV(t):
    r'true|false'
    return t

def t_CHARV(t):
    r"(\'([^\\\'])\')|(\"([^\\\"])\")"
    return t

def t_ID(t):
    r"[a-zA-Z][a-zA-Z_0-9]*"
    if t.value in reservedKeywords:
        t.type = t.value.upper()
    return t

def t_REAL(t):  
    r"(\d*\.\d+)" 
    print(t.value) 
    t.value = float(t.value)  
    return t

def t_NUMBER(t):
    r'(\d+|_)+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t







# Reads a string
def t_string(t):
    # Reads the first character " and jumps to the string state
    r"\""
    t.lexer.string_start = t.lexer.lexpos
    t.lexer.begin("string")


def t_string_word(t):
    r"[^\\\"\n]+"


def t_string_notWord(t):
    r"((\\n)|(\\t)|(\\\^c)|(\\[0-9][0-9][0-9])|(\\\")|(\\\\))+"


# If the lexer reads the beginning of a MULtiline string, enter special state
def t_string_specialCase(t):
    r"\\"
    t.lexer.special_start = t.lexer.lexpos
    t.lexer.begin("escapeString")


def t_escapeString_finish(t):
    r"\\"
    t.lexer.begin("string")


def t_string_STRING(t):
    # Reads the second character " and returns the STRING token
    r"\""
    t.value = t.lexer.lexdata[t.lexer.string_start - 1 : t.lexer.lexpos]
    t.type = "STRINGV"
    t.lexer.begin("INITIAL")
    return t 


def t_comment(t):
    r"\#"
    t.lexer.code_start = t.lexer.lexpos
    t.lexer.level = 1
    t.lexer.begin("comment")


def t_comment_begin(t):
    r"\#"
    t.lexer.level += 1
    pass


def t_comment_COMMENT(t):
    r"(?!\/\*|\*\/)\S+"
    pass


def t_comment_end(t):
    r"\n"
    t.lexer.level -= 1

    if t.lexer.level == 0:
        t.lexer.begin("INITIAL")

# Define a rule so we can track line numbers
def t_INITIAL_comment_escapeString_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ANY_ignore = " \t"

# Error handling rule
def t_ANY_error(t):
    print("Illegal character '%s' in line '%s'" % (t.value[0], t.lineno))



# lexer = lex.lex()
# raw_input = "val actual_min : int := \"hdjka\";"
# file_input = "plush_testsuite/0_valid/maxRangeSquared.pl"
# if __name__ == "__main__":

#     f = open(file_input, "r")
#     data = f.read()
#     f.close()
#     print(data)
#     data += raw_input
#     lex.input(data)
#     t = 1
#     # Tokenize
#     while True:
#         tok = lex.token()
#         if  not tok :
#             break  # No more input
#         print(tok)