import json
import numpy as np
from memoria import Memoria

class MaquinaVirtual:
    def __init__(self):
        self.program = None
        self.memoria = Memoria()

        self.pila_contextos = []
    
    '''
        Procesa la informacion del json con informacion del codigo intermedio
        :param program -> nombre de programa
    '''
    def process(self, program):
        compiled = f"pruebas/{program}_comp.cuac"
        
        compiled_file = open(compiled, 'r')

        compiled_data = json.load(compiled_file)

        self.pila_contextos.append('main')
        self.program = program

        self.process_consts(compiled_data['Constantes'])
        self.process_quads(compiled_data['Quads'], compiled_data['FuncsDir'])
    
    '''
        Procesa las constantes y las guarda en memoria
        :param consts -> constantes
    '''
    def process_consts(self, consts):
        for const in consts: 
            dir = const[0]
            val = const[1]

            self.memoria.mem_constantes[dir] = val

    '''
        Obtiene las memorias de cada parametro
        :param left_operand
        :param right_operand
        :param result
    '''
    def get_memories(self, left_operand, right_operand, result):
        return self.get_memory(left_operand), self.get_memory(right_operand), self.get_memory(result)
    
    '''
        Obtiene el tipo dependiendo de la direccion
        :param address -> direccion
    '''
    def get_type(self, address):
        if 1000 <= address < 5000 or 21000 <= address < 25000:
            return int
        elif 5000 <= address < 9000 or 25000 <= address < 29000:
            return float
        elif 9000 <= address < 13000 or 29000 <= address < 33000:
            return str
        elif address >= 41000:
            return type(self.memoria.mem_constantes[address])
        else:
            return bool
    
    '''
        Obtiene la memoria dependiendo de la direccion
        :param address -> direccion
    '''
    def get_memory(self, address):
        if address is None:
            return None
        elif 1000 <= address < 21000:
            return self.memoria.mem_global
        elif 21000 <= address < 41000:
            return self.memoria.active.mem_local if self.memoria.active is not None else self.memoria.mem_local
        else: 
            return self.memoria.mem_constantes
    
    '''
        Obiene el contenido de los apuntadores a memoria
        :param address -> direccion
    '''
    def get_content(self, address):
        aux_address = int(address[1:-1])
        mem_address = self.get_memory(aux_address)
        arr_addr = mem_address[aux_address]
        return arr_addr

    '''
        Procesa los cuadruplos dependiendo del operador
        :param quads -> Cuadruplos
        :param funcs_dir -> Tabla de Funciones
        :param next -> Contador del siguiente cuadruplo a ejecutar
    '''
    def process_quads(self, quads, funcs_dir, next=0):

        params = []
        returned = None


        while True:
            operator = quads[next][0]
            left_operand = quads[next][1]
            right_operand = quads[next][2]
            result = quads[next][3]

            if isinstance(left_operand, str) and left_operand[0] == '(':
                left_operand = self.get_content(left_operand)
            if isinstance(right_operand, str) and right_operand[0] == '(':
                right_operand = self.get_content(right_operand)
                

            if operator == '=':
                if isinstance(result, str) and result[0] == '(':
                    aux_address = int(result[1:-1])
                    mem_address = self.get_memory(aux_address)
                    mem1 = self.get_memory(left_operand)
                    arr_address = mem_address[aux_address]
                    mem_arr_addr = self.get_memory(arr_address)
                    mem_arr_addr[arr_address] = mem1[left_operand]
                else:
                    mem1, mem2, mem_r = self.get_memories(left_operand, right_operand, result)
                    result_type = self.get_type(result)
                    mem_r[result] = (mem1[left_operand])

                next+=1

            elif operator == '+':
                if isinstance(result, str) and result[0] == '(':
                    aux_address = int(result[1:-1])
                    mem_address = self.get_memory(aux_address)
                    mem1 = self.get_memory(left_operand)
                    mem_address[aux_address] = int(mem1[left_operand]) + int(right_operand)
                else:
                    mem1, mem2, mem_r = self.get_memories(left_operand, right_operand, result)
                    if(isinstance(mem1[left_operand], str) and not isinstance(mem2[right_operand], str)) or (isinstance(mem2[right_operand],str) and not isinstance(mem1[left_operand],str)):
                        mem_r[result] = str(mem1[left_operand]) + str(mem2[right_operand])
                    else:
                        mem_r[result] = mem1[left_operand] + mem2[right_operand]
                
                next+=1
            
            elif operator == '-':
                mem1, mem2, mem_r = self.get_memories(left_operand, right_operand, result)
                mem_r[result] = mem1[left_operand] - mem2[right_operand]
                next += 1

            elif operator == '*':
                mem1, mem2, mem_r = self.get_memories(left_operand, right_operand, result)
                mem_r[result] = mem1[left_operand] * mem2[right_operand]
                next += 1
            
            elif operator == '/':
                mem1, mem2, mem_r = self.get_memories(left_operand, right_operand, result)

                if mem2[right_operand] == 0:
                    raise TypeError(f"Error: No se puede dividir entre 0")

                mem_r[result] = float(mem1[left_operand] / mem2[right_operand])
                next += 1
            
            elif operator == '>':
                mem1, mem2, mem_r = self.get_memories(left_operand, right_operand, result)
                mem_r[result] = mem1[left_operand] > mem2[right_operand]
                next +=1
            
            elif operator == '<':
                mem1, mem2, mem_r = self.get_memories(left_operand, right_operand, result)
                mem_r[result] = mem1[left_operand] < mem2[right_operand]
                next +=1
            
            elif operator == '<=':
                mem1, mem2, mem_r = self.get_memories(left_operand, right_operand, result)
                mem_r[result] = mem1[left_operand] <= mem2[right_operand]
                next +=1
            
            elif operator == '>=':
                mem1, mem2, mem_r = self.get_memories(left_operand, right_operand, result)
                mem_r[result] = mem1[left_operand] >= mem2[right_operand]
                next +=1
            
            elif operator == '==':
                mem1, mem2, mem_r = self.get_memories(left_operand, right_operand, result)
                mem_r[result] = mem1[left_operand] == mem2[right_operand]
                next +=1
            
            elif operator == '!=':
                mem1, mem2, mem_r = self.get_memories(left_operand, right_operand, result)
                mem_r[result] = mem1[left_operand] != mem2[right_operand]
                next +=1
            
            elif operator == '&&':
                mem1, mem2, mem_r = self.get_memories(left_operand, right_operand, result)
                mem_r[result] = mem1[left_operand] and mem2[right_operand]
                next +=1
            
            elif operator == '||':
                mem1, mem2, mem_r = self.get_memories(left_operand, right_operand, result)
                mem_r[result] = mem1[left_operand] or mem2[right_operand]
                next +=1
            
            elif operator == 'VERIF':
                mem1 = self.get_memory(left_operand)

                if not(0 <= mem1[left_operand] < int(result)):
                    raise TypeError("Fuera de los limites")
                
                next += 1
            
            elif operator == 'ESCRIBE':
                if isinstance(result, str) and result[0] == '(':
                    try:
                        dir = self.get_content(result)
                        mem = self.get_memory(dir) 
                        print(mem[dir])
                    except:
                        print("NULL")
                        break
                else:
                    mem = self.get_memory(result)
                    print(mem[result])
                next +=1
            
            elif operator == 'LEER':
                if isinstance(result, str) and result[0] == '(':
                    aux_address = int(result[1:-1])
                    mem_address = self.get_memory(aux_address)
                    mem1 = self.get_memory(left_operand)
                    arr_address = mem_address[aux_address]
                    mem_arr_addr = self.get_memory(arr_address)
                    arr_type = self.get_type(arr_address)
                    try:
                        mem_arr_addr[arr_address] = arr_type(input)
                    except:
                        print("ERROR: El dato de entrada no es del mismo tipo de dato que la variable a leer")
                        break
                else:
                    result_type = self.get_type(result)
                    mem = self.get_memory(result)
                    try:
                        input_result = result_type(input())
                    except:
                        print("ERROR: El dato de entrada no es del mismo tipo de dato que la variable a leer")
                        break
                
                mem[result] = input_result
                next+=1
            
            elif operator == 'GOTOF':
                mem_b = self.get_memory(left_operand)
                if not mem_b[left_operand]:
                    next = int(result) - 1
                else:
                    next += 1

            elif operator == 'GOTOV':
                mem_b = self.get_memory(left_operand)
                if mem_b[left_operand]:
                    next = int(result) - 1
                else:
                    next += 1        

            elif operator == 'GOTO':
                next = int(result) - 1
            
            elif operator == 'ERA':
                if self.memoria.active is not None:
                    superior = self.memoria.active
                else:
                    superior = self.memoria
                self.memoria.mem_func(superior, int(result))
                next += 1
            
            elif operator == 'GOSUB':
                self.memoria.active = self.memoria.mem_ejec[list(self.memoria.mem_ejec.keys())[-1]]

                self.pila_contextos.append(result)

                self.memoria.active.assign_params(params)
                params = []
                value = self.process_quads(quads, funcs_dir, int(result) - 1)

                if value is not None:
                    mem = self.get_memory(left_operand)
                    mem[left_operand] = value
                next += 1
            
            elif operator == 'REGRESA':
                mem = self.get_memory(result)
                returned = mem[result]

                self.memoria.remove_scope()
                self.pila_contextos.pop()

                return returned
                next+=1
            
            elif operator == 'PARAM':
                mem = self.get_memory(left_operand)
                params.append(mem[left_operand])

                next += 1
            
            elif operator == 'ENDFUNC':
                self.memoria.remove_scope()
                self.pila_contextos.pop()
                break
            
            elif operator == 'END':
                self.memoria.remove_scope()
                self.pila_contextos.pop()
                break
            
            #OPERACIONES MATRICIALES

            elif operator == '$':
                size = int(left_operand[0]) * int(left_operand[1])

                mem_arr = self.get_memory(right_operand)
                arr_type = self.get_type(right_operand)

                if arr_type not in [int, float]:
                    raise TypeError("Para usar el determinante es necesario que la matriz sea de tipo flotante o entero")
                
                dims = []
                aux = []
                arr_addr = int(right_operand)

                for i in range(size):
                    try:
                        val = mem_arr[arr_addr + i]
                    except:
                        raise TypeError('Elemento del arreglo no inicializado')
                    aux.append(val)
                    if (i+1)%left_operand[0] == 0:
                        dims.append(aux)
                        aux = []

                matrix = np.array(dims)  
                
                determinant = np.linalg.det(matrix)

                mem_r = self.get_memory(result)
                mem_r[result] = determinant

                next+=1
            
            elif operator == '!':
                size = int(left_operand[0]) * int(left_operand[1])

                mem_arr = self.get_memory(right_operand)
                arr_type = self.get_type(right_operand)

                dims = []
                aux = []
                arr_addr = int(right_operand)

                for i in range(size):
                    try:
                        val = mem_arr[arr_addr + i]
                    except:
                        raise TypeError('Elemento del arreglo no inicializado')
                    aux.append(val)
                    if (i+1)%left_operand[0] == 0:
                        dims.append(aux)
                        aux = []

                matrix = np.array(dims)  
                
                transpose = matrix.transpose()

                mem_r = self.get_memory(result)
                mem_r[result] = transpose

                next+=1
            
            elif operator == '?':
                size = int(left_operand[0]) * int(left_operand[1])

                mem_arr = self.get_memory(right_operand)
                arr_type = self.get_type(right_operand)

                dims = []
                aux = []
                arr_addr = int(right_operand)

                for i in range(size):
                    try:
                        val = mem_arr[arr_addr + i]
                    except:
                        raise TypeError('Elemento del arreglo no inicializado')
                    aux.append(val)
                    if (i+1)%left_operand[0] == 0:
                        dims.append(aux)
                        aux = []

                matrix = np.array(dims)  
                
                inverse = np.linalg.inv(matrix)

                mem_r = self.get_memory(result)
                mem_r[result] = inverse

                next+=1


                


                

                

                        
                    
