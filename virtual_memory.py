class VirtualMemory(object):
    _instance = None

    mem_global = {}
    mem_local = {}
    mem_constantes = {}

    # Bases donde inician las memorias
    _BASE_GLOBAL = 1000
    _BASE_GLOBAL_TEMP = 1700
    _BASE_LOCAL = 21000
    _BASE_LOCAL_TEMP = 37000
    _BASE_CONSTATES = 41000

    # Desplazamiento por tipo de dato VARIABLE
    _B_INT = 0
    _B_FLOAT = 4000
    _B_STRING = 8000
    _B_BOOL = 12000

    # Desplazamiento por tipo de dato TEMPORAL
    _B_INT_TEMP = 0
    _B_FLOAT_TEMP = 1000
    _B_STRING_TEMP = 2000
    _B_BOOL_TEMP = 3000

    segmento_global = [0, 0, 0 ,0]
    segmento_global_temporal = [0, 0, 0, 0]
    segmento_local = [0, 0, 0, 0]
    segmento_local_temporal = [0, 0, 0, 0]
    segmento_constantes = [0, 0, 0, 0]

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(VirtualMemory, cls).__new__(cls)
        return cls._instance

    '''
    SEGMENTO GLOBAL
        GLOBAL (Variables)
            int     [1000  -  4999]
            float   [5000  -  8999]
            string  [9000  - 12999]
            bool    [13000 - 16999]
        TEMPORAL
            int     [17000 - 17999]
            float   [18000 - 18999]
            string  [19000 - 19999]
            bool    [20000 - 20999]

    SEGMENTO LOCAL
        LOCAL (Variables)
            int     [21000 - 24999]
            float   [25000 - 28999]
            string  [29000 - 32999]
            bool    [33000 - 36999]
        TEMPORAL
            int     [37000 - 37999]
            float   [38000 - 38999]
            string  [39000 - 39999]
            bool    [40000 - 40999]

    SEGMENTO CONSTANTES
            int     [41000 - 42999]
            float   [43000 - 44999]
            string  [45000 - 46999]
            bool    [47000 - 48999] 
    '''

    def getDir(self, segmento, temp, type):
        if temp:
            return self._checkTypeTemp(type, segmento)
        else:
            return self._checkType(type, segmento)

    def _checkType(self, type, segmento):
        # print("LOG: checkType")
        BASE = self._BASE_GLOBAL if segmento == 'global' else self._BASE_CONSTATES if segmento == 'constante' else self._BASE_LOCAL
        segmento = self.segmento_global if segmento == 'global' else self.segmento_constantes if segmento == 'constante' else self.segmento_local
        if type == 'int':
            dir = BASE + self._B_INT + segmento[0]
            segmento[0] += 1
            return dir
        elif type == 'float':
            dir = BASE + self._B_FLOAT + segmento[1]
            segmento[1] += 1
            return dir
        elif type == 'str':
            dir = BASE + self._B_STRING + segmento[2]
            segmento[2] += 1
            return dir
        elif type == 'bool':
            dir = BASE + self._B_BOOL + segmento[3]
            segmento[3] += 1
            return dir

    def _checkTypeTemp(self, type, segmento):
        # print("LOG: checkTypeTemp")
        BASE_TEMP = self._BASE_LOCAL_TEMP if segmento != 'global' else self._BASE_GLOBAL_TEMP
        segmento_temp = self.segmento_local_temporal if segmento != 'global' else self.segmento_global_temporal
        if type == 'int':
            dir = BASE_TEMP + self._B_INT_TEMP + segmento_temp[0]
            segmento_temp[0] += 1
            return dir
        elif type == 'float':
            dir = BASE_TEMP + self._B_FLOAT_TEMP + segmento_temp[1]
            segmento_temp[1] += 1
            return dir
        elif type == 'str':
            dir = BASE_TEMP + self._B_STRING_TEMP + segmento_temp[2]
            segmento_temp[2] += 1
            return dir
        elif type == 'bool':
            dir = BASE_TEMP + self._B_BOOL_TEMP + segmento_temp[3]
            segmento_temp[3] += 1
            return dir

    '''
    El segmento local se reinicia para cada funcion
    Esta funcion es llamada en patitomasmas.py en la función p_punto_meter_funcion
    '''
    def resetCounters(self):
        self.segmento_local = [0, 0, 0, 0]
        self.segmento_local_temporal = [0, 0, 0, 0]


    '''
    Las constantes SÓLO se gurdan una vez.
    Por ejemplo si te encuentras un 2 y despues en otra funcion hay un 2, la direccion de memoria de ambos 2 es la misma
    '''
    # TODO: Checar como se deben de guarar las constantes e implementar la función
    def addConstant(self, value, type):
        print("ADD CONSTANT", value, type)
        if value in self.mem_constantes.values():
            for dir, val in self.mem_constantes.items():
                if val == value:
                    return dir

        if type == 'str':
            value = value.strip('"').strip("'")

        dir = self.getDir("constante", False, type)
        self.mem_constantes[dir] = value
        return dir