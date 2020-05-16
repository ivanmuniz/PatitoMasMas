class SemanticCube:
    def __init__(self):
        # TODO: incluir chars
        self.cube = {
            '+': {
                'int':{
                    'int': 'int',
                    'float': 'float',
                    'str': 'err',
                    'bool': 'int',
                },
                'float': {
                    'int': 'float',
                    'float': 'float',
                    'str': 'err',
                    'bool': 'float'
                },
                'str': {
                    'int': 'err',
                    'float': 'err',
                    'str': 'str',
                    'bool': 'err'
                },
                'bool': {
                    'int': 'int',
                    'float': 'float',
                    'str': 'err',
                    'bool': 'int'
                }
            },
            '-': {
                'int': {
                    'int': 'int',
                    'float': 'float',
                    'str': 'err',
                    'bool': 'int'
                },
                'float': {
                    'int': 'float',
                    'float': 'float',
                    'str': 'err',
                    'bool': 'float'
                },
                'str': {
                    'int': 'err',
                    'float': 'err',
                    'str': 'err',
                    'bool': 'err'
                },
                'bool':{
                    'int': 'int',
                    'float': 'float',
                    'str': 'err',
                    'bool': 'err'
                }
            },
            '/': {
                'int': {
                    'int': 'float',
                    'float': 'float',
                    'str': 'err',
                    'bool': 'float'
                },
                'float': {
                    'int': 'float',
                    'float': 'float',
                    'str': 'err',
                    'bool': 'float'
                },
                'str': {
                    'int': 'err',
                    'float': 'err',
                    'str': 'str',
                    'bool': 'float'
                },
                'bool':{
                    'int': 'float',
                    'float': 'float',
                    'str': 'err',
                    'bool': 'float'
                }
            },
            '*': {
                'int': {
                    'int': 'int',
                    'float': 'float',
                    'str': 'str',
                    'bool': 'int'
                },
                'float': {
                    'int': 'float',
                    'float': 'float',
                    'str': 'err',
                    'bool': 'float'
                },
                'str': {
                    'int': 'str',
                    'float': 'err',
                    'str': 'err',
                    'bool': 'err'
                },
                'bool':{
                    'int': 'int',
                    'float': 'float',
                    'str': 'err',
                    'bool': 'err'
                }
            },
            # TODO: Faltan los condicionales
            '>': {},
            '<': {},
            '&&': {},
            '||': {}
        }