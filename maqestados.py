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

def q0(x):
        global cadena
        global state
        ret = 0
        
	if(x in letras):
		ch = 'letra'
	elif(x in numeros):
		ch = 'numero'
	else:
		ch = x
		
	entrada={
		'{': 'q1',
	        'numero': 'q2',
	        ']': 'q5',
	        '[': 'q4',
	        '<': 'q6',
	        '>': 'q10',
	        ';': 'q13',
	        'letra': 'q14',
                '_': 'q14',
	        '+': 'q16',
	        '-': 'q17',
	        '*': 'q18',
	        '/': 'q19',
	        '.': 'q20',
	        '(': 'q21',
	        ')': 'q22',
	        ':': 'q23',
                '\n': 'q0',
                ' ':  'q0',
                '\t': 'q0'
	}
        
        cadena = cadena + x
	state = entrada[ch]

        if(state=='q0'):
		cadena=""
	return ret

def q1(x):
        ret = 0
        global bandera
        global state
		
	if(x=='}'):
		
		bandera = False
		state='q0' 
	else: 
		#global state
                state = 'q1'
		#global bandera
		bandera = True
        
        return ret
                 
def q2(x):
        ret = 0
        global state
        global cadena
        
	if(x in numeros):
		state = 'q2'
	else:
                ret = 1
                state = 'q3'
        cadena = cadena + x
        return ret
                
def q3(x):
        ret = 1
	global state
        global cadena
        
        state = 'q0'
        cadena = cadena[:-1]
        tokens.append(["NUMERO",cadena])        
        cadena = ""
        return ret

def q4(x):
        ret = 1
	global state
        global cadena
        
        state = 'q0'
        cadena = ""
        tokens.append(["CORCHETE_A",x])        
        return ret

def q5(x):
        ret = 1
	global state
        global cadena
        
        state = 'q0'
        cadena = ""
        tokens.append(["CORCHETE_C",x])        
        return ret

def q6(x):
        ret = 0
	global cadena
        global state
        
        cadena = cadena + x
        entrada={
                '=' : 'q8',
                '>' : 'q9'
        }
        try:
                state= entrada[x]
        except KeyError:
                ret = 1
                state='q7'
                
        return ret

def q7(x):
        ret = 1
	global state
        state = 'q0'
        global cadena
        cadena = cadena[:-1]
        tokens.append(["OPERADOR_RELACIONAL",cadena])        
        cadena = ""
        return ret

def q8(x):
        ret = 1
	global state
        global cadena
        
        state = 'q0'
        tokens.append(["OPERADOR_RELACIONAL",cadena])        
        cadena = ""
        return ret

def q9(x):
        ret = 1
        global cadena
        global state
        state = 'q0'
        tokens.append(["OPERADOR_RELACIONAL",cadena])        
        cadena = ""
        return ret

def q10(x):
        ret = 0
	global cadena
        global state
        
        cadena = cadena + x
        entrada={
                '=' : 'q12'
        }
        try:
                state = entrada[x]
        except KeyError:
                ret = 1
                state = 'q11'
                
        return ret

def q11(x):
        ret = 1
        global cadena
        global state
        
        cadena = cadena[:-1]
        tokens.append(["OPERADOR_RELACIONAL",cadena])
        cadena =""
        state ='q0'
        return ret

def q12(x):
        global state
        global cadena
        
        ret = 1
        tokens.append(["OPERADOR_RELACIONAL",cadena])
        cadena = ""
        state = 'q0'
        return ret

def q13(x):
        global cadena
        global state
        
        ret = 1
        tokens.append(["PUNTO_COMA",cadena])
        cadena = ""
        state = 'q0'
        return ret

def q14(x):
        ret = 0
        global cadena
        global state
        
        if(x in letras):
		char = 'letra'
	elif(x in numeros):
		char = 'numero'
	else:
		char = x
	
        entrada={
		'numero': 'q14',
	        'letra': 'q14',
	}
        try:

                state = entrada[char]
        except KeyError:
                state = 'q15'
                ret = 1
        cadena = cadena + x
	return ret

def q15(x):
        ret = 1
        global cadena
        global tokens
        global state

        cadena = cadena[:-1]
        if(cadena.upper() in palabrasReservadas):
                tokens.append([cadena.upper(),cadena])
        else:
        #        global tokens
                tokens.append(["IDENTIFICADOR",cadena])
        cadena =""
        state ='q0'
        return ret

def q16(x):
        global state
        global cadena
        
        ret = 1
        tokens.append(["OPERADOR_ARITMETICO",cadena])
        cadena =""
        state ='q0'
        return ret

def q17(x):
        global state
        global cadena
        
        ret = 1
        tokens.append(["OPERADOR_ARITMETICO",cadena])
        cadena =""
        state ='q0'
        return ret

def q18(x):
        global cadena
        global state
        
        ret = 1
        tokens.append(["OPERADOR_TERMINO",cadena])
        cadena = ""
        state = 'q0'
        return ret

def q19(x):
        global cadena
        global state
        
        ret = 1
        tokens.append(["OPERADOR_TERMINO",cadena])
        cadena = ""
        state = 'q0'
        return ret

def q20(x):
        global cadena
        global state
        
        ret = 1
        tokens.append(["PUNTO",cadena])
        cadena=""
        state = 'q0'
        return ret

def q21(x):
        global cadena
        global state
        
        ret = 1
        tokens.append(["PARENTESIS_A",cadena])
        cadena = ""
        state = 'q0'
        return ret


def q22(x):
        global cadena
        global state
        
        ret = 1
        tokens.append(["PARENTESIS_C",cadena])
        cadena = ""
        state = 'q0'
        return ret

def q23(x):
        ret = 0
        global cadena
        global state
        
        cadena = cadena + x
        entrada={
                '=' : 'q24'
        }
        state = entrada[x]
        return ret

def q24(x):
        global cadena
        global state

        ret = 1
        tokens.append(["ASIGNACION",cadena])
        cadena = ""
        state = 'q0'
        return ret

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
global verbose
verbose= False

#Bandera para control de comentario abierto
global bandera
bandera = False

#Lista de Tokens reconocidos
global tokens
tokens=[]

#Estado actual
global state
state='q0'

#Letras
global letras
letras =  list(string.ascii_uppercase)

#Numeros
global numeros
numeros = ['1','2','3','4','5','6','7','8','9','0']

#Error
global error
error=[]

#Cadena procesado
global cadena
cadena=""

#Palabras reservadas
global palabrasReservadas
palabrasReservadas=["BEGIN","BOOL","END","WHILE","TRUE","FALSE","IF","ELSE","PROGRAM","DO","THEN","AND","OR","FUNCTION","INTEGER","PROCEDURE","READ","VAR","WRITE"]

#Definicion de estados posibles
global estados
estados = {
	'q0': q0,
	'q1': q1,
	'q2': q2,
	'q3': q3,
	'q4': q4,
	'q5': q5,
	'q6': q6,
	'q7': q7,
	'q8': q8,
	'q9': q9,
	'q10': q10,
	'q11': q11,
	'q12': q12,
	'q13': q13,
	'q14': q14,
	'q15': q15,
	'q16': q16,
	'q17': q17,
	'q18': q18,
	'q19': q19,
	'q20': q20,
	'q21': q21,
	'q22': q22,
        'q23': q23,
        'q24': q24,
        
	}

                        
                        
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

