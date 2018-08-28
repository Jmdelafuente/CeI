#!/usr/bin/env python
# coding=utf-8

import string
import random
import argparse
import os

from collections import deque

#Authors: Bonet Peinado Daiana, de la Fuente Juan M.
#Year: 2018
#License: GNU GPLv3. See LICENSE file for more information.


	
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
		'=': 'q25',
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
		'\t': 'q0',
		',': 'q27'
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
    tokens.append(["NUMERO",cadena,nroLinea])        
    cadena = ""
    return ret

def q4(x):
    ret = 1
	global state
    global cadena
        
    state = 'q0'
    cadena = ""
    tokens.append(["CORCHETE_A",x,nroLinea])        
    return ret

def q5(x):
    ret = 1
	global state
    global cadena
        
    state = 'q0'
    cadena = ""
    tokens.append(["CORCHETE_C",x,nroLinea])        
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
    tokens.append(["OPERADOR_RELACIONAL",cadena,nroLinea])        
    cadena = ""
    return ret

def q8(x):
    ret = 1
	global state
    global cadena
        
    state = 'q0'
    tokens.append(["OPERADOR_RELACIONAL",cadena,nroLinea])        
    cadena = ""
    return ret

def q9(x):
    ret = 1
    global cadena
    global state
    state = 'q0'
    tokens.append(["OPERADOR_RELACIONAL",cadena,nroLinea])        
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
    tokens.append(["OPERADOR_RELACIONAL",cadena,nroLinea])
    cadena =""
    state ='q0'
    return ret

def q12(x):
        global state
        global cadena
        
        ret = 1
        tokens.append(["OPERADOR_RELACIONAL",cadena,nroLinea])
        cadena = ""
        state = 'q0'
        return ret

def q13(x):
        global cadena
        global state
        
        ret = 1
        tokens.append(["PUNTO_COMA",cadena,nroLinea])
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
        if(cadena.upper() in operadoresLogicos):
                tokens.append([cadena.upper(),cadena,nroLinea])
        elif(cadena.upper() in palabrasReservadas):
                tokens.append([cadena.upper(),cadena,nroLinea])
        else:
        #        global tokens
                tokens.append(["IDENTIFICADOR",cadena,nroLinea])
        cadena =""
        state ='q0'
        return ret

def q16(x):
        global state
        global cadena
        
        ret = 1
        tokens.append(["OPERADOR_ARITMETICO",cadena,nroLinea])
        cadena =""
        state ='q0'
        return ret

def q17(x):
        global state
        global cadena
        
        ret = 1
        tokens.append(["OPERADOR_ARITMETICO",cadena,nroLinea])
        cadena =""
        state ='q0'
        return ret

def q18(x):
        global cadena
        global state
        
        ret = 1
        tokens.append(["OPERADOR_TERMINO",cadena,nroLinea])
        cadena = ""
        state = 'q0'
        return ret

def q19(x):
        global cadena
        global state
        
        ret = 1
        tokens.append(["OPERADOR_TERMINO",cadena,nroLinea])
        cadena = ""
        state = 'q0'
        return ret

def q20(x):
        global cadena
        global state
        
        ret = 1
        tokens.append(["PUNTO",cadena,nroLinea])
        cadena=""
        state = 'q0'
        return ret

def q21(x):
        global cadena
        global state
        
        ret = 1
        tokens.append(["PARENTESIS_A",cadena,nroLinea])
        cadena = ""
        state = 'q0'
        return ret


def q22(x):
        global cadena
        global state
        
        ret = 1
        tokens.append(["PARENTESIS_C",cadena,nroLinea])
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
        try:
                state= entrada[x]
        except KeyError:
                ret = 1
                state='q26'
        return ret

def q24(x):
        global cadena
        global state

        ret = 1
        tokens.append(["ASIGNACION",cadena,nroLinea])
        cadena = ""
        state = 'q0'
        return ret

def q25(x):
        global cadena
        global state

        ret = 1
        tokens.append(["OPERADOR_RELACIONAL",cadena,nroLinea])
        cadena = ""
        state = 'q0'
        return ret


def q26(x):
        ret = 1
	global state
        state = 'q0'
        global cadena
        cadena = cadena[:-1]
        tokens.append(["DOS_PUNTOS",cadena,nroLinea])        
        cadena = ""
        return ret

def q27(x):
        ret = 1
	global state
        state = 'q0'
        global cadena
        cadena = cadena[:-1]
        tokens.append(["COMA",cadena,nroLinea])        
        cadena = ""
        return ret




def process(line):
    i=0
    global nroLinea
    global cadena
    global error
    if(args.verbose_mode):
		print "Longitud de Linea: " + repr(len(line))
		  
    #Revision caracter a caracter de la linea
    while i < (len(line)):
		#Por normalizacion, se trabaja en minusculas
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

#Numero de Linea
global nroLinea

#Cadena procesado
global cadena
cadena=""

#Palabras reservadas
global palabrasReservadas
palabrasReservadas=["BEGIN","BOOLEAN","END","WHILE","TRUE","FALSE","IF","ELSE","PROGRAM","DO","THEN","FUNCTION","INTEGER","PROCEDURE","READ","VAR","WRITE"]
operadoresLogicos = ["AND","OR","NOT"]
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
    'q25': q25,
    'q26': q26,
	}

                        
def main():
	global nroLinea
	global tokens
	                    
	#Procesamos el archivo linea por linea    
	nroLinea=1
	with open(args.archivo) as f:
	    for line in f:
			tokens.append(process(line))
	                nroLinea += 1
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
	file.close()
	#Corroboramos la existencia de errores y los reportamos
	if(error):
	        print "ERRORES DETECTADOS EN ANALISIS LEXICO: "+ repr(len(error))
	        for e in error:
	                print e
	        os.system('kill %d' % os.getpid())
	else:
	        print "Analisis lexico finalizado. No hay errores detectados"

def analizarArchivo(archivo,verboso):
	#Procesamos el archivo linea por linea    
	global nroLinea
	global tokens
	
	
	nroLinea=1
	
	with open(archivo) as f:
	    for line in f:
			tokens.append(process(line))
	                nroLinea += 1
	f.close()
	
	
	tokens = [x for x in tokens if x is not None]
	#Corroboramos EOF y Comentario abierto
	if bandera:
		error.append("[EOF] Final de archivo inesperado: Comentario no finalizado") #hay que pensar si puede haber mas de un error como tratarlo quizas imprimir un error por linea y enumerarlos
	        
	#Salida de Tokens
	if(verboso):
	        print tokens
	
	#Corroboramos la existencia de errores y los reportamos
	#if(error):
	#        print "ERRORES DETECTADOS EN ANALISIS LEXICO: "+ repr(len(error))
	#        for e in error:
	#                print e
	#        os.system('kill %d' % os.getpid())
	#else:
	#        print "Analisis lexico finalizado. No hay errores detectados"
	
	
def siguientePreanalisis():
	global nroLinea
	
	if(len(tokens)):
		t = (tokens.pop(0))
		nroLinea = t[2]
		print "--------------->"+t[0]
		return t[0].lower()
	else:
		return "EOF"
		
if __name__ == '__main__':
	#Definicion de argumentos y pasaje de parametros.
	parser = argparse.ArgumentParser(description="Analizador Sintactico de Pascal Reducido")
	parser.add_argument("archivo", help="Ruta relativa del fichero a analizar sintacticamente.", type=str)
	parser.add_argument("-verbose_mode","-v", help="Flag para modo Verboso con impresiones de control.",action='store_true')
	parser.add_argument("-standalone","-s", help="Flag para funcionamiento por separado del aplicativo.",action='store_true')
	args = parser.parse_args()

	if(args.standalone):
		main()
	else:
		analizarArchivo(args.archivo,args.verbose_mode)
	

