import string
import random
import sys

#Argumentos
archivo = sys.argv[1]


#Procedimientos de los estados
def q0(x):
        ret = 0
	if(x in letras):
		ch = 'letra'
	elif(x in numeros):
		ch = 'numero'
	else:
		ch = x
		
	entrada={
		' ': 'q0',
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
                ' ':  'q0'
	}
        global cadena
        cadena = cadena + x
	global state
	state = entrada[ch]
	return ret

def q1(x):
        ret = 0
	if(x=='}'):
		global state
		state='q0' 
	else: 
		global state
                state = 'q1'
        
        return ret
                 
def q2(x):
        ret = 0
	if(x in numeros):
		global state
                state = 'q2'
	else:
                global state
                state = 'q3'
        global cadena
        cadena = cadena + x
        return ret
                
def q3(x):
        ret = 1
	global state
        state = 'q0'
        global cadena
        cadena = cadena + x
        tokens.add(["NUMERO",cadena])        
        global cadena
        cadena = ""
        return ret

def q4(x):
        ret = 0
	global state
        state = 'q0'
        global cadena
        cadena = ""
        tokens.append(["CORCHETE_A",x])        
        return ret

def q5(x):
        ret = 0
	global state
        state = 'q0'
        global cadena
        cadena = ""
        tokens.append(["CORCHETE_C",x])        
        return ret

def q6(x):
        ret = 0
	global cadena
        cadena = cadena + x
        entrada={
                '=' : 'q8',
                '>' : 'q9'
        }
        try:
                global state
                state= entrada[x]
        except KeyError:
                global state
                state='q7'
                
        return ret

def q7(x):
        ret = 1
	global state
        state = 'q0'
        global cadena
        cadena = cadena[:-1]
        tokens.append(["OPERADOR_RELACIONAL",cadena])        
        global cadena
        cadena = ""
        return ret

def q8(x):
        ret = 0
	global state
        state = 'q0'
        tokens.append(["OPERADOR_RELACIONAL",cadena])        
        global cadena
        cadena = ""
        return ret

def q9(x):
        ret = 0
	global state
        state = 'q0'
        tokens.append(["OPERADOR_RELACIONAL",cadena])        
        global cadena
        cadena = ""
        return ret

def q10(x):
        ret = 0
	global cadena
        cadena = cadena + x
        entrada={
                '=' : 'q12'
        }
        try:
                global state
                state = entrada[x]
        except KeyError:
                global state
                state = 'q11'
                
        return ret

def q11(x):
        ret = 1
        global cadena
        cadena = cadena[:-1]
        tokens.append(["OPERADOR_RELACIONAL",cadena])
        global cadena
        cadena =""
        global state
        state ='q0'
        return ret

def q12(x):
        ret = 0
        tokens.append(["OPERADOR_RELACIONAL",cadena])
        global cadena
        cadena = ""
        global state
        state = 'q0'
        return ret

def q13(x):
        ret = 0
        tokens.append(["PUNTO_COMA",cadena])
        global cadena
        cadena = ""
        global state
        state = 'q0'
        return ret

def q14(x):
        ret = 0
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
                global state
                state = entrada[char]
        except KeyError:
                global state
                state = 'q15'
        global cadena
        cadena = cadena + x
	return ret

def q15(x):
        ret = 1
        global cadena
        cadena = cadena[:-1]
        if(cadena.upper in palabrasReservadas):
                global tokens
                tokens.append([cadena.upper(),cadena])
        else:
                global tokens
                tokens.append(["IDENTIFICADOR",cadena])
        global cadena
        cadena =""
        global state
        state ='q0'
        return ret

def q16(x):
        ret = 0
        tokens.append(["OPERADOR_ARITMETICO",cadena])
        global cadena
        cadena =""
        global state
        state ='q0'
        return ret

def q17(x):
        ret = 0
        tokens.append(["OPERADOR_ARITMETICO",cadena])
        global cadena
        cadena =""
        global state
        state ='q0'
        return ret

def q18(x):
        ret = 0
        tokens.append(["OPERADOR_TERMINO",cadena])
        global cadena
        cadena = ""
        global state
        state = 'q0'
        return ret

def q19(x):
        ret = 0
        tokens.append(["OPERADOR_TERMINO",cadena])
        global cadena
        cadena = ""
        global state
        state = 'q0'
        return ret

def q20(x):
        ret = 0
        tokens.append(["PUNTO",cadena])
        global cadena
        cadena=""
        global state
        state = 'q0'
        return ret

def q21(x):
        ret = 0
        tokens.append(["PARENTESIS_A",cadena])
        global cadena
        cadena = ""
        global state
        state = 'q0'
        return ret


def q22(x):
        ret = 0
        tokens.append(["PARENTESIS_C",cadena])
        global cadena
        cadena = ""
        global state
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
        ret = 0
        tokens.append["ASIGNACION",cadena]
        global cadena
        cadena = ""
        global state
        state = 'q0'
        return ret

def process(line):
	for i in xrange(len(line)):
	        x = line[i]
                x=x.upper()
		print "El estado es: " + state
		print "X es: " + repr(x)
                try:
                        valor = estados[state](x)                   #Valor almacena cuantos caracteres hay que retroceder luego de llegar al estado
                        i = i - valor
                except KeyError:
                        print "Token no reconocido " + cadena
                        global cadena
                        cadena = ""


##Variables globales

#Lista de Tokens reconocidos
tokens=[]
#Estado actual
state='q0'
#Letras
letras =  list(string.ascii_uppercase)
#Numeros
numeros = xrange(0,9)
#Error
error=""
#Cadena procesado
cadena=""
#Palabras reservadas
palabrasReservadas=["BEGIN","BEGIN.","END","WHILE","TRUE","FALSE","IF","ELSE","PROGRAM","DO","THEN","AND","OR","FUNCTION","INTEGER","PROCEDURE","READ","VAR","WRITE"]
#Definicion de estados
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
	
 
print letras
global tokens
tokens.append("PRUEBA")
#Procesamos el archivo    
with open(archivo) as f:
    for line in f:
		tokens.append(process(line))

f.close()
print tokens
    
#letras = cadena.ascii_lowercase
#letras = cadenay.join(map(chr, range(97, 123)),'\',\'') #or list(map(chr, range(ord('a'), ord('z')+1)))

#print "Que hermoso switch que hice en Python"


    
