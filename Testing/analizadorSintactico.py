#!/usr/bin/env python
# coding=utf-8

'''#Authors: Bonet Peinado Daiana, de la Fuente Juan M.
#Year: 2018
#License: GNU GPLv3. See LICENSE file for more information.'''

#import string
#import random
import argparse
import os
import analizadorLexico
from tabla import Tabla

#from analizadorLexico import lexema

###Variables globales

#Bandera de modo verboso
global verbose

#Preanalisis procesado
global preanalisis
global preanalisisAnterior
preanalisis=""
preanalisisAnterior=""

#Posicion del token analizado
global posicion
posicion=0

##Variables para Analisis Semántico
#Tabla de Simbolos y entrada actual
global tablaSimbolos
tablaSimbolos = None
global tablaActual
tablaActual = None
global identificadoresActuales
identificadoresActuales=list()

#Definicion de casos posibles


def digitos():
	ret = "VOID"
	if verbose:
		print("-->digitos")
	if(preanalisis == "numero"):
		match("numero")
		ret = "INTEGER"
	elif (preanalisis == "operador_aritmetico"):
		match("operador_aritmetico")
		match("numero")
		ret = "INTEGER"
	else:
		reportar("Error de Sintaxis: se esperaba un numero, - o + ",preanalisis,"digitos")
	if verbose:
		print("<--digitos")
	return ret

def identificador():
	global identificadoresActuales
	global preanalisis
	ret = "VOID"
	if verbose:
		print("-->identificador")
	if(preanalisis == "identificador"):
		#Se añade el identificador a la lista de identificadores pendientes
		identificadoresActuales.append(analizadorLexico.lexema)
		#Sintactico
		match('identificador')
		ret = "VOID"
	else:
		reportar("Error de Sintaxis: se esperaba un identificador valido",preanalisis,"identificador")
	if verbose:
		print("<--identificador")
	return ret

def declaracionVariables():
	ret = "VOID"
	if verbose:
		print("-->declaracionVariables")
	if(preanalisis == 'var'):
		match('var')
		ret = listaVariables()
	else:
		reportar("Error de Sintaxis: se esperaba VAR",preanalisis,"declaracionVariables")
	if verbose:
		print("<--declaracionVariables")
	return ret

def listaVariables():
	ret = "VOID"
	if verbose:
		print("-->listaVariables")
	if(preanalisis == "identificador"):
		ret = listaIdentificador()
		match("dos_puntos")
		if not(tipoVariables() == ret):
			ret = "ERROR"
		match('punto_coma')
		if not(listaVariablesRep() == ret):
			ret = "ERROR"
	else:
		reportar("Error de Sintaxis: se esperaba un identificador valido",preanalisis,"listaVariables")
	if verbose:
		print("<--listaVariables")
	return ret

def listaVariablesRep():
	global identificadoresActuales
	ret = "VOID"
	if verbose:
		print("-->listaVariablesRep")
	if(preanalisis == "identificador"):
		#Semantico:Si se definen mas variables, es necesario re-comenzar la lista
		identificadoresActuales=[]
		#Sintactico
		ret = listaVariables()
	elif verbose:
		print('\033[93m'+"> Lambda")+'\033[0m'
	if verbose:
		print("<--listaVariablesRep")
	return ret

def listaIdentificador():
	ret = "VOID"
	if verbose:
		print("-->listaIdentificador")
	if(preanalisis == "identificador"):
		ret = identificador()
		if not(listaIdentificadorRep() == ret):
			ret = "ERROR"
	else:
		reportar("Error de Sintaxis: se esperaba un identificador valido",preanalisis,"listaIdentificador")
	if verbose:
		print("<--listaIdentificador")
	return ret

def listaIdentificadorRep():
	ret = "VOID"
	if verbose:
		print("-->listaIdentificadorRep")
	if preanalisis == "coma":
		match("coma")
		ret = identificador()
		if not listaIdentificadorRep()== ret:
			ret = "ERROR"
	elif verbose:
		print('\033[93m'+"> Lambda")+'\033[0m'
	if verbose:
		print("<--listaIdentificadorRep")
	return ret

def tipoVariables():
	ret = "VOID"
	if verbose:
		print("-->tipoVariable")
	if( preanalisis == "integer"):
		#Semantico: se añade el tipo a los identificadores almacenados
		generarEntradas(preanalisis)
		#Sintactico
		match("integer")
	elif( preanalisis == "boolean"):
		#Semantico: se añade el tipo a la lista de variables definida
		generarEntradas(preanalisis)
		#Sintactico
		match("boolean")
	else:
		reportar("Error de Sintaxis: se esperaba INTEGER o BOOLEAN",preanalisis,"tipoVariables")
	if verbose:
		print("<--tipoVariable")
	return ret

def sentenciaCompuesta():
	ret = "VOID"
	if verbose:
		print("-->sentenciaCompuesta")
	if(preanalisis == "begin"):
		match("begin")
		ret = compuesta()
		match("end")
		match("punto_coma")
	else:
		reportar("Error de Sintaxis: se esperaba BEGIN",preanalisis,"sentenciaCompuesta")
	if verbose:
		print("<--sentenciaCompuesta")
	return ret

def compuesta():
	ret = "VOID"
	if verbose:
		print("-->compuesta")
	case1 = {'write','while','read','if'}
	if ((preanalisis == "identificador") or (preanalisis in case1)):
		ret = sentencia()
		if not (sentenciaOptativa() == ret):
			ret = "ERROR"
	elif (preanalisis == "begin"):
		ret = sentenciaCompuesta()
	elif verbose:
		print('\033[93m'+"> Lambda")+'\033[0m'
	if verbose:
		print("<--compuesta")
	return ret

def sentenciaOptativa():
	ret = "VOID"
	if verbose:
		print("-->sentenciaOptativa")
	if(preanalisis == "punto_coma"):
		match("punto_coma")
		#sentenciaOptativa2()
		ret = compuesta()
	elif verbose:
		print('\033[93m'+"> Lambda")+'\033[0m'
	if verbose:
		print("<--sentenciaOptativa")
	return ret

def no():
	ret = "VOID"
	if verbose:
		print("-->no")
	if(preanalisis == "not"):
		match("not")
	elif verbose:
		print('\033[93m'+"> Lambda")+'\033[0m'
	if verbose:
		print("<--no")
	return ret

def sentencia():
	ret = "VOID"
	if verbose:
		print("-->sentencia")
	if(preanalisis == "if"):
		ret = ifthen()
	elif(preanalisis == 'while'):
		ret = mientras()
	elif(preanalisis == 'write'):
		match("write")
		match("parentesis_a")
		expresionGeneral()
		match("parentesis_c")
	elif(preanalisis == "read"):
		match("read")
		match("parentesis_a")
		identificador()
		try:
			tablaActual[identificadoresActuales.pop()]
		except KeyError:
			ret = "ERROR"
		match("parentesis_c")
	elif(preanalisis == "identificador"):
		ret = identificador()
		if not asignacionollamada() == tablaActual[identificadoresActuales.pop()]["tipo"]:
			ret = "ERROR"
	else:
		reportar("Error de Sintaxis: se esperaba READ, WRITE, IF, WHILE o Identificador Valido",preanalisis,"sentencia")
	if verbose:
		print("<--sentencia")
	return ret

def asignacionollamada():
	ret = "VOID"
	if verbose:
		print("-->asignacionollamada")
	if preanalisis == "asignacion":
		match("asignacion")
		ret = expresionGeneral()
	elif preanalisis == "parentesis_a":
		ret = llamada()
	elif preanalisis == "punto_coma":
		match("punto_coma")
	else:
		reportar("Error de sintaxis: se esperaba :=, (, o ;",preanalisis,"asignacionollamada")
	if verbose:
		print("<--asignacionollamada")
	return ret

def expresionAritmetica():
	ret = "VOID"
	if verbose:
		print("-->expresionAritmetica")
	case1 = {"write","true","false","read","parentesis_a","operador_aritmetico"}
	if (preanalisis == "identificador") or (preanalisis == "numero") or (preanalisis in case1):
		ret = termino()
		ret = expresionAritmetica1(ret)
	else:
		reportar("Error de sintaxis: se esperaba READ, WRITE, TRUE, FALSE, Identificador valido o digitos",preanalisis,"expresionAritmetica1")
	if verbose:
		print("<--expresionAritmetica")
	return ret

def expresionAritmetica1(ret):
	if verbose:
		print("-->expresionAritmetica1")
	if preanalisis == "operador_aritmetico":
		match("operador_aritmetico")
		ret2 = termino()
		if not(ret == "INTEGER" and ret2=="INTEGER"):
			ret = "ERROR"
		ret = expresionAritmetica1(ret)
	elif verbose:
		print('\033[93m'+"> Lambda")+'\033[0m'
	if verbose:
		print("<--expresionAritmetica1")
	return ret

def termino():
	ret = "VOID"
	if verbose:
		print("-->termino")
	case1 = {"write","true","false","read","operador_aritmetico","parentesis_a"}
	if((preanalisis == "identificador") or (preanalisis == "numero") or (preanalisis in case1)):
		ret = factor()
		ret = termino1(ret)
	else:
		reportar("Error de Sintaxis: se esperaba WRITE,READ,TRUE,FALSE,Identificador valido o Digitos",preanalisis,"expresionAritmetica1")
	if verbose:
		print("<--termino")
	return ret

def termino1(ret):
	if verbose:
		print("-->termino1")
	if preanalisis == "operador_termino":
		match("operador_termino")
		if not factor()==ret:
			#No son de tipo compatible
			ret = "ERROR"
		termino1(ret)
	elif verbose:
		print('\033[93m'+"> Lambda")+'\033[0m'
	if verbose:
		print("<--termino1")
	return ret

def factor():
	ret = "VOID"
	parametros = {}
	if verbose:
		print("-->factor")
	if (preanalisis == "identificador"):
		identificador()
		try:
			id = tablaActual[identificadoresActuales.pop()]
			if id["tipo"] in {"function","procedure"}:
				parametros = id["parametros"]
		except KeyError:
			ret = "ERROR"
		ret = llamada(parametros)
	elif (preanalisis == "write"):
		match("write")
		match("parentesis_a")
		expresionGeneral()
		match("parentesis_c")
	elif (preanalisis == "read"):
		match("read")
		match("parentesis_a")
		identificador()
		try:
			ret = tablaActual[identificadoresActuales.pop()]["tipo"]
		except KeyError:
			#No existe el identificador
			ret="ERROR"
		match("parentesis_c")
	elif preanalisis == "numero" or preanalisis == "operador_aritmetico":
		ret = digitos()
	elif preanalisis == "true":
		match("true")
		ret = "BOOLEAN"
	elif preanalisis == "false":
		match("false")
		ret = "BOOLEAN"
	elif preanalisis == "parentesis_a":
		match("parentesis_a")
		ret = expresionGeneral()
		match("parentesis_c")
	else:
		reportar("Error de sintaxis: se esperaba WRITE,READ,TRUE,FALSE,DIGITO,NOT,( o Identificador valido",preanalisis,"factor")
	if verbose:
		print("<--factor")
	return ret

def operadorRelacional():
	ret = "VOID"
	if verbose:
		print("-->operadorRelacional")
	if preanalisis == "operador_relacional":
		match("operador_relacional")
	else:
		reportar("Error de sintaxis: se esperaba un operador relacional <,<=,=>,>,<> o =",preanalisis,"operadorRelacional")
	if verbose:
		print("<--operadorRelacional")
	return ret

def programa():
	ret = "VOID"
	global tablaSimbolos
	global tablaActual
	global identificadoresActuales
	if verbose:
		print("-->programa")
	if preanalisis == "program":
		#Semantico:Creación de la Tabla de Simbolos y actualización de la tabla actual
		tablaSimbolos = Tabla()
		tablaActual = tablaSimbolos
		#Sintactico
		match("program")
		identificador()
		#Semantico: Generamos la entrada para el nombre de Program
		generarEntradas("program")
		#Sintactico
		match("punto_coma")
		ret3 = declaracionVariableOpt()
		#programaRepPyf()
		ret1 = declaracionPyfRep()
		match("begin")
		ret2 = programaRepSentencia()
		#ret2 = sentenciaCompuesta()
		match("end")
		match("punto")
		if not(ret3 == "VOID" and ret1 == "VOID" and ret2 == "VOID"):
			ret = "ERROR"
	else:
		reportar("Error de sintaxis: debe comenzar con la sentencia PROGRAM Identificador",preanalisis,"programa")
	if verbose:
		print("<--programa")
		print repr(tablaSimbolos)
		return ret

def declaracionVariableOpt():
	ret = "VOID"
	if verbose:
		print("-->declaracionVariablesOpt")
	if preanalisis == "var":
		ret = declaracionVariables()
	elif verbose:
		print('\033[93m'+"> Lambda")+'\033[0m'
	if verbose:
		print("<--declaracionVariablesOpt")
	return ret


def programaRepSentencia():
	ret = "VOID"
	if verbose:
		print("-->programaRepSentencia")
	caso1={"begin", "read", "write","while","if"}
	if (preanalisis in caso1) or (preanalisis == "identificador"):
		ret = compuesta()
		if not programaRepSentencia() == ret:
			ret = "ERROR"
	elif verbose:
		print('\033[93m'+"> Lambda")+'\033[0m'
	if verbose:
		print("<--programaRepSentencia")
	return ret

def expresionGeneral():
	if verbose:
		print("-->expresionGeneral")
	caso1={'false', 'true', 'parentesis_a', 'operador_aritmetico', 'write', 'read','not'}#,'and'}
	if((preanalisis == "identificador") or (preanalisis == "numero") or (preanalisis in caso1)):
		#compararAnd()
		no()
		ret = expresionAritmetica()
		ret = expresionRelacional(ret)
		ret = compararAnd(ret)
		ret = expresionGeneral1(ret)
	else:
		reportar("Error de sintaxis: se esperaba WRITE,READ,NOT,TRUE,FALSE,(,-,Digito o Identificador valido",preanalisis,"expresionGeneral")
	if verbose:
		print("<--expresionGeneral")
	return ret

def expresionGeneral1(ret):
	if verbose:
		print("-->expresionGeneral1")
	if preanalisis == "or":
		match("or")
		if not(expresionGeneral()==ret):
			ret = "ERROR"
		else:
			ret = "BOOLEAN"
	elif verbose:
		print('\033[93m'+"> Lambda")+'\033[0m'
	if verbose:
		print("<--expresionGeneral1")
	return ret

def expresionRelacional(ret):
	if verbose:
		print("-->expresionAritmetica2")
	if(preanalisis  == "operador_relacional"):
		operadorRelacional()
		if not ret == expresionAritmetica():
			ret = "ERROR"
		else:
			ret = "BOOLEAN"
	elif verbose:
		print('\033[93m'+"> Lambda")+'\033[0m'
	if verbose:
		print("<--expresionAritmetica2")
	return ret

def compararAnd(ret):
	if verbose:
		print("-->compararAnd")
	if preanalisis == "and":
		match("and")
		no()
		ret2 = expresionAritmetica()
		if not(expresionRelacional(ret2) == ret):
			ret = "ERROR"
		compararAnd(ret)
	elif verbose:
		print('\033[93m'+"> Lambda")+'\033[0m'
	if verbose:
		print("<--compararAnd")
	return ret

def ifthen():
	ret = "VOID"
	if verbose:
		print("-->ifthen")
	if preanalisis == "if":
		match("if")
		if not(expresionGeneral() == "BOOLEAN"):
			ret = "ERROR"
		match("then")
		ret = ifthen1()
	else:
		reportar("Error de sintaxis: se esperaba IF expresion THEN",preanalisis,"ifthen")
	if verbose:
		print("<--ifthen")
	return ret

def ifthen1():
	ret = "VOID"
	if verbose:
		print("-->ifthen1")
	caso2={"read", "write","while","if"}
	if preanalisis == "begin":
		match("begin")
		ret = compuesta()
		match("end")
		if not alternativa() == ret:
			ret = "ERROR"
	elif ((preanalisis in caso2) or (preanalisis == "identificador")):
		ret = sentencia()
		if not alternativa()==ret:
			ret = "ERROR"
	else:
		reportar("Error de sintaxis: se esperaba WRITE,READ,WHILE,IF,BEGIN o Identificador valido",preanalisis,"ifthen1")
	if verbose:
		print("<--ifthen1")

def alternativa():
	ret = "VOID"
	if verbose:
		print("-->alternativa")
	if  (preanalisis == "punto_coma"):
		match("punto_coma")
	elif (preanalisis == "else"):
		match("else")
		ret = compuesta()
	else:
		reportar("Error de sintaxis: se esperaba ; o ELSE",preanalisis,"alternativa")
	if verbose:
		print("<--alternativa")
	return ret

def mientras():
	ret = "VOID"
	if verbose:
		print("-->mientras")
	if ( preanalisis == "while"):
		match("while")
		if not(expresionGeneral()=="BOOLEAN"):
			ret = "ERROR"
		match("do")
		if (ret == "VOID"):
			ret = sentenciaCompuesta()
		else:
			sentenciaCompuesta()
	else:
		reportar("Error de sintaxis: se esperaba WHILE",preanalisis,"mientras")
	if verbose:
		print("<--mientras")
	return ret

def declaracionPyf():
	global tablaActual
	global identificadoresActuales
	ret = "VOID"
	nombreSubprograma=""
	if verbose:
		print("-->declaracionPyf")
	if preanalisis == "procedure":
		#Sintactico
		match("procedure")
		identificador()
		#Semantico: Generar entrada en la Tabla para el procedimiento
		nombreSubprograma = identificadoresActuales[0] #guardamos temporalmente el nombre del subprograma
		generarEntradas("procedure") #generamos la entrada en la Tabla de Simbolos para el subprograma
		#Semantico: Cambio de ambito: de Program a Procedure -lectura de parametros-
		tablaActual = tablaActual.new_child() #generamos un contexto para guardar los parametros
		#Sintactico
		ret = parametrosFormales()
		#Semantico: Los parametros deben figurar como variables en el contexto del procedure que es el nuevo actual
		tablaActual.parent[nombreSubprograma].update({"parametros":dict(tablaActual.map.items())}) #guardamos los parametros en la Tabla de Simbols del padre
		#Sintactico
		match("punto_coma")
		ret1 = declaracionVariableOpt()
		ret2 = declaracionPyfRep()
		ret3 = sentenciaCompuesta()
		if not(ret == "VOID" and ret1 == "VOID" and ret2 == "VOID" and not(ret3 == "ERROR")):
			ret = "ERROR"
		#Semantico: Cambio de contexto: desapilo la tabla procedure
		identificadoresActuales=[]
		tablaActual = tablaActual.parent
	elif preanalisis == "function":
		#Sintactico
		match("function")
		identificador()
		#Semantico: Generar entrada en la Tabla para el procedimiento y almacenar el nombre de la funcion para su variable ret
		nombreSubprograma = identificadoresActuales[0] #guardamos temporalmente el nombre del subprograma
		variableRetorno = identificadoresActuales
		generarEntradas("function")
		#Semantico: Cambio de contexto: de Program a Function
		tablaActual = tablaActual.new_child()
		#Sintactico
		ret1 = parametrosFormales()
		#Semantico: Los parametros deben figurar como variables en el contexto del procedure que es el nuevo actual
		tablaActual.parent[nombreSubprograma].update({"parametros":dict(tablaActual.map.items())}) #guardamos los parametros en la Tabla de Simbols del padre
		match("dos_puntos")
		#Semantico: Definimos la variable de retorno para ser insertada con su tipo de Variable
		identificadoresActuales = variableRetorno
		#Sintactico
		ret = tipoVariables()
		match("punto_coma")
		ret1 = declaracionVariableOpt()
		ret2 = declaracionPyfRep()
		ret3 = sentenciaCompuesta()
		if not(ret1 == "VOID" and ret2 == "VOID" and not(ret3 == "ERROR")):
			ret = "ERROR"
		#Semantico: Cambio de contexto: desapilo la tabla de function
		identificadoresActuales=[]
		tablaActual = tablaActual.parent
	else:
		reportar("Error de sintaxis: se esperaba PROCEDURE o FUNCTION",preanalisis,"declaracionPyf")
	if verbose:
		print("<--declaracionPyf")
	return ret

def parametrosFormales():
	ret = "VOID"
	if verbose:
		print("-->parametrosRep")
	if  preanalisis == "parentesis_a":
		match("parentesis_a")
		ret = listaIdentificador()
		match("dos_puntos")
		if not(tipoVariables() == ret):
			ret = "ERROR"
		if not(parametrosFormalesRep() == "VOID"):
			ret = "ERROR"
		match("parentesis_c")
	elif verbose:
		print('\033[93m'+"> Lambda")+'\033[0m'
	if verbose:
		print("<--parametrosRep")
	return ret

# def declaracionVariablesRep():
# 	ret = "VOID"
# 	if(verbose):
# 		print("-->declaracionVariablesRep")
# 	if ( preanalisis == "var"):
# 		ret = declaracionVariables()
# 	elif verbose:
# 		print('\033[93m'+"> Lambda")+'\033[0m'
# 	if(verbose):
# 		print("<--declaracionVariablesRep")
# 	return ret

def declaracionPyfRep():
	ret = "VOID"
	if(verbose):
		print("-->declaracionPyfRep")
	if ( preanalisis == "function" or preanalisis == "procedure"):
		ret = declaracionPyf()
		if not(declaracionPyfRep() == ret):
			ret == "ERROR"
	elif verbose:
		print('\033[93m'+"> Lambda")+'\033[0m'
	if(verbose):
		print("<--declaracionPyfRep")
	return ret

def parametrosFormalesRep():
	ret = "VOID"
	if(verbose):
		print("-->parametrosFormalesRep")
	if ( preanalisis == "punto_coma"):
		match("punto_coma")
		listaIdentificador()
		match("dos_puntos")
		tipoVariables()
		parametrosFormalesRep()
	elif verbose:
		print('\033[93m'+"> Lambda")+'\033[0m'
	if(verbose):
		print("<--parametrosFormalesRep")
	return ret

def parametrosReales(parametros):
	ret = "VOID"
	if verbose:
		print("-->parametrosReales")
	if ( preanalisis == "coma"):
		match("coma")
		ret = expresionGeneral()
		try:
			if not ret == parametros.popitem(False).tipo:
					#Tipo de parametro incorrecto
					ret="ERROR"
			parametrosReales(parametros)
		except IndexError:
			#Cantidad de parametros incorrecta
			ret="ERROR"
	elif verbose:
		print('\033[93m'+"> Lambda")+'\033[0m'
	if verbose:
		print("<--parametrosReales")
	return ret

def llamada(parametros):
	ret = "VOID"
	if verbose:
		print("-->llamada")
	if preanalisis == "parentesis_a":
		match("parentesis_a")
		ret = expresionGeneral()
		try:
			if not ret == parametros.popitem(False).tipo:
				#Tipo de parametro incorrecto
				ret="ERROR"
			parametrosReales(parametros)
		except IndexError:
			#Cantidad de parametros incorrecta
			ret="ERROR"
		match("parentesis_c")
	elif verbose:
		print('\033[93m'+"> Lambda")+'\033[0m'
	if verbose:
		print("<--llamada")
	return ret

#Procedimiento Match dado en la teoria
def match(t):
	global preanalisis
	global preanalisisAnterior
	global nroLinea

	if(preanalisis == t):
		if(verbose):
			print '\033[93m'+">Match:"+str(preanalisis)+'\033[0m'
		preanalisisAnterior = preanalisis
		preanalisis = analizadorLexico.siguientePreanalisis()
		if(verbose):
			print '\033[1m'+">Preanalisis:"+str(preanalisis)+'\033[0m'
	else:
		reportarMatch("["+str(analizadorLexico.nroLinea)+"] "+"Error de sintaxis, no se esperaba ",preanalisis,preanalisisAnterior,"match")

def reportar(tipoError,simbolo,metodo,tipoReporte="Sintactico"):
	global error
	global preanalisisAnterior
	global nroLinea
	if tipoReporte=="Sintactico":
		err = "["+str(analizadorLexico.nroLinea)+"] "+tipoError+ " en la expresion "+ repr(preanalisis)+" despues de "+ repr(preanalisisAnterior)+"\n"
	elif tipoReporte=="Semantico":
		err = "["+str(analizadorLexico.nroLinea)+"] "+tipoError+ " ya definido antes de definirse como "+ repr(preanalisis)+"\n"
	if(args.standalone):
		print err
		exit(0)
	else:
		error.append(err)

def reportarMatch(tipoError,simbolo,simboloanterior,metodo):
	global error
	if(simboloanterior == preanalisis):
		err= tipoError+ " "+ repr(preanalisis) +". El archivo debe finalizar con END seguido de punto."+"\n"
	else:
		err= tipoError+ " "+ repr(preanalisis) +" despues de "+ repr(simboloanterior)+"\n"
	if(args.standalone):
		print err
		exit(0)
	else:
		error.append(err)

def between(value, a, b):
    # Find and validate before-part.
    pos_a = value.find(a)
    if pos_a == -1: return ""
    # Find and validate after part.
    pos_b = value.rfind(b)
    if pos_b == -1: return ""
    # Return middle part.
    adjusted_pos_a = pos_a + len(a)
    if adjusted_pos_a >= pos_b: return ""
    return value[adjusted_pos_a:pos_b]

def main():
	#Error
	global error
	error=[]

	#Tokens
	global tokens
	tokens=[]

	global nroLinea
	global preanalisis

	archivo = args.archivo
	archivo += ".tokens"
	#Procesamos el archivo linea por linea
	nroLinea=1
	with open(archivo) as f:
	    for line in f:
			linea = between(line,'[',',')
			linea = linea[1:-1]
			if(linea != ''):
				tokens.append(linea.lower())
	f.close()

	#Comenzamos a procesar los tokens encontrados sabiendo que un programa Pascal comienza con la sentencia program
	if(posicion < len(tokens)):
		preanalisis = tokens[posicion]
		if(verbose):
			print('\033[93m'+"-------->TRAZA DE EJECUCION DE LA GRAMATICA:"+'\033[0m')
		programa()
		print('\033[93m'+"Fin de la ejecucion"+'\033[0m')
	#Salida de Tokens
	if(args.verbose_mode):
	        print tokens

def procesar():
	global preanalisis
	global error

	#Comenzamos a procesar los tokens encontrados sabiendo que un programa Pascal comienza con la sentencia program
	preanalisis = analizadorLexico.siguientePreanalisis()
	if(verbose):
		print("-------->TRAZA DE EJECUCION DE LA GRAMATICA:")
	programa()
	#Salida de Tokens
	#if(args.verbose_mode):
	#        print tokens

	if(error):
		error = list(set(error))
		print '\033[91m'+"ERRORES DETECTADOS: "+ repr(len(error))
		print '\033[93m'+"[Nro de Linea] Descripcion del error"+'\033[0m'
		for e in error:
			print e
		os.system('kill %d' % os.getpid())
	else:
	        print "Analisis finalizado. No hay errores detectados"

##DEFINICIONES SEMANTICO
def generarEntradas(tipo):
	global identificadoresActuales
	global tablaActual
	#Añadir cada identificador a la tabla con el tipo asociado
	for identificador in identificadoresActuales:
		#si el identificador existe: añadimos el error
		try:
			tablaActual.map[identificador]
			reportar("Identificador "+repr(identificador)+" ya definido",identificador,"generarVariables","Semantico")
		#El identificador no existe
		except KeyError:
			tablaActual[identificador]={"tipo":tipo}
			if(verbose):
				print ('\033[92m'+"[SEMANTICO] Nueva entrada: "+repr(identificador)+" : "+repr(tipo)+'\033[0m')
	#Ya se guardaron todos los identificadores en la tabla de simbolos
	identificadoresActuales=[]

if __name__ == '__main__':
	#Definicion de argumentos y pasaje de parametros.
	parser = argparse.ArgumentParser(description="Analizador Sintactico de Pascal Reducido")
	parser.add_argument("archivo", help="Ruta relativa del fichero a analizar sintacticamente.", type=str)
	parser.add_argument("-verbose_mode","-v", help="Flag para modo Verboso con todas las impresiones de control.",action='store_true')
	parser.add_argument("-standalone","-s", help="Flag para funcionamiento por separado del aplicativo.",action='store_true')
	args = parser.parse_args()
	verbose= args.verbose_mode

	if(args.standalone):
		main()
	else:
		procesar()
