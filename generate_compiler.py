import json
from maquina_virtual import MaquinaVirtual

'''
Función para generar el archivo json con con los cuadruplos, directorio de funciones y constantes y ejecutar la maquina virtual una vez que el archivo este creado.
@param dict funcs_table: Directorio de funciones usado durante compilación
@param list quads: Cuadruplos generados durante compilación
@param list consts: Constantes encontradas durante compilación
'''
def generate_obj(program, funcs_table, quads, consts):
    obj_comp = {
        "Quads": quads,
        "FuncsDir": funcs_table,
        "Constantes": consts    
    }

    with open(f'pruebas/{program}_comp.cuac', 'w') as nuevo_arch:
        json.dump(obj_comp,nuevo_arch, separators = (',',':'))
    

    MaquinaVirtual().process(program)