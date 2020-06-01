import json
from maquina_virtual import MaquinaVirtual

def generate_obj(program, funcs_table, quads, consts):
    obj_comp = {
        "Quads": quads,
        "FuncsDir": funcs_table,
        "Constantes": consts    
    }

    with open(f'pruebas/{program}_comp.cuac', 'w') as nuevo_arch:
        json.dump(obj_comp,nuevo_arch, separators = (',',':'))
    
    print('''
          _          _          _          _          _
        >(')____,  >(')____,  >(')____,  >(')____,  >(') ___,
        (` =~~/    (` =~~/    (` =~~/    (` =~~/    (` =~~/
        ^~^`---'~^~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~^`---'~^~^~
        CUAC CUAC CUAC CUAC CUAC CUAC CUAC CUAC CUAC CUAC CUAC CUAC
    ''')
    
    MaquinaVirtual().process(program)