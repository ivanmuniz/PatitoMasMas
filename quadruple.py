class Quadruple: 
    def __init__(self, operator, left_oper, right_oper, result):
        self.operator = operator
        self.left_oper = left_oper
        self.right_oper = right_oper
        self.result = result
    
    def __repr__(self):
        return f"<Quadruple {self.operator}, {self.left_oper}, {self.right_oper}, {self.result}>\n"
