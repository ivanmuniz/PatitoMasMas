import json
from memoria import Memoria


class MaquinaVirtual:
    def __init__(self):
        self.program = None
        self.memoria = Memoria()

        self.pila_contextos = []
    
    def process(self, program):
        compiled = f"pruebas/{program}_comp.cuac"
        
        compiled_file = open(compiled, 'r')

        compiled_data = json.load(compiled_file)

        self.pila_contextos.append('main')
        self.program = program

        self.process_consts(compiled_data['Constantes'])
        self.process_quads(compiled_data['Quads'], compiled_data['FuncsDir'])
    
    def process_consts(self, consts):
        for const in consts: 
            dir = const[0]
            val = const[1]

            self.memoria.mem_constantes[dir] = val

    def get_memories(self, left_operand, right_operand, result):
        return self.get_memory(left_operand), self.get_memory(right_operand), self.get_memory(result)
    
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
    
    def get_memory(self, address):
        if address is None:
            return None
        elif 1000 <= address < 21000:
            return self.memoria.mem_global
        elif 21000 <= address < 41000:
            return self.memoria.active.mem_local if self.memoria.active is not None else self.memoria.mem_local
        else: 
            return self.memoria.mem_constantes
    
    def get_content(self, address):
        aux_address = int(address[1:-1])
        mem_address = self.get_memory(aux_address)
        return mem_address[aux_address]

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
            if isinstance(result, str) and result[0] == '(':
                result = self.get_content(result)

            if operator == '=':
                mem1, mem2, mem_r = self.get_memories(left_operand, right_operand, result)
                result_type = self.get_type(result)
                mem_r[result] = result_type(mem1[left_operand])

                next+=1

            elif operator == '+':
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
                result_type = self.get_type(result)

                if mem2[right_operand] == 0:
                    raise TypeError(f"Error: No se puede dividir entre 0")

                mem_r[result] = result_type(mem1[left_operand] / mem2[right_operand])
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
                mem = self.get_memory(result)
                print(mem[result])
                next +=1
            
            elif operator == 'LEER':
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
            
            elif operator == 'END':
                break