import ply.lex as lex
import ply.yacc as yacc
import sys
from functions_table import FunctionsTable
from intermediate_code import IntermediateCode

funcs_table = FunctionsTable()
inter_code = IntermediateCode()

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
    'CEQUAL', 'GREATEROREQUAL', 'LESSEROREQUAL',
    'AND', 'OR','CTEI', 'CTEF', 'CTESTRING', 
    'CTECHAR', 'LBRACKET', 'RBRACKET'
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
t_CEQUAL = r'\=='
t_NOTEQUAL = r'\!='
t_GREATEROREQUAL = r'\>='
t_LESSEROREQUAL = r'\<='
t_AND = r'\&&'
t_OR = r'\|\|'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t\n'

# Error handling rule
def t_error(t):
    print("Illegal character: %s" % t.value[0])
    t.lexer.skip(1)

def t_CTEF(t):
    r'[-+]?\d*\.\d+'
    t.value = float(t.value)
    return t

def t_CTEI(t):
    r'0|[-+]?[1-9][0-9]*'    
    t.value = int(t.value)
    return t

def t_CTECHAR(t):
    r'\'[\w]\'|"[\w]"'
    return t

def t_CTESTRING(t):
    r'"[\w\d\s\,. ]*"|\'[\w\d\s\,. ]*\''
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

    print(funcs_table.table)
    print(inter_code.quadruples)

    p[0] = "PROGRAM COMPILED"

# ----------------------- Declaración de variables ----------------------------------
def p_declaraciones(p):
    '''
        declaraciones : VAR var_dec_type
            | empty
    '''
    if p[1] != None:
       funcs_table.add_vars(inter_code.scope, p[2])

def p_var_dec_type(p):
    '''
        var_dec_type : tipo var_dec SEMICOLON
            | tipo var_dec SEMICOLON var_dec_type
    '''
    p[0] = ''
    for i in range(1, len(p)):
        p[0] += p[i] + ' '

def p_var_dec(p):
    '''
        var_dec : ID
            | ID COMMA var_dec
            | ID LBRACKET CTEI RBRACKET
            | ID LBRACKET CTEI RBRACKET COMMA var_dec
            | ID LBRACKET CTEI RBRACKET LBRACKET CTEI RBRACKET
            | ID LBRACKET CTEI RBRACKET LBRACKET CTEI RBRACKET COMMA var_dec

    '''

    # Esto itera por la gramatica y regresa las variables
    p[0] = ''
    for i in range(1, len(p)):
        p[0] += str(p[i])
    
def p_tipo(p):
    '''
        tipo : INT
            | FLOAT
            | CHAR
    '''
    p[0] = p[1]
# ------------------------ Termina declaración de variables -------------------------


# ------------------------------------ Funciones ------------------------------------
def p_funciones(p):
    '''
        funciones : FUNCION retorno ID punto_meter_funcion OPENPAREN parametros_funcion CLOSEPAREN declaraciones bloque funciones
            | empty     
    '''

def p_punto_meter_funcion(p):
    '''
        punto_meter_funcion : 
    '''
    funcs_table.add_function(p[-1], p[-2])
    inter_code.scope = p[-1]

def p_parametros_funcion(p):
    '''
        parametros_funcion : variables_funcion
            | empty
    '''
    if p[1] != None:
        funcs_table.add_params(inter_code.scope, p[1])


def p_variables_funcion(p):
    '''
        variables_funcion : tipo ID
            | tipo ID COMMA variables_funcion
    '''
    p[0] = ''
    for i in range(1, len(p)):
        p[0] += p[i] + " "

def p_retorno(p):
    '''
        retorno : tipo
            | VOID
    '''
    p[0] = p[1]
# ---------------------------------- Termina funciones ------------------------------

def p_bloque(p):
    '''
        bloque : OPENCURL CLOSECURL
            | OPENCURL estatutosprime CLOSECURL
    '''

def p_estatutosprime(p):
    '''
        estatutosprime : estatutos
            | estatutos estatutosprime
    '''

def p_estatutos(p):
    '''
        estatutos : asignacion
            | condicion
            | escritura
            | retorno_de_funcion
            | lectura
            | rep_no_cond
            | rep_cond
            | llamada_a_funcion_void
    '''

def p_asignacion(p):
    '''
        asignacion : variable meter_variable_asignacion EQUAL punto_meter_operador exp punto_quad_asignacion SEMICOLON
    '''

def p_meter_variable_asignacion(p):
    '''
        meter_variable_asignacion : 
    '''
    inter_code.p_operands.append(p[-1])

def p_punto_quad_asignacion(p):
    '''
        punto_quad_asignacion : 
    '''
    print("asignacion ", inter_code.p_operands)
    inter_code.quad_assignment()

def p_variable(p):
    '''
        variable : ID
            | ID LBRACKET exp RBRACKET punto_agregar_dimension 
            | ID LBRACKET exp RBRACKET punto_agregar_dimension LBRACKET exp RBRACKET punto_agregar_dimension 
    '''
    p[0] = p[1]

def p_punto_agregar_dimension(p):
    '''
        punto_agregar_dimension : 
    '''
    inter_code.p_operands.pop()
    print(inter_code.p_operands)

def p_expresion(p):
    '''
        expresion : exp
            | exp AND expresion
            | exp OR expresion
    '''

def p_exp(p):
    '''
        exp : exp_ar
            | exp_ar GREATERTHAN exp_ar
            | exp_ar LESSTHAN exp_ar
            | exp_ar GREATEROREQUAL exp_ar
            | exp_ar LESSEROREQUAL exp_ar
            | exp_ar CEQUAL exp_ar
            | exp_ar NOTEQUAL exp_ar
    '''

def p_exp_ar(p):
    '''
        exp_ar : termino punto_quad_arithmetic
            | termino punto_quad_arithmetic PLUS punto_meter_operador exp_ar
            | termino punto_quad_arithmetic MINUS punto_meter_operador exp_ar
    '''

def p_termino(p):
    '''
        termino : factor punto_quad_arithmetic
            | factor punto_quad_arithmetic TIMES punto_meter_operador termino
            | factor punto_quad_arithmetic DIVIDE punto_meter_operador termino
    '''

def p_punto_quad_arithmetic(p):
    '''
        punto_quad_arithmetic : 
    '''
    inter_code.quad_arithmetic()

def p_punto_meter_operador(p):
    '''
        punto_meter_operador : 
    '''
    inter_code.push_operator(p[-1])

def p_factor(p):
    '''
        factor : var_cte punto_meter_operando_constante
            | variable punto_meter_operando
            | llamada_a_funcion
            | OPENPAREN exp CLOSEPAREN
    '''
    p[0] = p[1]

def p_var_cte(p):
    '''
        var_cte : CTEI
            | CTEF
            | CTECHAR
    '''
    p[0] = p[1]

def p_punto_meter_operando(p):
    '''
        punto_meter_operando : 
    '''
    var = p[-1]
    inter_code.p_operands.append(var)
    operand_type = funcs_table.search_type(inter_code.scope, var)
    inter_code.p_types.append(operand_type)
    print(inter_code.p_operands)

def p_punto_meter_operando_constante(p):
    '''
        punto_meter_operando_constante : 
    '''
    print(p[-1])
    inter_code.p_operands.append(p[-1])
    inter_code.p_types.append(type(p[-1]).__name__)
    print(inter_code.p_operands)


def p_condicion(p):
    '''
        condicion : SI OPENPAREN expresion CLOSEPAREN ENTONCES bloque
            | SI OPENPAREN expresion CLOSEPAREN ENTONCES bloque SINO bloque
    '''

def p_escritura(p):
    '''
        escritura : ESCRIBE OPENPAREN escrituraprime CLOSEPAREN SEMICOLON
    '''

def p_escrituraprime(p):
    '''
        escrituraprime : expresion
            | expresion COMMA escrituraprime
            | CTESTRING
            | CTESTRING COMMA escrituraprime

    '''

def p_retorno_de_funcion(p):
    '''
        retorno_de_funcion : REGRESA OPENPAREN exp CLOSEPAREN SEMICOLON
    '''

def p_lectura(p):
    '''
        lectura : LEE OPENPAREN lecturaprime CLOSEPAREN SEMICOLON
    '''

def p_lecturaprime(p):
    '''
        lecturaprime : variable
            | variable COMMA lecturaprime
    '''

def p_rep_no_cond(p):
    '''
        rep_no_cond : DESDE variable EQUAL exp HASTA exp HACER bloque
    '''

def p_rep_cond(p):
    '''
        rep_cond : MIENTRAS OPENPAREN exp CLOSEPAREN HAZ bloque
    '''

def p_llamada_a_funcion(p):
    '''
        llamada_a_funcion : ID OPENPAREN CLOSEPAREN
            | ID OPENPAREN argumentos_funcion CLOSEPAREN
    '''

def p_argumentos_funcion(p):
    '''
        argumentos_funcion : tipo ID
            |   tipo ID COMMA argumentos_funcion
    '''

def p_llamada_a_funcion_void(p):
    '''
        llamada_a_funcion_void : llamada_a_funcion SEMICOLON
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