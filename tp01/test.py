from sudoku import *

print "Casillero:"

print "\tComprobando valores posibles"
casillero = Casillero (9)
assert (len (casillero.posibles) == 9)
for numero in range (1, 10):
	assert (numero in casillero.posibles)

print "\tComprobando quitarPosible"
casillero = Casillero (9)
casillero.quitarPosible (7)
casillero.quitarPosible (2)
assert (len (casillero.posibles) == 7)
for numero in [7, 2]:
	assert (numero not in casillero.posibles)
for numero in [1, 3, 4, 5, 6, 8, 9]:
	assert (numero in casillero.posibles)


print "\tComprobando agregarPosible"
casillero = Casillero (9)
casillero.agregarPosible(10)
casillero.agregarPosible(15)
assert (len (casillero.posibles) == 11)
for numero in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15]:
	assert (numero in casillero.posibles)


print "\tComprobando refrescar"
casillero = Casillero (9)
assert (not casillero.esConocido ())
for numero in [1, 2, 3, 4, 6, 7, 8, 9]:
	casillero.quitarPosible (numero);
assert (not casillero.esConocido ())
casillero.refrescar ()
assert (casillero.esConocido ())
assert (casillero.valor == 5)
assert (len (casillero.posibles) == 1)
assert (5 in casillero.posibles)


print "\tComprobando establecerValor"
casillero = Casillero (9)
assert (not casillero.esConocido ())
assert (len (casillero.posibles) == 9)
casillero.establecerValor (8)
assert (casillero.esConocido ())
assert (casillero.valor == 8)
assert (len (casillero.posibles) == 1)


print ""
print "Grupo:"

print "\tComprobando establecerValor"
grupo = GrupoCasilleros (3)
for x in range (len (grupo.casilleros)):
	for y in range (len (grupo.casilleros[x])):
		casillero = grupo.casilleros[x][y]
		assert (not casillero.esConocido ())
		for numero in [3, 6, 1, 7]:
			grupo.establecerValor (x, y, numero)
			assert (casillero.esConocido ())
			assert (casillero.valor == numero)

print "\tComprobando estaResuleto"
grupo = GrupoCasilleros (3)
assert (not grupo.estaResuelto ())
for x in [0, 1, 2]:
	for y in [0, 2]:
		grupo.establecerValor (x, y, 9)
assert (not grupo.estaResuelto ())
grupo.establecerValor (0, 1, 9)
grupo.establecerValor (1, 1, 9)
assert (not grupo.estaResuelto ())
grupo.establecerValor (2, 1, 9)
assert (grupo.estaResuelto ())

print "\tComprobando definidos"
grupo = GrupoCasilleros (3)
definidos = grupo.definidos ()
assert (len (definidos) == 0)
definidos = grupo.definidos ()
grupo.establecerValor (0, 0, 5)
grupo.establecerValor (0, 1, 6)
grupo.establecerValor (0, 2, 8)
definidos = grupo.definidos ()
assert (len (definidos) == 3)
for numero in [5, 6, 8]:
	assert (numero in definidos)
for numero in [1, 2, 3, 4, 7, 9]:
	assert (numero not in definidos)

print "\tComprobando definidosFila"
grupo = GrupoCasilleros (3)
definidos = grupo.definidosFila (1)
assert (len (definidos) == 0)
grupo.establecerValor (2, 0, 5)
grupo.establecerValor (0, 1, 4)
grupo.establecerValor (0, 1, 6)
grupo.establecerValor (1, 1, 9)
grupo.establecerValor (0, 2, 8)
definidos = grupo.definidosFila (1)
assert (len (definidos) == 2)
for numero in [9, 6]:
	assert (numero in definidos)
for numero in [1, 2, 3, 4, 5, 7, 8]:
	assert (numero not in definidos)

print "\tComprobando definidosColumna"
grupo = GrupoCasilleros (3)
definidos = grupo.definidosColumna (2)
assert (len (definidos) == 0)
grupo.establecerValor (2, 0, 9)
grupo.establecerValor (0, 0, 7)
grupo.establecerValor (2, 1, 6)
grupo.establecerValor (1, 2, 5)
grupo.establecerValor (0, 2, 8)
definidos = grupo.definidosColumna (2)
assert (len (definidos) == 2)
for numero in [9, 6]:
	assert (numero in definidos)
for numero in [1, 2, 3, 4, 5, 7, 8]:
	assert (numero not in definidos)


print ""
print "Juego:"

print "\tComprobando cantidad de casilleros"
juego = Juego (3)
assert (len (juego.grupos) == 3)
for lg in juego.grupos:
	assert (len (lg) == 3)
	for grupo in lg:
		assert (len (grupo.casilleros) == 3)
		for lc in grupo.casilleros:
			assert (len (lc) == 3)
print "\tComprobando clonar"
juego =  Juego (2)
juego.establecerValor(0,1, 1,1, 3)
clon = juego.clonar()
assert (juego.grupos[0][1].casilleros[1][1].valor == 3)
assert (clon.grupos[0][1].casilleros[1][1].valor == 3)
clon.establecerValor(0,1, 1,1, 2)
assert (juego.grupos[0][1].casilleros[1][1].valor == 3)
assert (clon.grupos[0][1].casilleros[1][1].valor == 2)
clon.establecerValor(0,0, 0,0, 1)
assert (juego.grupos[0][0].casilleros[0][0].valor is None)
assert (clon.grupos[0][0].casilleros[0][0].valor == 1)
