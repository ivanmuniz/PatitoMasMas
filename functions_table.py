class FunctionsTable:
    def __init__(self):
        self.table = {
            'global': { 'type': 'void', 'vars': [] }, 
            'principal': { 'type': 'void', 'vars': [] }
        }

    def add_vars(self, function, vars_dec):
        fun_vars = self.table[function]['vars']
        vars_dec = vars_dec.strip().split(';')
        vars_dec.pop()
        
        for vars in vars_dec:
            vars_n_type = vars.strip().split(' ')
            type_vars = vars_n_type[0]
            for var in vars_n_type[1].split(','):
                if any(var in var_fun.values() for var_fun in fun_vars):
                    raise TypeError("La variable ya existe en el scope")
                self.table[function]['vars'].append({'type': type_vars, 'name': var})
    
    def add_function(self, function, type):
        self.table[function] = { 'type': type, 'vars': [] }
    
    def add_params(self, function, params):
        for param in params.split(','):
            param_values = param.strip().split(' ')
            var_type = param_values[0]
            var_name = param_values[1]
            self.table[function]['vars'].append({'type': var_type, 'name': var_name})