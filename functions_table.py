class FunctionsTable:
    def __init__(self):
        self.table = {
            'global': { 'type': 'void', 'vars': [] }, 
            'principal': { 'type': 'void', 'vars': [] }
        }
        self.status = { 'current_fun': 'global' }

    def add_vars(self, vars, type):
        fun_vars = self.table[self.status['current_fun']]['vars']
        for var in vars.split(','):
            if any(var in var_fun.values() for var_fun in fun_vars):
                return -1
            self.table[self.status['current_fun']]['vars'].append({'type': type, 'name': var})
    
    def add_function(self, function, type):
        self.status['current_fun'] = function
        self.table[function] = { 'type': type, 'vars': [] }
    
    def add_params(self, params):
        for param in params.split(','):
            param_values = param.strip().split(' ')
            var_type = param_values[0]
            var_name = param_values[1]
            self.table[self.status['current_fun']]['vars'].append({'type': var_type, 'name': var_name})