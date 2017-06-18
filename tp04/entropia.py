# -*- coding: utf-8 -*-

from math import log

def calcular_entropia_valores (datos):
	for atributo in datos:
		print atributo
		entropia_del_atributo = calcular_entropia_total (datos[atributo])
		print "\t[ total %s: %f ]" % (atributo, entropia_del_atributo)

def calcular_entropia (elem1, elem2):
	total = float(elem1 + elem2)
	if (elem1 == elem2):
		return 1
	elif ((elem1 == 0) or (elem2 == 0)):
		return 0
	else:
		return -(float(elem1)/total) * log (float(elem1)/total, 2) - (float(elem2)/total)*log (float(elem2)/total, 2)

def formula_entropia (elem1, elem2):
	total = int(elem1 + elem2)
	calculado = calcular_entropia (elem1, elem2)
	txt = "\indent $-\\frac{{{1}}}{{{0}}} \log_2\left(\\frac{{{1}}}{{{0}}}\\right) -\\frac{{{2}}}{{{0}}} \log_2\left(\\frac{{{2}}}{{{0}}}\\right) \\approx {3:.3f}$\\\\\n".format(total, elem1, elem2, calculado)
	return txt

def calcular_entropia_total (atributo):
	entropias = {}
	cantidad_elementos = {}
	suma = 0
	total_elementos = 0

	for valor in atributo:
		total_elementos += len(atributo[valor]["SI"]) + len(atributo[valor]["NO"]) 

	for valor in atributo:
		entropias[valor] = calcular_entropia (len(atributo[valor]["SI"]), len(atributo[valor]["NO"]))
		cantidad_elementos[valor] = len(atributo[valor]["SI"])+len(atributo[valor]["NO"])
		suma += entropias[valor]*float(cantidad_elementos[valor])/float(total_elementos)

	return suma

def formulas_entropia_atributo (elementos, titulo):
	txt = ""

	for valor in elementos:
		txt += "Entropía para %s = %s\\\\\n" % (titulo, valor)
		txt += formula_entropia (len(elementos[valor]["SI"]), len(elementos[valor]["NO"]))
		txt += "\\\\\\\\\n"
	txt += "Entropia total de variable %s\\\\\n" % titulo
	txt += formula_entropia_total (elementos)
	return txt

def formula_entropia_total (atributo):
	total_elementos = 0
	txt = "\indent $"
	entropia_total = calcular_entropia_total (atributo)
	formulas = []

	for valor in atributo:
		total_elementos += len(atributo[valor]["SI"]) + len(atributo[valor]["NO"]) 

	for valor in atributo:
		entropia = calcular_entropia (len(atributo[valor]["SI"]), len(atributo[valor]["NO"]))
		cantidad_elementos = len(atributo[valor]["SI"])+len(atributo[valor]["NO"])
		formulas.append ("\\frac{{{0}}}{{{1}}} \cdot {2:.3f}".format (cantidad_elementos, total_elementos, entropia))
	txt += " + ".join (formulas)
	txt += " \\approx {0:.3f}".format (entropia_total)
	txt += "$\\\\\n"
	return txt


