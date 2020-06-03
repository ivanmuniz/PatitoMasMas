# Patito++
Patito++ es un lenguaje de programación imperativo procedural que maneja expresiones aritméticas, logicas y relacionales, estatutos de interacción, estatutos de control de flujo, elementos de cambio de contexto, manejo de elementos no atómicos, sobre carga de operadores para operaciones con vectores y matrices, y operadores especiales para operaciones sobre matrices.

Los operadores +, -, * se pueden aplicar directamente sobre elementos dimensionados. También existen dos operadores especiales para matrices: $ denota el determinante de una matriz, ! (exclamación cerrada) denota la transpuesta de una matriz.

## Requerimientos para uso del lenguaje
- Python 3
- Numpy

## Declaración de variables
```
programa declaracion_de_variables;
var int 
```

## Mi primer programa
Crear el archivo holamundo.pmm
```
programa miprimerprograma;

principal() {
    escribe("Hola mundo!");
}
```
```
python patitomasmas.py pruebas/holamundo.pmm
```

## Declaración e incialización de variables
```
programa main;
var int i, j, resultado; 
    string mensaje;

principal() {
    i = 5;
    j = 20;
    resultado = i * j;
    mensaje = "El resultado de la operación es:";

    escribe(mensaje, resultado);
}
```

## Uso de funciones
```
programa main;

funcion void desplegarInformacion(string nombre)
var int edad;
{
    edad = 24;
    escribe("Mi nombre es: ", nombre);
    escribe("Tengo", edad, "años");
}

principal() {
    desplegarInformacion("Iván");
}
```

## Estatutos de interacción
```
programa main;
var int numeroDeTacos;

principal() {
    escribe("Ingrese el número de tacos que comió Ricardo:");
    lee(numeroDeTacos);

    escribe("Ricardo comió", numeroDeTacos, "tacos");
}
```

## Calculo de factorial ciclico
```
programa factorial;
var int entrada, i, resultado;

principal() {
    resultado = 1;
    escribe("Escribe el numero para calcular factorial");
    lee(entrada);
    desde i = 1 hasta i > entrada hacer {
        resultado = i*resultado;
    }
    escribe(resultado);
}
```

## Calculo de factorial recursivo
```
programa factorial_recursivo;
var int entrada;

funcion int factorial_recursivo(int i)
var int aux; 
{
    si(i == 0 || i == 1) entonces {
        regresa(1);
    }
    regresa(i*factorial_recursivo(i - 1));
}

principal() {
    escribe("Dime el valor");
    lee(entrada);
    escribe(factorial_recursivo(entrada));
}
```

## Integrantes del Equipo
| Nombre | Matricula |
| ------ | --------- |
| Iván Muñiz Ramírez | A01039386 |
| Ricardo Acosta Esquivel | A01039456 |
