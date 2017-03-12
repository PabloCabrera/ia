from sys import stdout
import time
import random

suposiciones = 0

class Casillero:
	def __init__ (casillero, maximoNumero):
		casillero.conocido = False
		casillero.valor = None
		casillero.posibles = set ()
		for numero in range (1, maximoNumero+1):
			casillero.agregarPosible (numero)

	def agregarPosible (casillero, elemento):
		casillero.posibles.add (elemento)

	def quitarPosible (casillero, elemento):
		casillero.posibles.remove(elemento)

	def refrescar (casillero):
		posibilidades = len (casillero.posibles)
		
		if (posibilidades == 1):
			casillero.conocido = True
			for numero in casillero.posibles:
				casillero.valor = numero
			casillero.conocido  = True
		elif (posibilidades == 0):
			raise Inconsistencia ("Valor duplicado: "+ str (casillero.valor ))

	def esConocido (casillero):
		return casillero.conocido

	def establecerValor (casillero, numero):
		casillero.conocido = True
		casillero.posibles.clear ()
		casillero.agregarPosible (numero)
		casillero.valor = numero


class GrupoCasilleros:
	def __init__ (grupo, tamanio):
		maximoNumero = tamanio**2
		grupo.casilleros = []
		for x in range (0, tamanio):
			grupo.casilleros.append ([])
			for y in range (0, tamanio):
				grupo.casilleros[x].append (Casillero (maximoNumero))
				
	def establecerValor (grupo, x, y, valor):
		grupo.casilleros[x][y].establecerValor (valor)

	def estaResuelto (grupo):
		resuelto = True
		for lc in grupo.casilleros:
			for casillero in lc:
				resuelto = (resuelto and casillero.esConocido ())
		return resuelto

	def definidos (grupo):
		conjunto_definidos = set ()
		for lc in grupo.casilleros:
			for casillero in lc:
				if (casillero.esConocido ()):
					conjunto_definidos.add (casillero.valor)
		return conjunto_definidos

	def definidosFila (grupo, fila):
		conjunto_definidos = set ()
		for lc in grupo.casilleros:
			casillero = lc[fila]
			if (casillero.esConocido ()):
				conjunto_definidos.add (casillero.valor)
		return conjunto_definidos
			
	def definidosColumna (grupo, columna):
		conjunto_definidos = set ()
		for fila in range (len (grupo.casilleros)):
			casillero = grupo.casilleros[columna][fila]
			if (casillero.esConocido ()):
				conjunto_definidos.add (casillero.valor)
		return conjunto_definidos

	def comprobarConsistencia (grupo):
		lista_definidos = []
		for lc in grupo.casilleros:
			for casillero in lc:
				if (casillero.esConocido()):
					lista_definidos.append (casillero.valor)
		conjunto_definidos = set (lista_definidos)
		if (len (conjunto_definidos) < len (lista_definidos)):
			raise Inconsistencia ("Grupo inconsistente")


	def imprimirFila (grupo, fila):
		cadena = ""
		for columna in range (0, len (grupo.casilleros)):
			casillero = grupo.casilleros[columna][fila]
			if (casillero.esConocido ()):
				cadena += str (casillero.valor) + " "
			else:
				cadena += "." + " "
		stdout.write (cadena)
			

class Juego:
	def __init__ (juego, tamanio):
		juego.tamanio = tamanio
		juego.grupos = []
		for x in range (0, tamanio):
			juego.grupos.append ([])
			for y in range (0, tamanio):
				juego.grupos[x].append (GrupoCasilleros (tamanio))

	def imprimir (juego):
		tamanio = len (juego.grupos)
		for gy in range (0, tamanio):
			for cy in range (0, tamanio):
				for gx in range (0, tamanio):
					juego.grupos[gx][gy].imprimirFila (cy)
					stdout.write (" ")
				print ""
			print ""

	def establecerValor (juego, gx, gy, cx, cy, valor):
		juego.grupos[gx][gy].establecerValor (cx, cy, valor)

	def resolver (juego, mostrarExcepcion=True):
		juego.comprobarConsistencia ()
		salir = False;
		try:
			while (not (juego.estaResuelto () or salir)):
				cantidadCambios = juego.actualizarCasilleros ()
				if (cantidadCambios == 0):
					juego.resolverAdivinando (mostrarExcepcion)
					# print "No hay informacion suficiente para resolver el juego"
					salir = True
			return juego.estaResuelto()
		except Inconsistencia as inconsistencia:
			if mostrarExcepcion:
				print inconsistencia
			return False

	def estaResuelto (juego):
		resuelto = True
		for lg in juego.grupos:
			for grupo in lg:
				resuelto = (resuelto and grupo.estaResuelto ())
		return resuelto

	def actualizarCasilleros (juego):
		cantidadCambios = juego.calcularRestriccionesCasilleros ()
		juego.actualizarValoresCasilleros ()
		juego.comprobarConsistencia ()
		return cantidadCambios

	def calcularRestriccionesCasilleros (juego):
		cantidadCambios = 0
		for gx in range (0, len (juego.grupos)):
		 for gy in range (0, len (juego.grupos[gx])):
		  grupo = juego.grupos[gx][gy]
		  for cx in range (0, len (grupo.casilleros)):
		   for cy in range (0, len (grupo.casilleros[cx])):
		    if (juego.actualizarCasillero (gx, gy, cx, cy)):
		     cantidadCambios += 1
		return cantidadCambios

	def actualizarValoresCasilleros (juego):
		for gx in range (0, len (juego.grupos)):
		 for gy in range (0, len (juego.grupos[gx])):
		  grupo = juego.grupos[gx][gy]
		  for cx in range (0, len (grupo.casilleros)):
		   for cy in range (0, len (grupo.casilleros[cx])):
		    juego.grupos[gx][gy].casilleros[cx][cy].refrescar ()

	def actualizarCasillero (juego, gx, gy, cx, cy):
		huboCambios = False
		grupo = juego.grupos[gx][gy]
		casillero = grupo.casilleros[cx][cy]
		if (not casillero.esConocido ()):
			# Deberia llamarse aunque sea conocido para comprobar consistencia
			huboCambios = juego.aplicarRestriccionesGrupo (grupo, casillero) or huboCambios
			huboCambios = juego.aplicarRestriccionesFila (gy, cy, casillero) or huboCambios
			huboCambios = juego.aplicarRestriccionesColumna (gx, cx, casillero) or huboCambios
		return huboCambios

	def aplicarRestriccionesGrupo (juego, grupo, casillero):
		return juego.aplicarRestricciones (grupo.definidos (), casillero)

	def aplicarRestriccionesFila (juego, filaGrupo, filaCasillero, casillero):
		imposibles = set ()
		for lg in juego.grupos:
			grupo = lg[filaGrupo]
			imposibles = imposibles.union (grupo.definidosFila (filaCasillero)) 
		return juego.aplicarRestricciones (imposibles, casillero)

	def aplicarRestriccionesColumna (juego, columnaGrupo, columnaCasillero, casillero):
		imposibles = set ()
		for grupo in juego.grupos[columnaGrupo]:
			imposibles = imposibles.union (grupo.definidosColumna (columnaCasillero))
		return juego.aplicarRestricciones (imposibles, casillero)

	def aplicarRestricciones (juego, imposibles, casillero):
		huboCambios = False
		for valor in imposibles:
			if (valor in casillero.posibles):
				casillero.quitarPosible (valor)
				huboCambios = True
		return huboCambios
	
	def comprobarConsistencia (juego):
		juego.comprobarConsistenciaGrupos ()
		juego.comprobarConsistenciaFilas ()
		juego.comprobarConsistenciaColumnas ()

	def comprobarConsistenciaGrupos (juego):
		for lg in juego.grupos:
			for grupo in lg:
				grupo.comprobarConsistencia ()

	def comprobarConsistenciaFilas (juego):
		for gy in (range (0, juego.tamanio)):
			for cy in (range (0, juego.tamanio)):
				juego.comprobarConsistenciaFila (gy, cy)

	def comprobarConsistenciaFila (juego, gy, cy):
		lista_valores = []
		for gx in (range (0, juego.tamanio)):
			for cx in (range (0, juego.tamanio)):
				casillero=juego.grupos[gx][gy].casilleros[cx][cy]
				if (casillero.esConocido()):
					lista_valores.append (casillero.valor)
		conjunto_valores = set (lista_valores)
		if (len (conjunto_valores) < len (lista_valores)):
			raise Inconsistencia ("Fila inconsistente")

	def comprobarConsistenciaColumnas (juego):
		for gx in (range (0, juego.tamanio)):
			for cx in (range (0, juego.tamanio)):
				juego.comprobarConsistenciaColumna (gx, cx)

	def comprobarConsistenciaColumna (juego, gx, cx):
		lista_valores = []
		for gy in (range (0, juego.tamanio)):
			for cy in (range (0, juego.tamanio)):
				casillero=juego.grupos[gx][gy].casilleros[cx][cy]
				if (casillero.esConocido()):
					lista_valores.append (casillero.valor)
		conjunto_valores = set (lista_valores)
		if (len (conjunto_valores) < len (lista_valores)):
			raise Inconsistencia ("Columna inconsistente")

	def resolverAdivinando (juego, mostrarExcepcion=True):
		resuelto = False
		posicion = None
		posibilidades = 2
		while ((posicion is None) and (posibilidades <= juego.tamanio**2)):
			posicion=juego.casilleroConNPosibilidades (posibilidades)
			posibilidades += 1
		if (posicion is None):
			return False

		casillero = juego.grupos[posicion[0]][posicion[1]].casilleros[posicion[2]][posicion[3]]
		lista_posibles = list (casillero.posibles)
		indice_posible = 0
		while (indice_posible < len (lista_posibles)):
			valor_supuesto = lista_posibles[indice_posible]
			clon = juego.clonar ()
			clon.establecerValor (posicion[0],posicion[1], posicion[2],posicion[3], valor_supuesto)
			global suposiciones
			suposiciones += 1
			if suposiciones % 1000 == 0:
				print "Suposicion N" + str (suposiciones)
				clon.imprimir()
			#print ("Suponiendo valor %i en posicion [%i][%i][%i][%i]" %(valor_supuesto, gx,gy, cx,cy) )
			#clon.imprimir()
			try:
				if (clon.resolver (mostrarExcepcion=False)):
					juego.copiarValoresJuego (clon)
					resuelto = True
			except Inconsistencia as inconsistencia:
				pass
			indice_posible += 1
		if (resuelto and mostrarExcepcion):
			print "Juego resuelto."
		if ((not resuelto) and mostrarExcepcion):
			print "El juego no tiene solucion."
		return resuelto;

	def casilleroConNPosibilidades (juego, posibilidades):
		encontrado = None
		indice = 0
		while ((encontrado is None) and (indice < juego.tamanio**4)):
				cy = (indice // juego.tamanio**0) % juego.tamanio
				cx = (indice // juego.tamanio**1) % juego.tamanio
				gy = (indice // juego.tamanio**2) % juego.tamanio
				gx = (indice // juego.tamanio**3) % juego.tamanio
				probando = juego.grupos[gx][gy].casilleros[cx][cy]
				if ((not probando.esConocido ()) and (len (probando.posibles) == posibilidades)):
					encontrado = [gx, gy,  cx, cy]
				indice += 1
		return encontrado


	def clonar (juego):
		clon = Juego (juego.tamanio)
		clon.copiarValoresJuego (juego)
		return clon

	def copiarValoresJuego (juego, origen):
		for indice in range (0, juego.tamanio**4):
			cy = (indice // juego.tamanio**0) % juego.tamanio
			cx = (indice // juego.tamanio**1) % juego.tamanio
			gy = (indice // juego.tamanio**2) % juego.tamanio
			gx = (indice // juego.tamanio**3) % juego.tamanio
			casillero = origen.grupos[gx][gy].casilleros[cx][cy]
			if (casillero.esConocido ()):
				juego.establecerValor (gx, gy, cx, cy, casillero.valor)
			else:
				juego.grupos[gx][gy].casilleros[cx][cy].posibles = set (casillero.posibles)	


class Inconsistencia (Exception):
	def __init__ (inconsistencia, mensaje=""):
		inconsistencia.mensaje = mensaje

	def __str__ (inconsistencia):
		cadena = "Inconsistencia en juego: " + inconsistencia.mensaje
		return cadena

class CargadorJuego:
	def cargar (cargador, nombreArchivo):
		archivo = open (nombreArchivo, "r")
		lineas = archivo.readlines ();
		cargador.tamanio = cargador.calcularTamanio (lineas)
		cargador.juego = Juego (cargador.tamanio)
		cargador.establecerValores (lineas)
		return cargador.juego

	def calcularTamanio (juego, lineas):
		if (len (lineas[0]) == 20):
			tamanio = 3
		elif (len (lineas[0]) == 9):
			tamanio = 2
		else:
			raise Exception ("No se puede determinar tamanio de la grilla")
		return tamanio

	def establecerValores (cargador, lineas):
		gy = 0
		indice_linea = 0
		while (gy < cargador.tamanio):
		  linea = lineas[indice_linea]
		  cy = 0
		  while (cy < cargador.tamanio):
		    gx = 0
		    indice_caracter = 0
		    while (gx < cargador.tamanio):
		      cx = 0
		      while (cx < cargador.tamanio):
		        caracter = lineas[indice_linea][indice_caracter:indice_caracter+1]
		        try:
		          valor = int (caracter)
		          cargador.juego.establecerValor (gx, gy, cx, cy, valor)
		        except ValueError as error:
		          pass
		        cx += 1
		        indice_caracter += 2
		      gx += 1
		      indice_caracter += 1
		    cy += 1
		    indice_linea += 1
		  gy += 1
		  indice_linea += 1
