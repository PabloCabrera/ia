# -*- coding: utf-8 -*-
from entropia import formulas_entropia_atributo

def cargar_datos (nombre_archivo):
	archivo = open (nombre_archivo, "r")
	cabeceras = None
	datos = []
	n_observacion = 0
	for linea in archivo:
		fila = linea.rstrip().split (",")
		if cabeceras is None:
			cabeceras = fila
		else:
			observacion = {}
			n_observacion += 1
			observacion["ID"] = n_observacion
			for n_columna in xrange(0, len(cabeceras)):
				atributo = cabeceras[n_columna]
				observacion[atributo] = fila[n_columna]
			datos.append (observacion)
	return datos, cabeceras

def filtrar_datos (datos, atributo, valor):
	datos_filtrados = []
	for observacion in datos:
		if (observacion[atributo] == valor):
			datos_filtrados.append (observacion)
	return datos_filtrados

def listar_valores_atributo (datos, atributo):
	valores = []
	for observacion in datos:
		valor = observacion[atributo]
		if valor not in valores:
			valores.append (valor)
	return valores

def listar_resultados_posibles (datos, atr_objetivo):
	# CORREGIR
	return ["SI", "NO"]

def agrupar_por_atributo (datos, atributos, atr_objetivo):
	agrupados = {}

	for atributo in atributos:
		agrupados[atributo] = {}
		for valor in listar_valores_atributo (datos, atributo):
			agrupados[atributo][valor] = {}
			for resultado in listar_resultados_posibles (datos, atr_objetivo):
				agrupados[atributo][valor][resultado] = []

	for observacion in datos:
		resultado = observacion[atr_objetivo]
		for atributo in atributos:
			valor = observacion[atributo]
			agrupados[atributo][valor][resultado].append (observacion["ID"])

	return agrupados

def dibujar_tabla_datos (datos, cabeceras):
	txt = "\hspace*{-3cm}\\begin {tabular}{|%s|}\n" % "|".join(map (lambda v: "c", cabeceras))
	txt += "\\hline\n"
	txt += "&".join(cabeceras)
	txt += "\\\\\n\\hline\n"
	for observacion in datos:
		txt += "&".join (map (lambda atributo: "%s"%observacion[atributo], cabeceras))
		txt += "\\\\\n\\hline\n"
	txt += "\\end {tabular}\hspace*{-3cm}\\\\\n"
	return txt


def dibujar_arbol_atributo (elementos, atributo):
	txt = "\\Tree"
	txt += generar_rama (elementos, atributo)
	txt += "\\\\\n"
	return txt

def generar_rama (elementos, titulo=None):
	txt = "["
	if titulo is not None:
		txt += ".%s " % titulo
	if isinstance (elementos, dict):
		for clave in elementos:
			txt += generar_rama (elementos[clave], clave)
			txt += " "
	elif isinstance (elementos, list):
		for elemento in elementos:
			txt += generar_rama (elemento)
			txt += " "
	else:
		return "{%s} " % str (elementos)
	txt += "]"
	return txt

def generar_info_atributo (datos_agrupados, atributo):
		txt = "\subsection {Cálculo de entropía para variable %s}\n" % atributo
		txt += dibujar_arbol_atributo (datos_agrupados[atributo], atributo)
		txt += formulas_entropia_atributo (datos_agrupados[atributo], atributo)
		return txt

def main ():
	datos, cabeceras = cargar_datos ("datos.csv")
	atributos_arboles = cabeceras[:]
	atributos_arboles.remove("OBJETIVO")
	agrupados = agrupar_por_atributo (datos, atributos_arboles, "OBJETIVO")
	texto_documento = dibujar_tabla_datos (datos, cabeceras)
	texto_documento += "\section {Iteración 1}\n"
	for atributo in agrupados:
		texto_documento += generar_info_atributo (agrupados, atributo)
	atributo_menor_entropia = seleccionar_atributo_menor_entropia (agrupados)
	imprimir_documento(texto_documento)

def imprimir_documento (texto_documento):
	print """
\documentclass{article}
\usepackage[utf8]{inputenc}
\usepackage[table]{xcolor}
\usepackage{tikz-qtree}
\\begin {document}
%s
\end {document}
""" % texto_documento

main ()
