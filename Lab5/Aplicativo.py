#!/usr/bin/env python

import string
import random
#import sys
import argparse

#Authors: Bonet Peinado Daiana, de la Fuente Juan M.
#Year: 2018
#License: GNU GPLv3. See LICENSE file for more information.

#Definicion de argumentos y pasaje de parametros.

parser = argparse.ArgumentParser(description="Analizador Sintactico de Pascal Reducido")
parser.add_argument("archivo", help="Ruta relativa del fichero a analizar sintacticamente.", type=str)
parser.add_argument("verbose_mode", help="True para modo Verboso con impresiones de control.",nargs='?', default=False, type=bool)
args = parser.parse_args()

	


#Procedimientos de los estados, definicion: ESTADO(letra) -> estado [retroceso] [token]
#El funcionamiento de cada estado es sencillo, para una entrada revisa que transicion corresponde, actualiza el estado de acuerdo a la transicion, acumula la cadena procesada agregando la entrada y si corresponde agrega el token a la lista. Asimismo puede retornar un entero para avisar cuantos caracteres corresponde retroceder en el analisis de acuerdo a lo especificado en la maquina de estados del informe

def letra():
        global preanalisis
        global state
        ret = 0
        
		
			
	
	
def integer():


def process(line,nroLinea):
        i=0
        
        global cadena
        global error

        if(args.verbose_mode):
                print "Longitud de Linea: " + repr(len(line))
        
        #Revision caracter a caracter de la linea
	while i < (len(line)):
                #Por normalizacion, se trabaja en mayusculas
                x = line[i]
                x = x.upper()
                i +=1

                #Salida de programador activada?
                if(args.verbose_mode):
                        print "El estado es: " + state
		        print "X es: " + repr(x)
                        print "Caracter numero: " + repr(i)
                        
                #Llamada a la maquina de estados con estado 'state' y entrada 'x'
                try:
                        valor = estados[state](x)                   #Valor almacena cuantos caracteres hay que retroceder luego de llegar al estado
                        i = i - valor

                #No existe transicion para ese estado y ese caracter
                except KeyError:
                        error.append('['+repr(nroLinea)+']' " Caracter(es) no reconocido(s) " + cadena)
                        cadena = ""
                


##Variables globales

#Bandera de modo verboso
#global verbose
#verbose= False


#Letra
global letra
letra =  list(string.ascii_uppercase)

#Numeros
global numeros
digito = ['1','2','3','4','5','6','7','8','9','0']

#Preanalisis procesado
global preanalisis
preanalisis=""


#Error
global error
error=[]



#Palabras reservadas
global palabrasReservadas
palabrasReservadas=["BEGIN","BOOL","END","WHILE","TRUE","FALSE","IF","ELSE","PROGRAM","DO","THEN","AND","OR","FUNCTION","INTEGER","PROCEDURE","READ","VAR","WRITE"]

#Definicion de casos posibles
global casos
casos = {
	'q0': q0,
	
	}

def letra():
	if(preanalisis in letras):
		match(preanalisis)
	else:
		reportar("Error de Sintaxis",preanalisis,"letra")

def digitos()
	if(preanalisis in numeros):
		match(preanalisis)
	else:
		reportar("Error de Sintaxis",preanalisis,"digito")

def digitosRep()
	if(preanalisis in numeros):
		digito()
	else:
		reportar("Error de Sintaxis",preanalisis,"digitosRep")

def digitosRep1()
	if(preanalisis in numeros):
		digitosRep()

def identificador():
	if(preanalisis in letras):
		letra()
		identificadorRep()
	else:
		reportar("Error de Sintaxis",preanalisis,"identificador")
                    
def identificadorRep():
	if(preanalisis in letras):
		letra()
		identificadorRep()
	if(preanalisis in numeros):
		digitos()
		identificadorRep()

def declaracionVariables():
	if(preanalisis == "var"):
		match("var")
		listaVariables()
		match(;)
	else:
		reportar("Error de Sintaxis",preanalisis,"declaracionVariables")


def listaVariables():
	if(preanalisis == ";"):
		listaIdentificador()
		match(":")
		tipoVariable()
	else:
		reportar("Error de Sintaxis",preanalisis,"listaVariables")


def listaIdentificador():
	if(preanalisis in letras):
		identificador()
		listaIdentificadorRep()
	else:
		reportar("Error de Sintaxis",preanalisis,"listaIdentificador")

def listaIdentificadorRep():
	if( preanalisis == ","): 
		match(,)
		identificador()
		listaIdentificadorRep()

def tipoVariables():
	if( preanalisis == "integer"):
		match("integer")
	elif( preanalisis == "boolean"):
		match("boolean")
	else:
		reportar("Error de Sintaxis",preanalisis,"tipoVariables")

def sentenciaCompuesta():
	case2 = {'write(','while','read(','if'}
    if ( preanalisis == "begin") :
        match(begin)
        sentenciaCompuestaRep()
        fin()
    elif ((preanalisis in letras) or (preanalisis in case2)) :
        sentencia()
        match(;)
    else:
		reportar("Error de Sintaxis",preanalisis,"sentenciaCompuesta")


def sentenciaCompuestaRep():
	case2 = {'write(','while','read(','if'}
    if ((preanalisis in letras) or (preanalisis in case2)) :
        compuesta()
        sentenciaCompuestaRep()
        
def compuesta():
	case1 = {'begin','write(','while','read(','if'}
    if ((preanalisis in letras) or (preanalisis in case1)) :
        sentenciaCompuesta()
        compuesta()
    else:
		reportar("Error de Sintaxis",preanalisis,"compuesta")

def fin():
	case2 = {'write(','while','read(','if'}
	if (preanalisis == 'end;'):
		match('end;')
	elif (preanalisis in case2 ):
		sentencia()
		match('end;')
	else:
		reportar("Error de Sintaxis",preanalisis,"fin")


def sentencia():
	if(preanalisis == "if"):
		ifthen()
	elif(preanalisis == 'while'):
		mientras9)
	elif(preanalisis == 'write('):
		match("write(")
		llamada2()
	elif(preanalisis == 'read('):
		match("read(")
		identificador()
	elif(preanalisis in letras):
		identificador()
		asignacionollamada()
	else:
		reportar("Error de Sintaxis",preanalisis,"sentencia")

def asignacion():
	if(preanalisis in letras):
		identificador()
		match(":=")
		expresionGeneral()
		match(";")
	else:
		reportar("Error de Sintaxis",preanalisis,"asignacion")
		


#Procesamos el archivo linea por linea    
numeroLinea=1
with open(args.archivo) as f:
    for line in f:
		tokens.append(process(line,numeroLinea))
                numeroLinea += 1
f.close()

tokens = [x for x in tokens if x is not None]
#Corroboramos EOF y Comentario abierto
if bandera:
	error.append("[EOF] Final de archivo inesperado: Comentario no finalizado") #hay que pensar si puede haber mas de un error como tratarlo quizas imprimir un error por linea y enumerarlos
        
#Salida de Tokens
if(args.verbose_mode):
        print tokens

#Guardando archivo .tokens
with open(args.archivo+'.tokens', 'w') as file:
        for t in tokens:
                file.write(repr(t))
                file.write("\n")
                
#Corroboramos la existencia de errores y los reportamos
if(error):
        print "ERRORES DETECTADOS: "+ repr(len(error))
        for e in error:
                print e
else:
        print "Analisis Finalizado. No hay errores detectados"

