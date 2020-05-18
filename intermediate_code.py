from semantic_cube import SemanticCube
from quadruple import Quadruple

class IntermediateCode:
    def __init__(self):
        self.p_operators = []
        self.p_operands = []
        self.p_types = []
        self.p_jumps = []
        self.quadruples = []
        self.sc = SemanticCube()
        self.scope = 'global'
        self.cont_temp = 0;
    
    def push_operator(self, operator):
        self.p_operators.append(operator)
    
    #Genera cuadruplos para operaciones aritmeticas
    def quad_arithmetic(self):
        if self.p_operators == []:
            return
        if self.p_operators[-1] in ['*', '/', '+', '-']:
            operator = self.p_operators.pop()
            right_operando = self.p_operands.pop()
            print(self.p_operands)
            left_operando = self.p_operands.pop()
            print(self.p_operands)

            right_operando_type = type(right_operando).__name__
            left_operando_type = type(left_operando).__name__
            
            # if self.sc.cube[operator][right_operando_type][left_operando_type] == 'err':
            #     raise TypeError(f"unsupported operand type(s) for {operator}: '{left_operando}' and '{right_operando}'")

            quad = Quadruple(operator, left_operando, right_operando, 'temp')
            self.p_operands.append('temp')
            print(self.p_operands)
            self.quadruples.append(quad)

    def quad_assignment(self):
        if self.p_operators == []:
            return
        
        print("entre perro")
        operator = self.p_operators.pop()
        right_operando = self.p_operands.pop()
        print(self.p_operands)
        left_operando = self.p_operands.pop()
        print(self.p_operands)
        
        quad = Quadruple(operator, right_operando, None, left_operando )

        self.quadruples.append(quad)
        print(self.p_operands)