from semantic_cube import SemanticCube
from quadruple import Quadruple
from virtual_memory import VirtualMemory

class IntermediateCode:
    def __init__(self):
        self.p_operators = []
        self.p_operands = []
        self.p_types = []
        self.p_jumps = []
        self.quadruples = [Quadruple('GOTO', None, None, None)]
        self.sc = SemanticCube()
        self.scope = 'global'
        self.cont_temp = 0
        self.p_dim = {}
        self.cont_dim = 0
        self.cont_param = 0
    
    def push_operator(self, operator):
        self.p_operators.append(operator)
    
    #Genera cuadruplos para operaciones aritmeticas y condicionales
    def quad_arit_cond(self):
        operator = self.p_operators.pop()
        right_operando = self.p_operands.pop()
        left_operando = self.p_operands.pop()

        right_type = self.p_types.pop()
        left_type = self.p_types.pop()

        result_type = self.sc.cube[operator][right_type][left_type]
        
        if result_type  == 'err':
            raise TypeError(f"unsupported operand type(s) for {operator}: '{left_type}' and '{right_type}'")
            
        result = VirtualMemory().getDir(self.scope, True, result_type)

        quad = Quadruple(operator, left_operando, right_operando, result)

        self.p_operands.append(result)
        self.p_types.append(result_type)
        self.quadruples.append(quad)

    def quad_assignment(self):
        operator = self.p_operators.pop()
        right_operando = self.p_operands.pop()
        left_operando = self.p_operands.pop()
        
        quad = Quadruple(operator, right_operando, None, left_operando )

        self.quadruples.append(quad)
    
    def quad_statement(self):
        exp_type = self.p_types.pop()
        if exp_type != 'bool':
            raise TypeError("Type Mismatch")
        
        result = self.p_operands.pop()
        quad = Quadruple('GOTOF', result, None, None)
        self.quadruples.append(quad)
        self.p_jumps.append(len(self.quadruples) - 1)
    
    def end_condition(self):
        end = self.p_jumps.pop()
        self.quadruples[end].result = len(self.quadruples) + 1
    
    def quad_sino(self):
        quad = Quadruple('GOTO', None, None, None)
        self.quadruples.append(quad)
        false = self.p_jumps.pop()
        self.p_jumps.append(len(self.quadruples) - 1)
        self.quadruples[false].result = len(self.quadruples) + 1

    def end_mientras(self):
        end = self.p_jumps.pop()
        return_goto = self.p_jumps.pop()

        quad = Quadruple('GOTO', None, None, return_goto)
        self.quadruples.append(quad)

        self.quadruples[end].result = len(self.quadruples) + 1
    
    def end_func_quad(self):
        quad = Quadruple('ENDFUNC', None, None, None)
        self.quadruples.append(quad)
    
    def escribe_quad(self):

        result = self.p_operands.pop() 
        quad = Quadruple('ESCRIBE', None, None, result)

        self.quadruples.append(quad)

    def leer_quad(self, var):
        quad = Quadruple('LEER', None, None, var)
        self.quadruples.append(quad)
    
    def era_quad(self, size):
        quad = Quadruple('ERA', None, None, size)
        self.quadruples.append(quad)
    
    def desde_incremento_quad(self):
        var = self.p_operands.pop()
        
        constant_dir = VirtualMemory().addConstant(1, 'int')

        result = VirtualMemory().getDir(self.scope, True, 'int')
        quad = Quadruple('+', var, constant_dir , result)
        self.quadruples.append(quad)
        quad = Quadruple('=', result, None, var)
        self.quadruples.append(quad)
    
    def quad_gotov(self):
        exp_type = self.p_types.pop()
        if exp_type != 'bool':
            raise TypeError("Type Mismatch")
        
        result = self.p_operands.pop()
        quad = Quadruple('GOTOV', result, None, None)
        self.quadruples.append(quad)
        self.p_jumps.append(len(self.quadruples) - 1)

    def quad_verify_index(self, var_dimensions, dim):
        
        quad = Quadruple('VERIF', self.p_operands[-1], None, var_dimensions[dim]['dims'])
        self.quadruples.append(quad)

        if len(var_dimensions) == 2 and dim == 0:
            aux = self.p_operands.pop()
            result = VirtualMemory().getDir(self.scope, True, 'int')
            const_dim_address = VirtualMemory().addConstant(var_dimensions[dim]['mdim'], 'int')
            quad = Quadruple('*', aux, const_dim_address, result)
            self.quadruples.append(quad)
            self.p_operands.append(result)

        if dim > 0:
            aux2 = self.p_operands.pop()
            aux1 = self.p_operands.pop()
            result = VirtualMemory().getDir(self.scope, True, 'int')
            quad = Quadruple('+', aux1, aux2, result)
            self.quadruples.append(quad)
            self.p_operands.append(result)
        
    def quad_end_array_access(self, address):
        aux1 = self.p_operands.pop()
        result = VirtualMemory().getDir(self.scope, True, 'int')
        result = '('+str(result)+')'
        quad = Quadruple('+', aux1, address, result)
        self.quadruples.append(quad)

        self.p_operands.append(result)

        self.p_operators.pop()
    
    def quad_param(self, arg_func_type):
        argument = self.p_operands.pop()
        argument_type = self.p_types.pop()

        if argument_type != arg_func_type:
            raise TypeError("El tipo de argumento no es igual tipo del parametro")
            
        quad = Quadruple('PARAM', argument, None, self.cont_param+1)

        self.quadruples.append(quad)
    
    def quad_gosub(self, quad_func):
        quad = Quadruple('GOSUB', None, None, quad_func)
        self.quadruples.append(quad)
    
    def format_quads(self):
        quad = Quadruple('END', None, None, None)
        self.quadruples.append(quad)
        return [(quad.operator, quad.left_oper, quad.right_oper, quad.result) for quad in self.quadruples]

    def format_consts(self):
        return [(d, v) for d, v in VirtualMemory().mem_constantes.items()]
        
    def function_return(self, tipo_func):
        result_type = self.sc.cube['regresa'][tipo_func][self.p_types.pop()]

        if result_type != 'err':
            quad = Quadruple('REGRESA', None, None, self.p_operands.pop())
            self.quadruples.append(quad)
        else:
            raise TypeError("Return value is different from the one specified in the function")
