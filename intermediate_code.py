from semantic_cube import SemanticCube
from quadruple import Quadruple

class IntermediateCode:
    def __init__(self):
        self.p_operators = []
        self.p_operands = []
        self.p_types = []
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
            right_operator = self.p_operands.pop()
            left_operator = self.p_operands.pop()

            right_operator_type = type(right_operator).__name__
            left_operator_type = type(left_operator).__name__
            
            if self.sc.cube[operator][right_operator_type][left_operator_type] == 'err':
                raise TypeError(f"unsupported operand type(s) for {operator}: '{left_operator}' and '{right_operator}'")

            quad = Quadruple(operator, left_operator, right_operator, 'temp')
            self.quadruples.append(quad)
