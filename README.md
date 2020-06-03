# Patito++
Patito++ es un lenguaje de programación imperativo procedural que maneja expresiones aritméticas, logicas y relacionales, estatutos de interacción, estatutos de control de flujo, elementos de cambio de contexto, manejo de elementos no atómicos, sobre carga de operadores para operaciones con vectores y matrices, y operadores especiales para operaciones sobre matrices.

Los operadores +, -, * se pueden aplicar directamente sobre elementos dimensionados. También existen dos operadores especiales para matrices: $ denota el determinante de una matriz, ! (exclamación cerrada) denota la transpuesta de una matriz.

## Equipo Patito
| Nombre | Matricula |
| ------ | --------- |
| Iván Muñiz Ramírez | A01039386 |
| Ricardo Acosta Esquivel | A01039456 |

## Requerimientos para uso del lenguaje
- Python 3
- Numpy

## Manual de usuario
Los tipos de variables soportados por el lenguaje son int, float y string, y son declarados de la siguiente manera:
```
programa nombre;
var int i, j, resultado; 
    string mensaje;
    float pi;
    
principal() {
    < Aquí va tu programa principal >
}
```
Y se inicializan de la siguiente manera:
```
programa nombre;
var int i, j, suma; 
    string mensaje;
    float pi;
    
principal() {
    i = 10;
    j = 5;
    suma = i + j;
    pi = 3.14;
    
    escribe(i, j, suma, pi);
}
```
Notese que las variables siempre deben de inicializarse dentro del bloque principal.

Para hacer uso de condicionales se hace de la siguiente manera:
```
programa nombre;
var int i, j;

principal() {
    i = 15;
    j = 10;

    si(i < j) entonces {
        escribe("i es menor que j");
    } sino {
        si(i > j) entonces {
            escribe("i es mayor que j");
        }
    }
}
```
Para el uso de de ciclos se sigue la siguiente estructura:
```
programa nombre;
var int i;

principal() {
    desde i = 0 hasta i == 10 hacer {
        escribe(i);
    }

    mientras( i < 20 ) haz {
        escribe(i);
        i = i + 1;
    }
}
```
Para el uso de funciones se sigue la siguiente estructura:
```
programa nombre;
var int entrada;

funcion int miFuncion(int i)
var int aux; 
{
    aux = i + 5;
    regresa(aux);
}

principal() {
    escribe(miFuncion(5));
}
```
El usuario puede ingersar datos al programa en tiempo de ejecución con la función lee() de la siguiente manera:
```
programa nombre;
var int numeroDeTacos;

principal() {
    escribe("Ingrese el número de tacos que comió Ricardo:");
    lee(numeroDeTacos);

    escribe("Ricardo comió", numeroDeTacos, "tacos");
}
```

## Ejemplos de programas

### Mi primer programa
Crear el archivo holamundo.pmm
```
programa miprimerprograma;

principal() {
    escribe("Hola mundo!");
}
```
Para compilar el programa se hace de la siguiente manera:
```
python patitomasmas.py pruebas/holamundo.pmm
```

### Calculo de factorial ciclico
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

### Calculo de factorial recursivo
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
### Fibonacci ciclico
```
programa fibonacci_ciclico;
var int numero, fibo1, fibo2, i;

principal() {
    escribe("Introduce numero");
    lee(numero);

    fibo1 = 0;
    fibo2 = 1;
    escribe(fibo1);

    desde i = 1 hasta i >= numero hacer {
        escribe(fibo2);
        fibo2 = fibo1 + fibo2;
        fibo1 = fibo2 - fibo1;
    }
}
```

### Fibonacci recursivo
```
programa fibonacci;
var int numeros, i;

funcion int fibonacci(int i){
    si(i == 0 || i == 1) entonces {
        regresa(i);
    } sino {
        regresa(fibonacci(i - 1) + fibonacci(i - 2));
    }
}

principal() {
    escribe("Escribe cuanto numeros quieres calcular de la serie");
    lee(numeros);

    desde i=0 hasta i == numeros hacer {
        escribe(fibonacci(i));
    }
  
}
```
