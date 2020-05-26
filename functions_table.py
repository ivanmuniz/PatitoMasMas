from virtual_memory import VirtualMemory

class FunctionsTable:
    #TODO2: crear funcion para eliminar vars de las funciones, esto se aplicara cuando termine de hacer el parseo.
    def __init__(self):
        self.table = {
            'global': { 'type': 'void', 'vars': {}, 'params': [] }
        }

    def add_vars(self, function, vars_dec):
        fun_vars = self.table[function]['vars']
        vars_dec = vars_dec.strip().split(';')
        vars_dec.pop()
        
        for vars in vars_dec:
            vars_n_type = vars.strip().split(' ')
            type_vars = vars_n_type[0] 
            if type_vars == "string": 
                type_vars = "str"
            for var in vars_n_type[1].split(','):
                if '[' in var:
                    var = var[:var.find('[')] #esto quita las dimensiones *POR MIENTRAS, CREO QUE DEBEMOS DE GUARDARLAS
                    
                if var in self.table[function]['vars']:
                    raise TypeError("La variable ya existe en el scope")
                

                self.table[function]['vars'][var] = {'type': type_vars, 'dir': VirtualMemory().getDir(function, False, type_vars)}
    
    def add_function(self, function, type):
        self.table[function] = { 'type': type, 'vars': {}, 'params': [], 'quad_no': None }
    
    def add_params(self, function, params):
        for param in params.split(','):
            param_values = param.strip().split(' ')
            var_type = param_values[0]
            var_name = param_values[1]

            if var_type == "string": 
                var_type = "str"

            self.table[function]['vars'][var_name] = {'type': var_type, 'dir': VirtualMemory().getDir(function, False, var_type)}
            self.table[function]['params'].append(var_type)

    def search_var(self, scope, var):
        if var in self.table[scope]['vars']:
            return self.table[scope]['vars'][var]
        elif var in self.table['global']['vars']:
            return self.table['global']['vars'][var]
        else: 
            raise TypeError("La variable no ha sido declarada")
            