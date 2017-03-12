<h1>Sudoku</h1>

<p>Programa que resuelve el juego sudoku</p>

<h2>Algoritmo</h2>

<pre>Mientras juego no esta terminado:
	Reiniciar contador de cambios
	Para cada casillero:
		Si No esta resuelto:
			Para cada numero en la lista de valores posibles para el casillero:
				Si el mismo numero esta en el grupo, o en la fila, o en la columna :
					Eliminarlo de la lista de valores posibles para el casillero
					Aumentar contador de cambios
		Si el numero de posibles es 1:
			Marcar casillero como resuelto
		Si el numero de posibles es cero:
			Hay inconsistencia, abortar
	Si contador de cambios es cero:
		Para el casillero no resueltos con menos valores posibles:
			Para cada numero en lista de valores posibles para dicho casillero:
				Suponer que el valor de dicho casillero es dicho numero
					Intentar resolver basandose en la suposicion
				Si no hay No hay inconsistencia:
					Copiar datos de supuesto a real
</pre>

<h2>Como usar</h2>
	<p>En primer lugar, es necesario escribir un archivo de entrada. En el directorio <em>juegos</em> hay varios ejemplos. Puede utilizarse <em>grilla3.txt</em> como plantilla.</p>
	<p>Ejecutar desde la linea de commandos el script resolver.py con el nombre del archivo de juego como parametro.</p>
	<h3>Ejemplo</h3>
	<tt>user@host:/ia/sudoku$ python resolver.py juegos/08.txt</tt>
	<p>Produciria la siguiente salida:</tt>
	
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

