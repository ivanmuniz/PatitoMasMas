'''
    Clase que guarda el cubo semantico para verificar las operaciones
'''
class SemanticCube:
    def __init__(self):
        self.cube = {
            '+': {
                'int':{
                    'int': 'int',
                    'float': 'float',
                    'str': 'err',
                    'bool': 'err',
                    'array': 'err'
                },
                'float': {
                    'int': 'float',
                    'float': 'float',
                    'str': 'err',
                    'bool': 'float',
                    'array': 'err'
                },
                'str': {
                    'int': 'err',
                    'float': 'err',
                    'str': 'str',
                    'bool': 'err',
                    'array': 'err'
                },
                'bool': {
                    'int': 'int',
                    'float': 'float',
                    'str': 'err',
                    'bool': 'int',
                    'array': 'err'
                },
                'array': {
                    'array': 'array',
                    'int': 'err',
                    'float':'err',
                    'bool':'err',
                    'str': 'err'
                }
            },
            '-': {
                'int': {
                    'int': 'int',
                    'float': 'float',
                    'str': 'err',
                    'bool': 'int',
                    'array': 'err'
                },
                'float': {
                    'int': 'float',
                    'float': 'float',
                    'str': 'err',
                    'bool': 'float',
                    'array': 'err'
                },
                'str': {
                    'int': 'err',
                    'float': 'err',
                    'str': 'err',
                    'bool': 'err',
                    'array': 'err'
                },
                'bool':{
                    'int': 'int',
                    'float': 'float',
                    'str': 'err',
                    'bool': 'err',
                    'array': 'err'
                },
                'array': {
                    'array': 'array',
                    'int': 'err',
                    'float':'err',
                    'bool':'err',
                    'str': 'err',
                    'array': 'err'
                }
            },
            '/': {
                'int': {
                    'int': 'float',
                    'float': 'float',
                    'str': 'err',
                    'bool': 'float',
                    'array': 'err'
                },
                'float': {
                    'int': 'float',
                    'float': 'float',
                    'str': 'err',
                    'bool': 'float',
                    'array': 'err'
                },
                'str': {
                    'int': 'err',
                    'float': 'err',
                    'str': 'str',
                    'bool': 'float',
                    'array': 'err'
                },
                'bool':{
                    'int': 'float',
                    'float': 'float',
                    'str': 'err',
                    'bool': 'float',
                    'array': 'err'
                },
                'array': {
                    'array': 'err',
                    'int': 'err',
                    'float':'err',
                    'bool':'err',
                    'str': 'err',
                    'array': 'err'
                }
            },
            '*': {
                'int': {
                    'int': 'int',
                    'float': 'float',
                    'str': 'str',
                    'bool': 'int',
                    'array': 'err'
                },
                'float': {
                    'int': 'float',
                    'float': 'float',
                    'str': 'err',
                    'bool': 'float',
                    'array': 'err'
                },
                'str': {
                    'int': 'str',
                    'float': 'err',
                    'str': 'err',
                    'bool': 'err',
                    'array': 'err'
                },
                'bool':{
                    'int': 'int',
                    'float': 'float',
                    'str': 'err',
                    'bool': 'err',
                    'array': 'err'
                },
                'array': {
                    'array': 'array',
                    'int': 'err',
                    'float':'err',
                    'bool':'err',
                    'str': 'err',
                    'array': 'err'
                }
            },
            '>': {
                'int' : {
                    'int' : 'bool',
                    'float' : 'bool',
                    'str' : 'err',
                    'bool' : 'bool'
                },
                'float' : {
                    'int' : 'bool',
                    'float' : 'bool',
                    'str' : 'err',
                    'bool' : 'bool'
                },
                'str' : {
                    'int' : 'err',
                    'float' : 'err',
                    'str' : 'bool',
                    'bool' : 'err'
                },
                'bool' : {
                    'int' : 'bool',
                    'float' : 'bool',
                    'str' : 'err',
                    'bool' : 'bool'
                }
            },
            '<': {
                'int' : {
                    'int' : 'bool',
                    'float' : 'bool',
                    'str' : 'err',
                    'bool' : 'bool'
                },
                'float' : {
                    'int' : 'bool',
                    'float' : 'bool',
                    'str' : 'err',
                    'bool' : 'bool'
                },
                'str' : {
                    'int' : 'err',
                    'float' : 'err',
                    'str' : 'bool',
                    'bool' : 'err'
                },
                'bool' : {
                    'int' : 'bool',
                    'float' : 'bool',
                    'str' : 'err',
                    'bool' : 'bool'
                }
            },
            '>=': {
                'int' : {
                    'int' : 'bool',
                    'float' : 'bool',
                    'str' : 'err',
                    'bool' : 'bool'
                },
                'float' : {
                    'int' : 'bool',
                    'float' : 'bool',
                    'str' : 'err',
                    'bool' : 'bool'
                },
                'str' : {
                    'int' : 'err',
                    'float' : 'err',
                    'str' : 'bool',
                    'bool' : 'err'
                },
                'bool' : {
                    'int' : 'bool',
                    'float' : 'bool',
                    'str' : 'err',
                    'bool' : 'bool'
                }
            },
            '<=': {
                'int' : {
                    'int' : 'bool',
                    'float' : 'bool',
                    'str' : 'err',
                    'bool' : 'bool'
                },
                'float' : {
                    'int' : 'bool',
                    'float' : 'bool',
                    'str' : 'err',
                    'bool' : 'bool'
                },
                'str' : {
                    'int' : 'err',
                    'float' : 'err',
                    'str' : 'bool',
                    'bool' : 'err'
                },
                'bool' : {
                    'int' : 'bool',
                    'float' : 'bool',
                    'str' : 'err',
                    'bool' : 'bool'
                }
            },
            '!=': {
                'int' : {
                    'int' : 'bool',
                    'float' : 'bool',
                    'str' : 'bool',
                    'bool' : 'bool'
                },
                'float' : {
                    'int' : 'bool',
                    'float' : 'bool',
                    'str' : 'bool',
                    'bool' : 'bool'
                },
                'str' : {
                    'int' : 'bool',
                    'float' : 'bool',
                    'str' : 'bool',
                    'bool' : 'bool'
                },
                'bool' : {
                    'int' : 'bool',
                    'float' : 'bool',
                    'str' : 'bool',
                    'bool' : 'bool'
                }
            },
            '&&': {
                'int' : {
                    'int' : 'err',
                    'float' : 'err',
                    'str' : 'err',
                    'bool' : 'err'
                },
                'float' : {
                    'int' : 'err',
                    'float' : 'err',
                    'str' : 'err',
                    'bool' : 'err'
                },
                'str' : {
                    'int' : 'err',
                    'float' : 'err',
                    'str' : 'err',
                    'bool' : 'err'
                },
                'bool' : {
                    'int' : 'err',
                    'float' : 'err',
                    'str' : 'err',
                    'bool' : 'bool'
                }
            },
            '||': {
                'int' : {
                    'int' : 'err',
                    'float' : 'err',
                    'str' : 'err',
                    'bool' : 'err'
                },
                'float' : {
                    'int' : 'err',
                    'float' : 'err',
                    'str' : 'err',
                    'bool' : 'err'
                },
                'str' : {
                    'int' : 'err',
                    'float' : 'err',
                    'str' : 'err',
                    'bool' : 'err'
                },
                'bool' : {
                    'int' : 'err',
                    'float' : 'err',
                    'str' : 'err',
                    'bool' : 'bool'
                }
            },
            '==': {
                'int' : {
                    'int' : 'bool',
                    'float' : 'bool',
                    'str' : 'bool',
                    'bool' : 'bool'
                },
                'float' : {
                    'int' : 'bool',
                    'float' : 'bool',
                    'str' : 'bool',
                    'bool' : 'bool'
                },
                'str' : {
                    'int' : 'bool',
                    'float' : 'bool',
                    'str' : 'bool',
                    'bool' : 'bool'
                },
                'bool' : {
                    'int' : 'bool',
                    'float' : 'bool',
                    'str' : 'bool',
                    'bool' : 'bool'
                }
            },
            'regresa': {
                'int' : {
                    'int' : 'int',
                    'float' : 'err',
                    'str' : 'err',
                    'bool' : 'err'
                },
                'float' : {
                    'int' : 'err',
                    'float' : 'float',
                    'str' : 'err',
                    'bool' : 'err'
                },
                'string' : {
                    'int' : 'err',
                    'float' : 'err',
                    'str' : 'str',
                    'bool' : 'err'
                },
                'bool' : {
                    'int' : 'err',
                    'float' : 'err',
                    'str' : 'err',
                    'bool' : 'bool'
                }
            }
        }    