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
                is_array = False
                dimensions = ''
                if '[' in var:
                    is_array = True
                    dimensions = var[var.find('['):]
                    var = var[:var.find('[')]
                    
                if var in self.table[function]['vars']:
                    raise TypeError("La variable ya existe en el scope")
                
                var_dims_n_size = self.get_dimensions(is_array, dimensions)

                var_dir = VirtualMemory().getDir(function, False, type_vars, var_dims_n_size[1])

                self.table[function]['vars'][var] = {
                    'type': type_vars, 
                    'dir': var_dir, 
                    'is_array': is_array,
                    'dimensions': var_dims_n_size[0]
                }
    
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

    def get_dimensions(self, is_array, dimensions):
        if is_array:
            dim = 0
            r = 1
            var_dims = []
            number = ''

            for c in dimensions:
                if c == '[':
                    node = {'dims': None, 'mdim': None}
                elif c == ']':
                    dim += 1
                    node['dims'] = int(number)
                    number = ''
                    var_dims.append(node)
                    r = node['dims'] * r 
                else:
                    number = number + c

            size = r                      
            for i in range(dim):
                mdim = int(r/(var_dims[i]['dims']))
                var_dims[i]['mdim'] = mdim
                r = mdim
            
            var_dims[-1]['mdim'] = 0
            return (var_dims, size)
        else:
            return (None, 1)