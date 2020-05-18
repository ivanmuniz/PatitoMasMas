class FunctionsTable:
    #TODO2: crear funcion para eliminar vars de las funciones, esto se aplicara cuando termine de hacer el parseo.
    def __init__(self):
        self.table = {
            'global': { 'type': 'void', 'vars': {}, 'params': [] }, 
            'principal': { 'type': 'void', 'vars': {}, 'params': [] }
        }

    def add_vars(self, function, vars_dec):
        fun_vars = self.table[function]['vars']
        vars_dec = vars_dec.strip().split(';')
        vars_dec.pop()
        
        for vars in vars_dec:
            vars_n_type = vars.strip().split(' ')
            type_vars = vars_n_type[0]
            for var in vars_n_type[1].split(','):
                if '[' in var:
                    var = var[:var.find('[')] #esto quita las dimensiones *POR MIENTRAS, CREO QUE DEBEMOS DE GUARDARLAS
                    
                if var in self.table[function]['vars']:
                    raise TypeError("La variable ya existe en el scope")
                
                print("AGREGANGO VAR ", var)
                self.table[function]['vars'][var] = {'type': type_vars}
    
    def add_function(self, function, type):
        self.table[function] = { 'type': type, 'vars': {}, 'params': [] }
    
    def add_params(self, function, params):
        for param in params.split(','):
            param_values = param.strip().split(' ')
            var_type = param_values[0]
            var_name = param_values[1]

            self.table[function]['vars'][var_name] = {'type': var_type}
            self.table[function]['params'].append(var_type)

    def search_type(self, scope, var):
        print("TABLOTA:", self.table)
        print(var)
        print(scope)
        if var in self.table[scope]['vars']:
            return self.table[scope]['vars'][var]['type']
        elif var in self.table['global']['vars']:
            return self.table['global']['vars'][var]['type']
        else: 
            raise TypeError("La variable no ha sido declarada")
            