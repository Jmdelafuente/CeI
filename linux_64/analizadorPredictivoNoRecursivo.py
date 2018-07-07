#!/usr/bin/env python
# coding=utf-8

import string
import random
import argparse
import re

#Authors: Bonet Peinado Daiana, de la Fuente Juan M.
#Year: 2018
#License: GNU GPLv3. See LICENSE file for more information.

#Definicion de argumentos y pasaje de parametros.

parser = argparse.ArgumentParser(description="Analizador Sintactico Predictivo de Pascal Reducido")
parser.add_argument("archivo", help="Ruta relativa del fichero de tokens a analizar sintacticamente.", type=str)
parser.add_argument("verbose_mode", help="True para modo Verboso con impresiones de control.",nargs='?', default=False, type=bool)
args = parser.parse_args()

	

##Variables globales

#Bandera de modo verboso
global verbose
verbose= args.verbose_mode


#Letra
global letras
letras =  list(string.ascii_uppercase)

#Numeros
global digito
digito = ['1','2','3','4','5','6','7','8','9','0']

#Preanalisis procesado
global preanalisis
preanalisis=""

#Posicion del token analizado
global posicion
posicion=0

#Error
global error
error=[]

#Tokens
global tokens
tokens=[]


#Palabras reservadas
global palabrasReservadas
palabrasReservadas=["begin","bool","end","while","true","false","if","else","program","do","then","and","or","function","integer","procedure","read","var","write"]


#Definicion de casos posibles
def letra():
	if(verbose):
		print("letra")
	if((re.search(r"[a-z]",preanalisis)) and (preanalisis not in palabrasReservadas)):
		match(preanalisis)
	else:
		reportar("Error de Sintaxis: se esperaba una letra",preanalisis,"letra")

def digitos():
	if(verbose):
		print("digitos")
	if(re.search(r"[0-9]",preanalisis)):
		digito()
		digitosRep()
	elif (preanalisis == "-"):
		match("-")
		digito()
		digitosRep()
	else:
		reportar("Error de Sintaxis: se esperaba un digito o - ",preanalisis,"digitos")

def digito():
	if(verbose):
		print("digito")
	if(re.search(r"[0-9]",preanalisis)):
		match(preanalisis)
	else:
		reportar("Error de Sintaxis: se esperaba un digito",preanalisis,"digito")


def digitosRep():
	if(verbose):
		print("digitosRep")
	if(re.search(r"[0-9]",preanalisis)):
		digito()
		digitosRep()
	
def identificador():
	if(verbose):
		print("identificador")
	global preanalisis
	if((re.search(r"[a-z]",preanalisis)) and (preanalisis not in palabrasReservadas)):
		preanalisis = preanalisis[1:]
		identificadorRep()
	else:
		reportar("Error de Sintaxis: se esperaba un identificador valido",preanalisis,"identificador")
                    
def identificadorRep():
	if(verbose):
		print("identificadorRep")
	global preanalisis
	global tokens
	global posicion
	if(re.search(r"[a-z]",preanalisis)):
		preanalisis = preanalisis[1:]
		identificadorRep()
	elif(re.search(r"[0-9]",preanalisis)):
		preanalisis = preanalisis[1:]
		identificadorRep()
	elif(preanalisis==''):
		posicion += 1
		preanalisis = tokens[posicion]
		

def declaracionVariables():
	if(verbose):
		print("declaracionVariables")
	if(preanalisis == 'var'):
		match('var')
		listaVariables()
		match(';')
	else:
		reportar("Error de Sintaxis: se esperaba VAR",preanalisis,"declaracionVariables")


def listaVariables():
	if(verbose):
		print("listaVariable")
	global letras
	if((re.search(r"[a-z]",preanalisis)) and (preanalisis not in palabrasReservadas)):
		listaIdentificador()
		match(":")
		tipoVariables()
	else:
		reportar("Error de Sintaxis: se esperaba un identificador valido",preanalisis,"listaVariables")


def listaIdentificador():
	if(verbose):
		print("listaIdentificador")
	if((re.search(r"[a-z]",preanalisis)) and (preanalisis not in palabrasReservadas)):
		identificador()
		listaIdentificadorRep()
	else:
		reportar("Error de Sintaxis: se esperaba un identificador valido",preanalisis,"listaIdentificador")

def listaIdentificadorRep():
	if(verbose):
		print("listaIdentificadorRep")
	if( preanalisis == ","): 
		match(",")
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
		match(";")
	else:
		reportar("Error de Sintaxis: se esperaba BEGIN",preanalisis,"sentenciaCompuesta")

def compuesta():
	if(verbose):
		print("compuesta")
	case1 = {'write','while','read','if'}
	if (((re.search(r"[a-z]",preanalisis)) and (preanalisis not in palabrasReservadas)) or (preanalisis in case1)) :
		sentencia()
		sentenciaOptativa()
	elif (preanalisis == "begin"):
		sentenciaCompuesta()
	else:
		reportar("Error de Sintaxis: se esperaba un identificador valido o BEGIN",preanalisis,"compuesta")

def sentenciaOptativa():
	if(verbose):
		print("sentenciaOptativa")
	if(preanalisis == ";"):
		match(";")
		sentenciaOptativa2()

def sentenciaOptativa2():
	if(verbose):
		print("sentenciaOptativa2")
	case1 = {"begin",'write','while','read','if'}
	if (((re.search(r"[a-z]",preanalisis)) and (preanalisis not in palabrasReservadas)) or (preanalisis in case1)) :
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
		match("(")
		llamada2()
	elif(preanalisis == "read"):
		match("read")
		match("(")
		identificador()
	elif((re.search(r"[a-z]",preanalisis)) and (preanalisis not in palabrasReservadas)):
		identificador()
		asignacionollamada()
	else:
		reportar("Error de Sintaxis: se esperaba READ, WRITE, IF, WHILE o Identificador Valido",preanalisis,"sentencia")

def asignacion():
	if(verbose):
		print("asignacion")
	if((re.search(r"[a-z]",preanalisis)) and (preanalisis not in palabrasReservadas)):
		identificador()
		match(":=")
		expresionGeneral()
	else:
		reportar("Error de Sintaxis: se esperaba un identificador valido",preanalisis,"asignacion")


def asignacionollamada():
	if(verbose):
		print("asignacionollamada")
	if (preanalisis == ":="):
		match(":=")
		expresionGeneral()
	elif (preanalisis == "("):
		match("(")
		llamada1()
	else:
		reportar("Error de sintaxis: se esperaba := o (",preanalisis,"asignacionollamada")


def expresionAritmetica():
	if(verbose):
		print("expresionAritmetica")
	case1 = {"write","true","false","read","-"}
	if (((re.search(r"[a-z]",preanalisis)) and (preanalisis not in palabrasReservadas)) or (re.search(r"[0-9]",preanalisis)) or (preanalisis in case1)) :
		termino() 
		expresionAritmetica1()
	else:
		reportar("Error de sintaxis: se esperaba READ, WRITE, TRUE, FALSE, Identificador valido o digitos",preanalisis,"expresionAritmetica1")
        
def expresionAritmetica1():
	if(verbose):
		print("expresionAritmetica1")
	if ( preanalisis == "+"):
	  match("+")
	  termino()
	  expresionAritmetica1()
	elif( preanalisis == "-"):
	  match("-")
	  termino()
	  expresionAritmetica1()

def termino():
	if(verbose):
		print("termino")
	case1 = {"write","true","false","read","-"}
	if(((re.search(r"[a-z]",preanalisis)) and (preanalisis not in palabrasReservadas)) or (re.search(r"[0-9]",preanalisis)) or (preanalisis in case1)) :
			factor()
			termino1()
	else:
			reportar("Error de Sintaxis: se esperaba WRITE,READ,TRUE,FALSE,Identificador valido o Digitos",preanalisis,"expresionAritmetica1")

def termino1():
	if(verbose):
		print("termino1")
	if (preanalisis == "*") :
				match("*")
				factor()
				termino1()
	elif (preanalisis == "/") :
				match("/")
				factor()
				termino1()


def factor():
	if(verbose):
		print("factor")
	if ((re.search(r"[a-z]",preanalisis)) and (preanalisis not in palabrasReservadas)) :
				identificador()
				factor1()
	elif (preanalisis == "write") :
				match("write")
				match("(")
				llamada2()
	elif (preanalisis == "read") :
				match("read")
				match("(")
				identificador()
				match(")")
	elif (re.search(r"[0-9]",preanalisis) or preanalisis == '-') :
				digitos()
	elif (preanalisis == "true") :
				match("true")
	elif (preanalisis == "false") :
				match("false")
	else:
				reportar("Error de sintaxis: se esperaba WRITE,READ,TRUE,FALSE,DIGITO o Identificador valido",preanalisis,"factor")

def factor1():
	if(verbose):
		print("factor1")
	if ( preanalisis == "(") :
		match("(")
		llamada1()

def operadorRelacional():
	if(verbose):
		print("operadorRelacional")
	if ( preanalisis == "="):
				match("=")
	elif (preanalisis == "<>") :
				match("<>")
	elif (preanalisis == "<") :
				match("<")
	elif (preanalisis == "<=") :
				match("<=")
	elif (preanalisis == ">") :
				match(">")
	elif (preanalisis == ">=") :
				match(">=")
	else:
				reportar("Error de sintaxis: se esperaba un operador relacional <,<=,=>,>,<> o =",preanalisis,"operadorRelacional")
				
def programa():
	if(verbose):
		print("programa")
	if ( preanalisis == "program") :
			 match("program")
			 identificador()
			 declaracionVariableOpt()
			 programaRepPyf()
			 match("begin")
			 programaRepSentencia()
			 match("end")
			 match(".")
	else:
			 reportar("Error de sintaxis: debe comenzar con la sentencia PROGRAM Identificador",preanalisis,"programa")


def declaracionVariableOpt():
	if(verbose):
		print("declaracionVariablesOpt")
	if ( preanalisis == "var") :
			 declaracionVariables()

def programaRepPyf():
	if(verbose):
		print("programaRepPyf")
	if (( preanalisis == "function") or (preanalisis == "procedure")) :
			 declaracionPyf()
			 programaRepPyf()
	

def programaRepSentencia():
	if(verbose):
		print("programaRepSentencia")
	global letras
	caso1={"begin", "read", "write","while","if"}
	if ( (preanalisis in caso1) or ((re.search(r"[a-z]",preanalisis)) and (preanalisis not in palabrasReservadas))) :
			 compuesta()
			 programaRepSentencia()
	
def expresionGeneral():
	if(verbose):
		print("expresionGeneral")
	caso1={'false', 'true', '(', '-', 'write', 'read', 'not'}
	if(((re.search(r"[a-z]",preanalisis)) and (preanalisis not in palabrasReservadas)) or (re.search(r"[0-9]",preanalisis)) or preanalisis in caso1):
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
	caso2={'false', 'true', '-', 'write', 'read'}
	if(preanalisis == "not" or preanalisis== "("):
		no()
		match("(")
		expresionGeneral()
		match(")")
		compararAnd1()
	elif (((re.search(r"[a-z]",preanalisis)) and (preanalisis not in palabrasReservadas)) or re.search(r"[0-9]",preanalisis) or preanalisis in caso2):
		expresionAritmetica() 
		expresionAritmetica2() 
	else:
		reportar("Error de sintaxis: se esperaba WRITE,READ,TRUE,FALSE,NOT,(,-,Digito o Identificador valido",preanalisis,"expresionGeneral")

def expresionAritmetica2():
	if(verbose):
		print("expresionAritmetica2")
	caso1={'<', '<=', '=', '>', '>=', '<>'}
	if(preanalisis  in caso1 ):
		operadorRelacional()
		expresionAritmetica()
		compararAnd1()

def compararAnd1():
	if(verbose):
		print("compararAnd1")
	if(preanalisis == "and"):
		match("and")
		compararAnd()


def ifthen():
	if(verbose):
		print("ifthen")
	if ( preanalisis == "if") :
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
	if ( preanalisis == "begin") :
			 match("begin")
			 compuesta()
			 match("end")
			 alternativa()
	elif ((preanalisis in caso2) or ((re.search(r"[a-z]",preanalisis)) and (preanalisis not in palabrasReservadas))):
			 sentencia()
			 match(";")
	else: 
			 reportar("Error de sintaxis: se esperaba WRITE,READ,WHILE,IF,BEGIN o Identificador valido",preanalisis,"ifthen1")

def alternativa():
	if(verbose):
		print("alternativa")
	global letras
	if  (preanalisis == ";"):
			 match(";")
	elif (preanalisis == "else"):
			 match("else")
			 compuesta()
	else:
			 reportar("Error de sintaxis: se esperaba ; o ELSE",preanalisis,"alternativa")
 
def mientras():
	if(verbose):
		print("mientras")
	if ( preanalisis == "while") :
			 match("while")
			 expresionGeneral()
			 match("do")
			 sentenciaCompuesta()
	else:
			 reportar("Error de sintaxis: se esperaba WHILE",preanalisis,"mientras")

def declaracionPyf():
	if(verbose):
		print("declaracionPyf")
	if ( preanalisis == "procedure") :
			 match("procedure")
			 identificador()
			 match("(")
			 parametrosRep()
			 match(")")
			 match(";")
			 declaracionVariableOpt()
			 declaracionPyfRep()
			 sentenciaCompuesta()
	elif ( preanalisis == "function") :
			 match("function")
			 identificador()
			 match("(")
			 parametrosRep()
			 match(")")
			 match(":")
			 tipoVariables()
			 match(";")
			 declaracionVariableOpt()
			 declaracionPyfRep()
			 sentenciaCompuesta()
	else:
			 reportar("Error de sintaxis: se esperaba PROCEDURE o FUNCTION",preanalisis,"declaracionPyf")

def parametrosRep():
	if(verbose):
		print("parametrosRep")
	if ( (re.search(r"[a-z]",preanalisis)) and (preanalisis not in palabrasReservadas)) :
		listaVariables()
		parametrosFormalesRep()	 


def declaracionVariablesRep():
	if(verbose):
		print("declaracionVariablesRep")
	if ( preanalisis == "var") :
			 declaracionVariables()

def declaracionPyfRep():
	if(verbose):
		print("declaracionPyfRep")
	if ( preanalisis == "function" or preanalisis == "procedure") :
			 declaracionPyf()
			 declaracionPyfRep()
	
	
def parametrosFormalesRep():
	if(verbose):
		print("parametrosFormalesRep")
	if ( preanalisis == ",") :
			 match(",")
			 listaVariables()
			 parametrosFormalesRep()

def parametrosReales():
	if(verbose):
		print("parametrosReales")
	caso1={'false', 'true', '(', '-', 'write', 'read', 'not'}
	if(((re.search(r"[a-z]",preanalisis)) and (preanalisis not in palabrasReservadas)) or (re.search(r"[0-9]",preanalisis)) or preanalisis in caso1):
			 expresionGeneral()
			 parametrosRealesRep()

def parametrosRealesRep():
	if(verbose):
		print("parametrosRealesRep")
	if ( preanalisis == ",") :
			 match(",")
			 expresionGeneral()
			 parametrosRealesRep()

def llamadaProcedimiento():
	if(verbose):
		print("llamadaProcedimiento")
	global letras
	if ( preanalisis == "write") :
			 match("write")
			 match("(")
			 llamada2()
			 #parametrosRealesRep()
	elif ( preanalisis == "read") :
			 match("read")
			 match("(")
			 identificador()
			 match(")")
	elif ( (re.search(r"[a-z]",preanalisis)) and (preanalisis not in palabrasReservadas)):
			 identificador()
			 match("(")
			 llamada1()
	else:
			 reportar("Error de sintaxis: se esparaba llamada a Procedimiento o Funcion",preanalisis,"llamadaProcedimiento")

def llamada1():
	if(verbose):
		print("llamada1")
	global letras
	caso2={'false', 'true', '(', '-', 'write', 'read', 'not'}
	if ( preanalisis == ")") :
			 match(")")
	elif(((re.search(r"[a-z]",preanalisis)) and (preanalisis not in palabrasReservadas)) or (re.search(r"[0-9]",preanalisis)) or preanalisis in caso2):
			 parametrosReales()
			 parametrosReales2()
			 match(")")
	else:
			 reportar("Error de sintaxis: se esperaba WRITE,READ,NOT,TRUE,FALSE,(,-,Digito o Identificador Valido",preanalisis,"llamada1")

def llamada2():
	if(verbose):
		print("llamada2")
	global letras
	if ( (re.search(r"[a-z]",preanalisis)) and (preanalisis not in palabrasReservadas)) :
			 identificador()
			 match(")")
	elif ( re.search(r"[0-9]",preanalisis) or preanalisis == "-") :
			 digitos()
			 match(")")
	else:
			 reportar("Error de sintaxis: se esperaba Digitos o un Identificador Valido",preanalisis,"llamada2")


def parametrosReales2():
	if(verbose):
		print("parametrosReales2")
	if ( preanalisis == ",") :
			 match(",")
			 parametrosReales()
			 parametrosReales2()

#Procedimiento Match dado en la teoría
def match(t):
	global tokens
	global posicion
	global preanalisis
	
	if(preanalisis == t):
		posicion += 1
		if(posicion < len(tokens)):
			preanalisis = tokens[posicion]
	else:
		reportarMatch("Error de sintaxis, no se esperaba ",preanalisis,tokens[posicion-1],"match")
		
def reportar(tipoError,simbolo,metodo):
	print "ERROR DETECTADO: "+ tipoError+ " en la expresion "+ repr(preanalisis)+" despues de "+ tokens[posicion-1] +"\n"
	exit(0)

def reportarMatch(tipoError,simbolo,simboloanterior,metodo):
	print "ERROR DETECTADO: "+ tipoError+ " "+ repr(preanalisis) +" despues de "+ repr(simboloanterior)+"\n"
	exit(0)

	
	
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


archivo = args.archivo
archivo += ".tokens"
#Procesamos el archivo linea por linea    
numeroLinea=1
with open(archivo) as f:
    for line in f:
		linea = between(line,' ','\n')
		linea = linea[1:-2]
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
