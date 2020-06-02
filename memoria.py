from collections import OrderedDict
'''
    Clase Memoria para emular la memoria en ejecucion
    - mem_global:  guarda variables o temporales globales
    - mem_local: guarda variables o temporales locales
    - mem_consantes: guarda todas las constantes
    - mem_ejec: guarda las funciones que se estan ejecutando
    - active: funcion/memoria activa
    - base_fun: direccion base de funcions
'''

class Memoria:

    def __init__(self):

        self.mem_global = {}
        self.mem_local = {}
        self.mem_constantes = {}

        self.mem_ejec = OrderedDict()
        self.active = None
        self.base_func = 40000
        self.counter = 0


    '''
        Funcion activar nueva memoria local de una funcion en la llamada
        y se agrega a la memoria de ejeucion
        :param superior -> Funcion que se llama
        :param size -> cantidad de variable de la funcion
    '''
    def mem_func(self, superior, size):

        if self.counter + size > 40000:
            raise TypeError("Desbordamiento de pila")

        actual = MemoriaLocal(superior, size)
        dir = self.base_func + self.counter
        self.mem_ejec[dir] = actual
    
    '''
        Elimina el scope de memoria local actual
    '''
    def remove_scope(self):

        if self.active is not None:
            if self.active.superior is not self:
                self.active = self.active.superior
            else:
                self.active = None
            
            func = list(self.mem_ejec.keys())[-1]
            self.counter -= self.mem_ejec[func].size
            self.mem_ejec[func]

# Clase MemoriaLocal que utiliza la clase Memoria
'''
    mem_local: variables de la memoria local
    counter: base de donde empieza la memoria local
    c_int: contador de enteros (base)
    c_float: contador de flotantes (base)
    c_str: contador de strings (base)
    superior: la memoria local actual
    size = tamaño de que utilizara
'''
class MemoriaLocal:

    def __init__(self, superior, size):
        self.mem_local = {}
        self.counter = 21000

        self.c_int = 0
        self.c_float = 4000
        self.c_str = 8000

        self.superior = superior
        self.size = size
    
    '''
        Asigna valores de parametros a la funcio
        :param params -> Lista de parametros
    '''
    def assign_params(self, params):
        
        for p in params:
            if type(p) is int:
                self.mem_local[self.counter+self.c_int] = p
                self.c_int += 1
            elif type(p) is float:
                self.mem_local[self.counter+self.c_float] = p
                self.c_float += 1
            else:
                self.mem_local[self.counter+self.c_str] = p
                self.c_str += 1
            
