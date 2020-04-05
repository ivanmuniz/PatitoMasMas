import ply.lex as lex
import ply.yacc as yacc

# RESERVED WORDS
reserved = { 
    'program': 'progam',
    'var': 'VAR',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'function': 'FUNCTION',
    'void': 'VOID',
    'return': 'RETURN',
    'input': 'INPUT',
    'print': 'PRINT',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'while': 'WHILE',
    'do': 'DO',
    'from': 'FROM',
    'until': 'UNTIL',
}

# LIST OF TOKENS
tokens = [
    'ID', 'MINUS', 'PLUS', 'TIMES', 'DIVIDE',
    'SEMICOLON', 'OPENPAREN', 'CLOSEPAREN',
    'COMMA', 'OPENCURL', 'CLOSECURL', 'COLON', 
    'EQUAL', 'GREATERTHAN', 'LESSTHAN', 'NOTEQUAL'
    'CTEI', 'CTEF', 'CTESTRING', 'CTECHAR'
] + list(reserved.values())

t_MINUS = r'\-'
t_PLUS = r'\+'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_SEMICOLON = r'\;'
t_OPENPAREN = r'\('
t_CLOSEPAREN = r'\)'
t_COMMA = r'\,'
t_EQUAL = r'\='
t_OPENCURL = r'\{'
t_CLOSECURL = r'\}'
t_COLON = r'\:'
t_GREATERTHAN = r'\>'
t_LESSTHAN = r'\<'
t_NOTEQUAL = r'\<>'

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\n'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_CTEF(t):
    r'[-+]?\d*\.\d+'
    t.value = float(t.value)
    return t

def t_CTEI(t):
    r'0|[-+]?[1-9][0-9]*'    
    t.value = int(t.value)
    return t

def t_CTESTRING(t):
    r'\'[\w\d\s\,. ]*\'|\"[\w\d\s\,. ]*\"'
    return t

def t_CTECHAR(t):
    r'\w'
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z_\d]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Build the lexer
lexer = lex.lex()