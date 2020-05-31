from collections import OrderedDict

class Memoria:

    def __init__(self):

        self.mem_global = {}
        self.mem_local = {}
        self.mem_constantes = {}

        self.mem_ejec = OrderedDict()
        self.active = None
        self.base_func = 40000
        self.counter = 0

    def mem_func(self, superior, size):

        if self.counter + size > 40000:
            raise TypeError("Stack Overflow")

        actual = MemoriaLocal(superior, size)
        dir = self.base_func + self.counter
        self.mem_ejec[dir] = actual
    
    def remove_scope(self):

        if self.active is not None:
            if self.active.superior is not self:
                self.active = self.active.superior
            else:
                self.active = None
            
            func = list(self.mem_ejec.keys())[-1]
            self.counter -= self.mem_ejec[func].size
            self.mem_ejec[func]

class MemoriaLocal:

    def __init__(self, superior, size):
        self.mem_local = {}
        self.counter = 21000

        self.c_int = 0
        self.c_float = 5000
        self.c_str = 8000

        self.superior = superior
        self.size = size
    

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
            
