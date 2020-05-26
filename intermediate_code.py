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
        while('ESCRIBE' in self.p_operators):
            result = self.p_operands.pop() 
            operator = self.p_operators.pop()
            quad = Quadruple(operator, None, None, result)

            self.quadruples.append(quad)

    def leer_quad(self, var):
        quad = Quadruple('LEER', None, None, var)
        self.quadruples.append(quad)
    
    def era_quad(self):
        quad = Quadruple('ERA', None, None, self.scope)
        self.quadruples.append(quad)