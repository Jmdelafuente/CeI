import string
import random
#import sys
import argparse

#Argumentos y pasaje de parametros

parser = argparse.ArgumentParser(description="Analizador Sintactico de Pascal Reducido")
parser.add_argument("archivo", help="Ruta relativa del fichero a analizar sintacticamente.", type=str)
parser.add_argument("verbose_mode", help="True para modo Verboso con impresiones de control.",nargs='?', default=False, type=bool)
args = parser.parse_args()
#print args
#archivo = args[1]

	


#Procedimientos de los estados, definicion: ESTADO(letra) :- estado
def q0(x):
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
        global cadena
        cadena = cadena + x
	global state
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
                
	if(x in numeros):
		state = 'q2'
	else:
                #global state
                state = 'q3'
        global cadena
        cadena = cadena + x
        return ret
                
def q3(x):
        ret = 2
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
        #        global state
                state='q7'
                
        return ret

def q7(x):
        ret = 2
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
                state = 'q11'
                
        return ret

def q11(x):
        ret = 2
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
        cadena = cadena + x
	return ret

def q15(x):
        ret = 2
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
        cadena = cadena + x
        entrada={
                '=' : 'q24'
        }
        global state
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
        
	while i < (len(line)):
        
                x = line[i]
                x = x.upper()
                i +=1
                if(args.verbose_mode):
                        print "El estado es: " + state
		        print "X es: " + repr(x)
                try:
                        valor = estados[state](x)                   #Valor almacena cuantos caracteres hay que retroceder luego de llegar al estado
                        i = i - valor
                except KeyError:
                        error.append('['+repr(nroLinea)+']' " Token no reconocido " + cadena)
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
#print letras
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
#Definicion de estados
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

                        
                        
#Procesamos el archivo    
numeroLinea=1
with open(args.archivo) as f:
    for line in f:
		tokens.append(process(line,numeroLinea))
                numeroLinea += 1
f.close()

tokens = [x for x in tokens if x is not None]
if bandera:
	error.append("[EOF] Final de archivo inesperado: Comentario no finalizado") #hay que pensar si puede haber mas de un error como tratarlo quizas imprimir un error por linea y enumerarlos
if(args.verbose_mode):
        print tokens

with open(args.archivo+'.tokens', 'w') as file:
        for t in tokens:
                file.write(repr(t))
                file.write("\n")
if(error):
        print "ERRORES DETECTADOS: "+ repr(len(error))
        for e in error:
                print e


