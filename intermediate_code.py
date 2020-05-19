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

            right_type = self.p_types.pop()
            left_type = self.p_types.pop()

            result_type = self.sc.cube[operator][right_type][left_type]
            
            if result_type  == 'err':
                raise TypeError(f"unsupported operand type(s) for {operator}: '{left_type}' and '{right_type}'")
            
            quad = Quadruple(operator, left_operando, right_operando, result_type)
            self.p_operands.append(result_type) #meter direccion(?)
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
    
    def quad_cond(self):
        print(self.p_operands)
        right_operando = self.p_operands.pop()
        left_operando = self.p_operands.pop()
        right_type = self.p_types.pop()
        left_type = self.p_types.pop()

        print(self.p_operands)
        operator = self.p_operators.pop()

        result_type = self.sc.cube[operator][right_type][left_type]

        if result_type  == 'err':
            raise TypeError(f"unsupported operand type(s) for {operator}: '{left_type}' and '{right_type}'")

        quad = Quadruple(operator, left_operando, right_operando, result_type)
        self.p_operands.append(result_type) #meter direccion(?)
        print(self.p_operands)
        self.quadruples.append(quad)