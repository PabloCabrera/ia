#!/usr/bin/env python

from sudoku import *
import sys

if (len (sys.argv) < 2):
	print "Uso: python resolver <archivo>"
	sys.exit (1)
else:
	nombre_archivo = sys.argv [1]

print "Cargando Juego desde archivo " + nombre_archivo
cargador = CargadorJuego()
juego = cargador.cargar (nombre_archivo)
juego.imprimir ()

print ""
print "Resolviendo Juego:"
print ""

if (juego.resolver ()):
	juego.imprimir ()

