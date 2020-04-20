import ply.lex as lex
import ply.yacc as yacc
import sys

# RESERVED WORDS
reserved = { 
    'programa': 'PROGRAMA',
    'var': 'VAR',
    'int': 'INT',
    'float': 'FLOAT',
    'char': 'CHAR',
    'funcion': 'FUNCION',
    'void': 'VOID',
    'regresa': 'REGRESA',
    'lee': 'LEE',
    'escribe': 'ESCRIBE',
    'si': 'SI',
    'entonces': 'ENTONCES',
    'sino': 'SINO',
    'mientras': 'MIENTRAS',
    'haz': 'HAZ',
    'desde': 'DESDE',
    'hasta': 'HASTA',
    'hacer': 'HACER',
    'principal': 'PRINCIPAL'
}

# LIST OF TOKENS
tokens = [
    'ID', 'MINUS', 'PLUS', 'TIMES', 'DIVIDE',
    'SEMICOLON', 'OPENPAREN', 'CLOSEPAREN',
    'COMMA', 'OPENCURL', 'CLOSECURL', 'COLON', 
    'EQUAL', 'GREATERTHAN', 'LESSTHAN', 'NOTEQUAL',
    'CTEI', 'CTEF', 'CTESTRING', 'CTECHAR',
    'LBRACKET', 'RBRACKET'
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
t_NOTEQUAL = r'\!='
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

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
    r'\'[\w]\''
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z_\d]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Build the lexer
lexer = lex.lex()

def p_programa(p):
    '''
        programa : PROGRAMA ID SEMICOLON declaraciones funciones PRINCIPAL OPENPAREN CLOSEPAREN bloque
    '''

# ----------------------- Declaración de variables ----------------------------------
def p_declaraciones(p):
    '''
        declaraciones : VAR var_dec_type
            | empty
    '''

def p_var_dec_type(p):
    '''
        var_dec_type : tipo var_dec SEMICOLON
            | tipo var_dec SEMICOLON var_dec_type
    '''

def p_var_dec(p):
    '''
        var_dec : ID
            | ID COMMA var_dec
            | ID LBRACKET CTEI RBRACKET
            | ID LBRACKET CTEI RBRACKET COMMA var_dec
            | ID LBRACKET CTEI RBRACKET LBRACKET CTEI RBRACKET
            | ID LBRACKET CTEI RBRACKET LBRACKET CTEI RBRACKET COMMA var_dec

    '''

def p_tipo(p):
    '''
        tipo : INT
            | FLOAT
            | CHAR
    '''
# ------------------------ Termina declaración de variables -------------------------


# ------------------------------------ Funciones ------------------------------------
def p_funciones(p):
    '''
        funciones : FUNCION retorno ID OPENPAREN parametros_funcion CLOSEPAREN declaraciones bloque
            | empty     
    '''

def p_parametros_funcion(p):
    '''
        parametros_funcion : variables_funcion
            | empty
    '''

def p_variables_funcion(p):
    '''
        variables_funcion : tipo ID
            | tipo ID COMMA variables_funcion
    '''

def p_retorno(p):
    '''
        retorno : tipo
            | VOID
    '''
# ---------------------------------- Termina funciones ------------------------------

def p_bloque(p):
    '''
        bloque : OPENCURL CLOSECURL
    '''

def p_empty(p):
    '''
        empty :
    '''
    pass

error = False
def p_error(p):
    global error
    print("Error de sintaxixs en el código")
    error = True

# Build the parser
parser = yacc.yacc()

if len( sys.argv ) < 2:
    print("Por favor especifique el nombre del archivo de texto que desea compilar.\n Ejemplo: python patitomasmas.py prueba.txt")
else:
    file_name = sys.argv[1]

    try:
        f = open( file_name, "r" )
    except FileNotFoundError as e:
        print( e )
        sys.exit()

    parser.parse( f.read() )
    if not error:
        print( "Código correcto" )
    f.close()