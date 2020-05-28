import ply.lex as lex
import ply.yacc as yacc
import sys
from functions_table import FunctionsTable
from intermediate_code import IntermediateCode
from virtual_memory import VirtualMemory

funcs_table = FunctionsTable()
inter_code = IntermediateCode()
memory = VirtualMemory()

# RESERVED WORDS
reserved = { 
    'programa': 'PROGRAMA',
    'var': 'VAR',
    'int': 'INT',
    'float': 'FLOAT',
    'string': 'STRING',
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
        programa : PROGRAMA ID SEMICOLON declaraciones funciones PRINCIPAL punto_principal OPENPAREN CLOSEPAREN bloque
    '''

    print(funcs_table.table)
    
    for (i, quad) in enumerate(inter_code.quadruples, start=1):
        print(i, quad)

    print(memory.mem_constantes)

    p[0] = "PROGRAM COMPILED"

def p_punto_principal(p):
    '''
        punto_principal : 
    '''
    inter_code.quadruples[0].result = len(inter_code.quadruples) + 1

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
            | STRING
    '''
    p[0] = p[1]
# ------------------------ Termina declaración de variables -------------------------


# ------------------------------------ Funciones ------------------------------------
def p_funciones(p):
    '''
        funciones : FUNCION retorno ID punto_meter_funcion OPENPAREN parametros_funcion CLOSEPAREN declaraciones punto_func_quad bloque punto_end_func funciones
            | empty     
    '''

def p_punto_func_quad(p):
    '''
        punto_func_quad : 
    '''
    funcs_table.table[inter_code.scope]['quad_no'] = len(inter_code.quadruples) + 1

def p_punto_end_func(p):
    '''
        punto_end_func : 
    '''
    inter_code.end_func_quad()

def p_punto_meter_funcion(p):
    '''
        punto_meter_funcion : 
    '''
    funcs_table.add_function(p[-1], p[-2])
    inter_code.scope = p[-1]
    memory.resetCounters()

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
        asignacion : variable EQUAL punto_meter_operador exp punto_quad_asignacion SEMICOLON
    '''

def p_punto_quad_asignacion(p):
    '''
        punto_quad_asignacion : 
    '''
    inter_code.quad_assignment()

def p_variable(p):
    '''
        variable : ID punto_meter_operando
            | ID punto_meter_operando LBRACKET punto_arr_1 exp punto_verif_index_quad_1 RBRACKET actualizar_dimension LBRACKET punto_arr_2 exp punto_verif_index_quad_2 RBRACKET punto_end_matriz_acceso
            | ID punto_meter_operando LBRACKET punto_arr_1 exp punto_verif_index_quad_1 RBRACKET punto_end_array_acceso
            
    '''
    p[0] = p[1]


def p_punto_end_array_acceso(p):
    '''
        punto_end_array_acceso : 
    '''
    var = p[-7]
    var_data = funcs_table.search_var(inter_code.scope, var) 
    inter_code.quad_end_array_access(var_data['dir'])

def p_punto_end_matrz_acceso(p):
    '''
        punto_end_matriz_acceso : 
    '''
    var = p[-13]
    var_data = funcs_table.search_var(inter_code.scope, var) 
    inter_code.quad_end_array_access(var_data['dir'])
    inter_code.p_operators.pop()

def p_punto_arr_1(p):
    '''
        punto_arr_1 : 
    '''
    var = p[-3]
    var_data = funcs_table.search_var(inter_code.scope, var)
    
    if not var_data['is_array']:
        raise TypeError("La variable no es un arreglo")
    
    dir_var = var_data['dir']

    inter_code.p_types.pop()

    inter_code.p_dim[dir_var] = inter_code.cont_dim
    inter_code.p_operators.append('(')

def p_punto_arr_2(p):
    '''
        punto_arr_2 : 
    '''
    var = p[-9]
    var_data = funcs_table.search_var(inter_code.scope, var)
    
    if not var_data['is_array']:
        raise TypeError("La variable no es un arreglo")
    
    dir_var = var_data['dir']
    
    inter_code.p_types.pop()

    inter_code.p_dim[dir_var] = inter_code.cont_dim
    inter_code.p_operators.append('(')

def p_punto_verif_index_quad_1(p):
    '''
        punto_verif_index_quad_1 : 
    '''
    var = p[-5]
    var_data = funcs_table.search_var(inter_code.scope, var)
    inter_code.quad_verify_index(var_data['dimensions'], 0)

def p_punto_verif_index_quad_2(p):
    '''
        punto_verif_index_quad_2 : 
    '''
    var = p[-11]
    var_data = funcs_table.search_var(inter_code.scope, var)
    inter_code.quad_verify_index(var_data['dimensions'], 1)

def p_actualizar_dimension(p):
    '''
        actualizar_dimension : 
    '''
    inter_code.cont_dim = inter_code.cont_dim + 1
    inter_code.p_dim[list(inter_code.p_dim)[-1]] = inter_code.cont_dim

def p_expresion(p):
    '''
        expresion : exp
            | exp AND punto_meter_operador expresion punto_quad_cond
            | exp OR punto_meter_operador expresion punto_quad_cond
    '''

def p_exp(p):
    '''
        exp : exp_ar
            | exp_ar exp_condicional punto_meter_operador exp_ar punto_quad_cond
    '''

def p_exp_condicional(p):
    '''
        exp_condicional : GREATERTHAN
        | LESSTHAN
        | GREATEROREQUAL
        | LESSEROREQUAL
        | CEQUAL
        | NOTEQUAL
    '''
    p[0] = p[1]

def p_punto_quad_cond(p):
    '''
        punto_quad_cond : 
    '''
    inter_code.quad_arit_cond()

def p_exp_ar(p):
    '''
        exp_ar : termino punto_quad_arithmetic_exp
            | termino punto_quad_arithmetic_exp PLUS punto_meter_operador exp_ar
            | termino punto_quad_arithmetic_exp MINUS punto_meter_operador exp_ar
    '''

def p_termino(p):
    '''
        termino : factor punto_quad_arithmetic_term
            | factor punto_quad_arithmetic_term TIMES punto_meter_operador termino
            | factor punto_quad_arithmetic_term DIVIDE punto_meter_operador termino
    '''

def p_punto_quad_arithmetic_exp(p):
    '''
        punto_quad_arithmetic_exp : 
    '''
    if inter_code.p_operators != []:
        if inter_code.p_operators[-1] in ['+', '-']:
            inter_code.quad_arit_cond()

def p_punto_quad_arithmetic_term(p):
    '''
        punto_quad_arithmetic_term : 
    '''
    if inter_code.p_operators != []:
        if inter_code.p_operators[-1] in ['*', '/']:
            inter_code.quad_arit_cond()

def p_punto_meter_operador(p):
    '''
        punto_meter_operador : 
    '''
    inter_code.push_operator(p[-1])

def p_factor(p):
    '''
        factor : var_cte punto_meter_operando_constante
            | variable
            | llamada_a_funcion
            | OPENPAREN punto_meter_fondo exp CLOSEPAREN punto_sacar_fondo
    '''
    p[0] = p[1]


def p_punto_meter_fondo(p):
    '''
        punto_meter_fondo : 
    '''
    inter_code.p_operators.append('(')

def p_punto_sacar_fondo(p):
    '''
        punto_sacar_fondo : 
    '''
    fondo = inter_code.p_operators.pop()
    if fondo != '(':
        raise TypeError('No hay fondo')


def p_var_cte(p):
    '''
        var_cte : CTEI
            | CTEF
            | CTESTRING
    '''
    p[0] = p[1]

def p_punto_meter_operando(p):
    '''
        punto_meter_operando : 
    '''
    var = p[-1]

    #Obiente informacion(tipo y direccion) de la variable de la tabla de funciones
    var_data = funcs_table.search_var(inter_code.scope, var)

    #Mete a la pila de operandos la direccion de la variable
    inter_code.p_operands.append(var_data['dir'])

    #Mete a la pila de tipos el tipo de variable
    inter_code.p_types.append(var_data['type'])


def p_punto_meter_operando_constante(p):
    '''
        punto_meter_operando_constante : 
    '''
    dir_constante = memory.addConstant(p[-1], type( p[-1] ).__name__)
    inter_code.p_operands.append(dir_constante)
    inter_code.p_types.append(type(p[-1]).__name__)


def p_condicion(p):
    '''
        condicion : SI OPENPAREN expresion CLOSEPAREN punto_quad_statement ENTONCES bloque punto_end_condition
            | SI OPENPAREN expresion CLOSEPAREN punto_quad_statement ENTONCES bloque SINO punto_quad_sino bloque punto_end_condition
    '''

def p_punto_quad_statement(p):
    '''
        punto_quad_statement :
    '''
    inter_code.quad_statement()

def p_punto_end_condition(p):
    '''
        punto_end_condition : 
    '''
    inter_code.end_condition()

def p_punto_quad_sino(p):
    '''
        punto_quad_sino : 
    '''
    inter_code.quad_sino()

def p_escritura(p):
    '''
        escritura : ESCRIBE OPENPAREN escrituraprime CLOSEPAREN SEMICOLON
    '''
    inter_code.escribe_quad()
    

def p_escrituraprime(p):
    '''
        escrituraprime :
            | CTESTRING punto_meter_operando_constante
            | CTESTRING punto_meter_operando_constante COMMA escrituraprime
            | expresion COMMA escrituraprime
            | expresion

    '''
    inter_code.p_operators.append("ESCRIBE")

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
    var_data = funcs_table.search_var(inter_code.scope, p[1])
    inter_code.leer_quad(var_data['dir'])
    

def p_rep_no_cond(p):
    '''
        rep_no_cond : DESDE variable punto_meter_operando EQUAL punto_meter_operador exp punto_quad_asignacion punto_meter_desde_var HASTA exp punto_desde_gotov HACER bloque punto_desde_incremento
    '''

def p_punto_desde_incremento(p):
    '''
        punto_desde_incremento : 
    '''
    inter_code.desde_incremento_quad()
    inter_code.end_mientras()

def p_punto_desde_gotov(p):
    '''
        punto_desde_gotov : 
    '''
    inter_code.quad_gotov()

def p_punto_meter_desde_var(p):
    '''
        punto_meter_desde_var : 
    '''
    #Obiente informacion(tipo y direccion) de la variable de la tabla de funciones
    var_data = funcs_table.search_var(inter_code.scope, p[-6])

    #Mete a la pila de operandos la direccion de la variable

    if var_data['type'] != 'int':
        raise TypeError('La variable tiene que ser entera para usar el DESDE')

    inter_code.p_operands.append(var_data['dir'])
    inter_code.p_jumps.append(len(inter_code.quadruples) + 1)

def p_rep_cond(p):
    '''
        rep_cond : MIENTRAS punto_mientras OPENPAREN exp CLOSEPAREN punto_quad_statement HAZ bloque punto_end_mientras
    '''

def p_punto_mientras(p):
    '''
        punto_mientras : 
    '''
    inter_code.p_jumps.append(len(inter_code.quadruples) + 1)

def p_punto_end_mientras(p):
    '''
        punto_end_mientras : 
    '''
    inter_code.end_mientras()

def p_llamada_a_funcion(p):
    '''
        llamada_a_funcion : ID punto_verify_func OPENPAREN punto_era_quad CLOSEPAREN
            | ID punto_verify_func OPENPAREN punto_era_quad argumentos_funcion CLOSEPAREN
    '''

def p_punto_era_quad(p):
    '''
        punto_era_quad : 
    '''
    inter_code.era_quad()

def p_punto_verify_func(p):
    '''
        punto_verify_func : 
    '''
    if p[-1] not in funcs_table.table:
        raise TypeError("No existe la funcion")

def p_argumentos_funcion(p):
    '''
        argumentos_funcion : expresion
            |   expresion COMMA argumentos_funcion
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