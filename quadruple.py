class Quadruple: 
    '''
    Clase para representar la estructura de un cuadruplo
    '''
    def __init__(self, operator, left_oper, right_oper, result):
        self.operator = operator
        self.left_oper = left_oper
        self.right_oper = right_oper
        self.result = result
    
    '''
    Funcion para representar como queremos que se desplieguen los objetos Quadruple cuando se haga print
    '''
    def __repr__(self):
        return f"<Quadruple {self.operator}, {self.left_oper}, {self.right_oper}, {self.result}>\n"
