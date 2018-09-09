#!/usr/bin/env python
# coding=utf-8

#Authors: Bonet Peinado Daiana, de la Fuente Juan M.
#Year: 2018
#License: GNU GPLv3. See LICENSE file for more information.


import string
import random
import argparse
import re
import os
#from analizadorLexico import siguientePreanalisis
import analizadorLexico
#import analizadorLexico



##Variables globales

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

#global nroLinea

#Palabras reservadas
global palabrasReservadas
palabrasReservadas=["begin","bool","end","while","true","false","if","else","program","do","then","and","or","function","integer","procedure","read","var","write"]


#Definicion de casos posibles

def digitos():
	if(verbose):
		print("digitos")
	if(preanalisis == "numero"):
		match("numero")
	elif (preanalisis == "operador_aritmetico"):
		match("operador_aritmetico")
		match("numero")
	else:
		reportar("Error de Sintaxis: se esperaba un numero o - ",preanalisis,"digitos")


def identificador():
	if(verbose):
		print("identificador")
	global preanalisis
	if(preanalisis == "identificador"):
		match('identificador')
	else:
		reportar("Error de Sintaxis: se esperaba un identificador valido",preanalisis,"identificador")
                    
def declaracionVariables():
	if(verbose):
		print("declaracionVariables")
	if(preanalisis == 'var'):
		match('var')
		listaVariables()
		
	else:
		reportar("Error de Sintaxis: se esperaba VAR",preanalisis,"declaracionVariables")

def listaVariables():
	if(verbose):
		print("listaVariables")
	if(preanalisis == "identificador"):
		listaIdentificador()
		match("dos_puntos")
		tipoVariables()
		match('punto_coma')
		listaVariablesRep()
	else:
		reportar("Error de Sintaxis: se esperaba un identificador valido",preanalisis,"listaVariables")

def listaVariablesRep():
	if(verbose):
		print("listaVariablesRep")
	if(preanalisis == "identificador"):
		listaVariables()


def listaIdentificador():
	if(verbose):
		print("listaIdentificador")
	if(preanalisis == "identificador"):
		identificador()
		listaIdentificadorRep()
	else:
		reportar("Error de Sintaxis: se esperaba un identificador valido",preanalisis,"listaIdentificador")

def listaIdentificadorRep():
	if(verbose):
		print("listaIdentificadorRep")
	if( preanalisis == "coma"): 
		match("coma")
		identificador()
		listaIdentificadorRep()

def tipoVariables():
	if(verbose):
		print("tipoVariable")
	if( preanalisis == "integer"):
		match("integer")
	elif( preanalisis == "boolean"):
		match("boolean")
	else:
		reportar("Error de Sintaxis: se esperaba INTEGER o BOOLEAN",preanalisis,"tipoVariables")


def sentenciaCompuesta():
	if(verbose):
		print("sentenciaCompuesta")
	if(preanalisis == "begin"):
		match("begin")
		compuesta()
		match("end")
		match("punto_coma")
	else:
		reportar("Error de Sintaxis: se esperaba BEGIN",preanalisis,"sentenciaCompuesta")

def compuesta():
	if(verbose):
		print("compuesta")
	case1 = {'write','while','read','if'}
	if ((preanalisis == "identificador") or (preanalisis in case1)):
		sentencia()
		sentenciaOptativa()
	elif (preanalisis == "begin"):
		sentenciaCompuesta()
	else:
		reportar("Error de Sintaxis: se esperaba WRITE, READ, WHILE, IF, un identificador valido o BEGIN",preanalisis,"compuesta")

def sentenciaOptativa():
	if(verbose):
		print("sentenciaOptativa")
	if(preanalisis == "punto_coma"):
		match("punto_coma")
		sentenciaOptativa2()

def sentenciaOptativa2():
	if(verbose):
		print("sentenciaOptativa2")
	case1 = {"begin",'write','while','read','if'}
	if ((preanalisis == "identificador") or (preanalisis in case1)):
		compuesta()

def no():
	if(verbose):
		print("not")
	if(preanalisis == "not"):
		match("not")
		

def sentencia():
	if(verbose):
		print("sentencia")
	if(preanalisis == "if"):
		ifthen()
	elif(preanalisis == 'while'):
		mientras()
	elif(preanalisis == 'write'):
		match("write")
		match("parentesis_a")
		expresionGeneral()
		match("parentesis_c")
	elif(preanalisis == "read"):
		match("read")
		match("parentesis_a")
		identificador()
		match("parentesis_c")
	elif(preanalisis == "identificador"):
		identificador()
		asignacionollamada()
	else:
		reportar("Error de Sintaxis: se esperaba READ, WRITE, IF, WHILE o Identificador Valido",preanalisis,"sentencia")


def asignacionollamada():
	#caso2={"operador_termino","operador_aritmetico","operador_relacional","and","or","parentesis_c","parentesis_a","then","do"}
	if(verbose):
		print("asignacionollamada")
	if (preanalisis == "asignacion"):
		match("asignacion")
		expresionGeneral()
	elif (preanalisis == "parentesis_a"):
		llamada1()
	elif (preanalisis == "punto_coma"):
		match("punto_coma")
	else:
		reportar("Error de sintaxis: se esperaba :=, (, o ;",preanalisis,"asignacionollamada")


def expresionAritmetica():
	if(verbose):
		print("expresionAritmetica")
	case1 = {"write","true","false","read","parentesis_a","operador_aritmetico"}
	if((preanalisis == "identificador") or (preanalisis == "numero") or (preanalisis in case1)):
		termino() 
		expresionAritmetica1()
	else:
		reportar("Error de sintaxis: se esperaba READ, WRITE, TRUE, FALSE, Identificador valido o digitos",preanalisis,"expresionAritmetica1")
        
def expresionAritmetica1():
	if(verbose):
		print("expresionAritmetica1")
	if ( preanalisis == "operador_aritmetico"):
	  match("operador_aritmetico")
	  termino()
	  expresionAritmetica1()


def termino():
	if(verbose):
		print("termino")
	case1 = {"write","true","false","read","operador_aritmetico","parentesis_a"}
	if((preanalisis == "identificador") or (preanalisis == "numero") or (preanalisis in case1)):
			factor()
			termino1()
	#elif(preanalisis=='parentesis_a'):
	#		match("parentesis_a")
	#		expresionGeneral()
	#		match("parentesis_c")
	else:
			reportar("Error de Sintaxis: se esperaba WRITE,READ,TRUE,FALSE,Identificador valido o Digitos",preanalisis,"expresionAritmetica1")

def termino1():
	if(verbose):
		print("termino1")
	if (preanalisis == "operador_termino"):
		match("operador_termino")
		factor()
		termino1()
		
def factor():
	if(verbose):
		print("factor")
	if (preanalisis == "identificador"):
		identificador()
		llamada1()
	elif (preanalisis == "write"):
		match("write")
		match("parentesis_a")
		llamada2()
	elif (preanalisis == "read"):
		match("read")
		match("parentesis_a")
		identificador()
		match("parentesis_c")
	elif (preanalisis == "numero" or preanalisis == "operador_aritmetico"):
		digitos()
	elif (preanalisis == "true"):
		match("true")
	elif (preanalisis == "false"):
		match("false")
	elif (preanalisis == "parentesis_a"):
		match("parentesis_a")
		expresionGeneral()
		match("parentesis_c")
	else:
		reportar("Error de sintaxis: se esperaba WRITE,READ,TRUE,FALSE,DIGITO,NOT,( o Identificador valido",preanalisis,"factor")

# def factor1():
# 	if(verbose):
# 		print("factor1")
# 	if ( preanalisis == "parentesis_a"):
# 		match("parentesis_a")
# 		llamada1()
		
def operadorRelacional():
	if(verbose):
		print("operadorRelacional")
	if ( preanalisis == "operador_relacional"):
				match("operador_relacional")
	else:
				reportar("Error de sintaxis: se esperaba un operador relacional <,<=,=>,>,<> o =",preanalisis,"operadorRelacional")
				
def programa():
	if(verbose):
		print("programa")
	if ( preanalisis == "program"):
			 match("program")
			 identificador()
			 match("punto_coma")
			 declaracionVariableOpt()
			 programaRepPyf()
			 match("begin")
			 programaRepSentencia()
			 match("end")
			 match("punto")
	else:
			 reportar("Error de sintaxis: debe comenzar con la sentencia PROGRAM Identificador",preanalisis,"programa")


def declaracionVariableOpt():
	if(verbose):
		print("declaracionVariablesOpt")
	if ( preanalisis == "var"):
		declaracionVariables()

def programaRepPyf():
	if(verbose):
		print("programaRepPyf")
	if (( preanalisis == "function") or (preanalisis == "procedure")):
		declaracionPyf()
		programaRepPyf()
	

def programaRepSentencia():
	if(verbose):
		print("programaRepSentencia")
	caso1={"begin", "read", "write","while","if"}
	if ( (preanalisis in caso1) or (preanalisis == "identificador")):
		compuesta()
		programaRepSentencia()
	
def expresionGeneral():
	if(verbose):
		print("expresionGeneral")
	caso1={'false', 'true', 'parentesis_a', 'operador_aritmetico', 'write', 'read','not'}#,'and'}
	if((preanalisis == "identificador") or (preanalisis == "numero") or (preanalisis in caso1)):
		compararAnd()
		expresionGeneral1()
	else:
		reportar("Error de sintaxis: se esperaba WRITE,READ,NOT,TRUE,FALSE,(,-,Digito o Identificador valido",preanalisis,"expresionGeneral")

def expresionGeneral1():
	if(verbose):
		print("expresionGeneral1")
	if(preanalisis == "or"):
		match("or")
		compararAnd()
		expresionGeneral1()

def compararAnd():
	if(verbose):
		print("compararAnd")
	caso2={'false', 'true', 'operador_aritmetico', 'write', 'read', 'parentesis_a','not'}
	#if(preanalisis == "and"): #or preanalisis== "parentesis_a"):
		#no()
	#	match("parentesis_a")
	#	expresionGeneral()
	#	match("parentesis_c")
     #           termino1()
	#	compararAnd1()
	if ((preanalisis == "identificador" or preanalisis == "numero" ) or (preanalisis in caso2)):
		no()
		expresionAritmetica() 
		expresionAritmetica2() 
		compararAnd1()
	else:
		reportar("Error de sintaxis: se esperaba WRITE,READ,TRUE,FALSE,NOT,(,-,Digito o Identificador valido",preanalisis,"expresionGeneral")

def expresionAritmetica2():
	if(verbose):
		print("expresionAritmetica2")
	if(preanalisis  == "operador_relacional"):
		operadorRelacional()
		expresionAritmetica()

def compararAnd1():
	if(verbose):
		print("compararAnd1")
	if(preanalisis == "and"):
		match("and")
		compararAnd()


def ifthen():
	if(verbose):
		print("ifthen")
	if ( preanalisis == "if"):
		match("if")
		expresionGeneral()
		match("then")
		ifthen1()
	else:
		reportar("Error de sintaxis: se esperaba IF expresion THEN",preanalisis,"ifthen")

def ifthen1():
	if(verbose):
		print("ifthen1")
	caso2={"read", "write","while","if"}
	if ( preanalisis == "begin"):
		match("begin")
		compuesta()
		match("end")
		alternativa()
	elif ((preanalisis in caso2) or (preanalisis == "identificador")):
		sentencia()
		alternativa()
	else: 
		reportar("Error de sintaxis: se esperaba WRITE,READ,WHILE,IF,BEGIN o Identificador valido",preanalisis,"ifthen1")

def alternativa():
	if(verbose):
		print("alternativa")
	if  (preanalisis == "punto_coma"):
		match("punto_coma")
	elif (preanalisis == "else"):
		match("else")
		compuesta()
	else:
		reportar("Error de sintaxis: se esperaba ; o ELSE",preanalisis,"alternativa")
 
def mientras():
	if(verbose):
		print("mientras")
	if ( preanalisis == "while"):
		match("while")
		expresionGeneral()
		match("do")
		sentenciaCompuesta()
	else:
		reportar("Error de sintaxis: se esperaba WHILE",preanalisis,"mientras")

def declaracionPyf():
	if(verbose):
		print("declaracionPyf")
	if ( preanalisis == "procedure"):
		match("procedure")
		identificador()
		parametrosRep()
		match("punto_coma")
		declaracionVariableOpt()
		declaracionPyfRep()
		sentenciaCompuesta()
	elif ( preanalisis == "function"):
		match("function")
		identificador()
		parametrosRep()
		match("dos_puntos")
		tipoVariables()
		match("punto_coma")
		declaracionVariableOpt()
		declaracionPyfRep()
		sentenciaCompuesta()
	else:
		reportar("Error de sintaxis: se esperaba PROCEDURE o FUNCTION",preanalisis,"declaracionPyf")

def parametrosRep():
	if(verbose):
		print("parametrosRep")
	if ( preanalisis == "parentesis_a"):
		match("parentesis_a")
		listaIdentificador()
		match("dos_puntos")
		tipoVariables()
		parametrosFormalesRep()	 
		match("parentesis_c")
		
def declaracionVariablesRep():
	if(verbose):
		print("declaracionVariablesRep")
	if ( preanalisis == "var"):
		declaracionVariables()

def declaracionPyfRep():
	if(verbose):
		print("declaracionPyfRep")
	if ( preanalisis == "function" or preanalisis == "procedure"):
		declaracionPyf()
		declaracionPyfRep()
	
	
def parametrosFormalesRep():
	if(verbose):
		print("parametrosFormalesRep")
	if ( preanalisis == "punto_coma"):
		match("punto_coma")
		listaIdentificador()
		match("dos_puntos")
		tipoVariables()
		parametrosFormalesRep()

def parametrosReales():
	if(verbose):
		print("parametrosReales")
	caso1={'false', 'true', 'parentesis_a', 'operador_aritmetico', 'write', 'read', 'operador_logico'}
	if(preanalisis == "identificador") or (preanalisis == "numero") or (preanalisis in caso1):
		expresionGeneral()
		parametrosRealesRep()

def parametrosRealesRep():
	if(verbose):
		print("parametrosRealesRep")
	if ( preanalisis == "coma"):
		match("coma")
		expresionGeneral()
		parametrosRealesRep()

def llamadaProcedimiento():
	if(verbose):
		print("llamadaProcedimiento")
	if ( preanalisis == "write"):
		match("write")
		match("parentesis_a")
		llamada2()
		#parametrosRealesRep()
	elif ( preanalisis == "read"):
		match("read")
		match("parentessis_a")
		identificador()
		match("parentesis_c")
	elif ( preanalisis == "identificador"):
		identificador()
		llamada1()
	else:
		reportar("Error de sintaxis: se esparaba llamada a Procedimiento o Funcion",preanalisis,"llamadaProcedimiento")

def llamada1():
	if(verbose):
		print("llamada1")
	#caso2={'false', 'true', 'parentesis_a', 'operador_aritmetico', 'write', 'read', 'operador_logico'}
	if(preanalisis == "parentesis_a"):
		match("parentesis_a")
		parametrosReales()
		parametrosReales2()
		match("parentesis_c")
	
def llamada2():
	if(verbose):
		print("llamada2")
	if ( (preanalisis == "identificador")):
		identificador()
		match("parentesis_c")
	elif ( preanalisis == "identificador") or (preanalisis == "operador_aritmetico"):
		digitos()
		match("parentesis_c")
	else:
		reportar("Error de sintaxis: se esperaba Digitos o un Identificador Valido",preanalisis,"llamada2")


def parametrosReales2():
	if(verbose):
		print("parametrosReales2")
	if ( preanalisis == "coma"):
		match("coma")
		parametrosReales()
		parametrosReales2()

#Procedimiento Match dado en la teoria
def match(t):
	global tokens
	global posicion
	global preanalisis
	global preanalisisAnterior
	global nroLinea

	if(preanalisis == t):
		if(verbose):
			print ">Match:"+str(preanalisis)        
		preanalisisAnterior = preanalisis
		preanalisis = analizadorLexico.siguientePreanalisis()
		if(verbose):
			print ">PREANALISIS:"+str(preanalisis)
	else:
		reportarMatch("["+str(analizadorLexico.nroLinea)+"] "+"Error de sintaxis, no se esperaba ",preanalisis,preanalisisAnterior,"match")
		
def reportar(tipoError,simbolo,metodo):
	global error
	global preanalisisAnterior
	global nroLinea

	err = "["+str(analizadorLexico.nroLinea)+"] "+tipoError+ " en la expresion "+ repr(preanalisis)+" despues de "+ preanalisisAnterior+"\n"
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
	#error=[]

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
			print("-------->TRAZA DE EJECUCION DE LA GRAMATICA:")
		programa()
		print("Fin de la ejecucion")
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
	
	        
if __name__ == '__main__':
	#Definicion de argumentos y pasaje de parametros.

	parser = argparse.ArgumentParser(description="Analizador Sintactico de Pascal Reducido")
	parser.add_argument("archivo", help="Ruta relativa del fichero a analizar sintacticamente.", type=str)
	parser.add_argument("-verbose_mode","-v", help="Flag para modo Verboso con impresiones de control.",action='store_true')
	parser.add_argument("-standalone","-s", help="Flag para funcionamiento por separado del aplicativo.",action='store_true')
	args = parser.parse_args()
	verbose= args.verbose_mode

	if(args.standalone):
		main()
	else:
		procesar()

	


# archivo = args.archivo
# archivo += ".tokens"
# #Procesamos el archivo linea por linea    
# numeroLinea=1
# with open(archivo) as f:
#     for line in f:
# 		linea = between(line,'[',',')
# 		linea = linea[1:-1]
# 		if(linea != ''):
# 			tokens.append(linea.lower())
# f.close()

# #Comenzamos a procesar los tokens encontrados sabiendo que un programa Pascal comienza con la sentencia program
# if(posicion < len(tokens)):
# 	preanalisis = tokens[posicion]
# 	if(verbose):
# 		print("-------->TRAZA DE EJECUCION DE LA GRAMATICA:")
# 	programa()
# 	print("Analisis Finalizado. Sin errores detectados")
# #Salida de Tokens
# if(args.verbose_mode):
#         print tokens
