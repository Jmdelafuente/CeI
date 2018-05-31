import string
import random
import sys

#Argumentos
archivo = sys.argv[1]


##Variables globales

#Lista de Tokens reconocidos
tokens=[]
#Estado actual
state='q0'
#Letras
letras =  (string.join(map(chr, range(97, 123)),'\',\'')) + '_'
#Numeros
numeros = xrange(0,9)
#Error
error=""
#String procesado
string=""
#Palabras reservadas
palabrasReservadas=["BEGIN","END","WHILE","TRUE","FALSE","IF","ELSE","PROGRAM","DO","THEN","AND","OR","FUNCTION","INTEGER","PROCEDURE","READ","VAR","WRITE"]

	
def q0(x):
	if(x in letras):
		char = letra
	elif(x in numeros):
		char = numero
	else:
		char = x
		
	entrada={
		' ': q0,
		'{': q1,
	        'numero': q2,
	        ']': q5,
	        '[': q4,
	        '<': q6,
	        '>': q10,
	        ';': q13,
	        'letra': q14,
	        '+': q16,
	        '-': q17,
	        '*': q18,
	        '/': q19,
	        '.': q20,
	        '(': q21,
	        ')': q22,
	        ':': q23,
	}
        global string
        string = string + x
	global state
	state = entrada[char]
	
def q1(x): 
	if(x=='}'):
		global state
		state='q0' 
	else: 
		global state
                state = q1
        
        return 0
                 
def q2(x): 
	if(x in numeros):
		global state
                state = q2
	else:
                global state
                state = q3
        global string
        string = string + x
        return 0
                
def q3(x): 
	global state
        state = q0
        global string
        string = string + x
        tokens.add(["NUMERO",string])        
        global string
        string = ""
        return 1

def q4(x): 
	global state
        state = 'q0'
        global string
        string = ""
        tokens.append(["CORCHETE_A",x])        
        return 0

def q5(x): 
	global state
        state = 'q0'
        global string
        string = ""
        tokens.append(["CORCHETE_C",x])        
        return 0

def q6(x): 
	global string
        string = string + x
        entrada={
                '=' : q8,
                '>' : q9
        }
        try:
                global state
                state= entrada[x]
        except KeyError:
                global state
                state=q7
                
        return 0

def q7(x): 
	global state
        state = 'q0'
        global string
        string = string[:-1]
        tokens.append(["OPERADOR_RELACIONAL",string])        
        global string
        string = ""
        return 1

def q8(x): 
	global state
        state = 'q0'
        tokens.append(["OPERADOR_RELACIONAL",string])        
        global string
        string = ""
        return 0

def q9(x): 
	global state
        state = 'q0'
        tokens.append(["OPERADOR_RELACIONAL",string])        
        global string
        string = ""
        return 0

def q10(x): 
	global string
        string = string + x
        entrada={
                '=' : q12
        }
        try:
                global state
                state = entrada[x]
        except KeyError:
                global state
                state = q11
                
        return 0

def q11(x):
        global string
        string = string[:-1]
        tokens.append["OPERADOR_RELACIONAL",string]
        global string
        string =""
        global state
        state ='q0'
        return 1

def q12(x):
        tokens.append["OPERADOR_RELACIONAL",string]
        global string
        string = ""
        global state
        state = 'q0'
        return 0

def q13(x):
        tokens.append["PUNTO_COMA",string]
        global string
        string = ""
        global state
        state = 'q0'
        return 0

def q14(x):
        if(x in letras):
		char = letra
	elif(x in numeros):
		char = numero
	else:
		char = x
	
        entrada={
		'numero': q14,
	        'letra': q14,
	}
        try:
                global state
                state = entrada[x]
        except KeyError:
                global state
                state = q15
        global string
        string = string + x
	return 0

def q15(x):
        global string
        string = string[:-1]
        if(string.upper in palabrasReservadas):
                tokens.append[string.upper,string]
        else:
                tokens.append["IDENTIFICADOR",string]
        global string
        string =""
        global state
        state ='q0'
        return 1

def q16(x):
        tokens.append["OPERADOR_ARITMETICO",string]
        global string
        string =""
        global state
        state ='q0'
        return 0

def q17(x):
        tokens.append["OPERADOR_ARITMETICO",string]
        global string
        string =""
        global state
        state ='q0'
        return 0

def q18(x):
        tokens.append["OPERADOR_TERMINO",string]
        global string
        string = ""
        global state
        state = 'q0'
        return 0

def q19(x):
        tokens.append["OPERADOR_TERMINO",string]
        global string
        string = ""
        global state
        state = 'q0'
        return 0

def q20(x):
        tokens.append["PUNTO",string]
        global string
        string=""
        global state
        state = 'q0'
        return 0

def q21(x):
        tokens.append["PARENTESIS_A",string]
        global string
        string = ""
        global state
        state = 'q0'
        return 0


def q22(x):
        tokens.append["PARENTESIS_C",string]
        global string
        string = ""
        global state
        state = 'q0'
        return 0


def process(line):
	#estados = {
	    #''q0'': a,
	    #'q1': b,
	    #'q2': c,
	    #'q3': a,
	    #'q4': a,
	    #'q5': a,
	    #'q6': a,
	    #'q7': a,
	    #'q8': a,
	    #'q9': a,
	    #'q10': a,
	    #'q11': a,
	    #'q12': a,
	    #'q13': a,
	    #'q14': a,
	    #'q15': a,
	    #'q16': a,
	    #'q17': a,
	    #'q18': a,
	    #'q19': a,
	    #'q20': a,
	    #'q21': a,
	    #'q22': a,
	    #'q23': a,
	    #'q24': a,
	    #'q25': a,
	    #'q26': a,
	    #'q27': a,
	    #'q28': a,
	    #'q29': a,
	    #'q30': a,
	    #'q31': a,
	#}
	for i in xrange(len(line)):
		x = line[i]
		print "El estado es: " + state
		print "X es: " + repr(x)
		#valor = estados[state](x)
                valor = state(x)                   #Valor almacena cuantos caracteres hay que retroceder luego de llegar al estado
                i = i - valor
    #x = x+1
	#print estados

 

#Procesamos el archivo    
with open(archivo) as f:
    for line in f:
		tokens.append(process(line))

close(archivo)
print tokens
    
#letras = string.ascii_lowercase
#letras = string.join(map(chr, range(97, 123)),'\',\'') #or list(map(chr, range(ord('a'), ord('z')+1)))

#print "Que hermoso switch que hice en Python"


    
