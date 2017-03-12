<h1>Sudoku</h1>

<p>Programa que resuelve el juego Sudoku</p>

<h2>Algoritmo</h2>

<pre>Mientras juego no esta terminado:
	Reiniciar contador de cambios
	Para cada casillero:
		Si No esta resuelto:
			Para cada numero en el conjunto de valores posibles para el casillero:
				Si el mismo numero esta en el grupo, o en la fila, o en la columna :
					Eliminarlo del conjunto de valores posibles para el casillero
					Aumentar contador de cambios
		Si el numero de posibles es 1:
			Marcar casillero como resuelto
		Si el numero de posibles es cero:
			Hay inconsistencia, abortar
	Si contador de cambios es cero:
		Para el casillero no resuelto con menos valores posibles:
			Para cada numero en conjunto de valores posibles para dicho casillero:
				Suponer que el valor de dicho casillero es dicho numero
					Intentar resolver basandose en la suposicion
				Si no hay No hay inconsistencia:
					Copiar datos de supuesto a real
</pre>
<p>Para modelar el problema se tiene un conjunto de valores posibles para cada casillero cuyo valor es desconocido. El algoritmo itera sobre estos casilleros, eliminando del conjunto de valores posibles aquellos valores ya existentes en en el mismo grupo, fila o columna. Esto se repite hasta que el proceso no produzca cambios.</p>
<p>A partir de entonces se pasa a la etapa de realizar suposiciones. Se toma el casillero con valor desconocido cuyo conjunto de valores posibles sea menor, y se prueba con uno de dichos valores. Si aplicando recursivamente el proceso se llega a una inconsistencia, se descarta el valor del conjunto de valores posibles para el casillero y se prueba con el siguiente. Si se llega a una solucion que sea consistente, significa que la suposicion fue correcta, y el juego esta resuelto.</p>

<h2>Como usar</h2>
<p>En primer lugar, es necesario escribir un archivo de entrada. En el directorio <em>juegos</em> hay varios ejemplos. Puede utilizarse <em>grilla3.txt</em> como plantilla para sudokus de 9x9. Cada "." representa un casillero vacio, los espacios en blanco son obligatorios para mejorar la legibilidad.</p>
<p>Ejecutar desde la linea de commandos el script <em>resolver.py</em> con el nombre del archivo de juego como parametro.</p>
<h3>Ejemplo</h3>
<pre>user@host:/ia/sudoku$ python resolver.py juegos/08.txt</pre>
<p>Produciria la siguiente salida:</p>
	
<pre>Cargando Juego desde archivo juegos/08.txt
. 9 7  . 6 4  . 5 .  
3 . 4  . . .  7 8 6  
2 . 6  . 7 .  . . 3  

. 7 .  4 5 8  6 . .  
. . .  . 3 6  . 7 .  
. . .  . . .  8 . .  

. 3 9  . . .  5 2 8  
6 . .  . 2 5  . . .  
. . .  . . .  . . .  


Resolviendo Juego:

Juego resuelto.
8 9 7  3 6 4  2 5 1  
3 1 4  5 9 2  7 8 6  
2 5 6  8 7 1  9 4 3  

9 7 3  4 5 8  6 1 2  
5 8 1  2 3 6  4 7 9  
4 6 2  7 1 9  8 3 5  

1 3 9  6 4 7  5 2 8  
6 4 8  1 2 5  3 9 7  
7 2 5  9 8 3  1 6 4  
</pre>

