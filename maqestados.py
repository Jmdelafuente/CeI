import string
import random

#Variables globales

#Lista de Tokens reconocidos
tokens=[]
#Estado actual
state='q0'
#Letras
letras =  (string.join(map(chr, range(97, 123)),'\',\'')) + '_'
#Numeros
numeros = xrange(0,9)
	
def q0(x):
	if(x in letras):
		char = letra
	elif(x in numeros):
		char = numero
	else:
		char = x
		
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
	    '+': 'q16',
	    '-': 'q17',
	    '*': 'q18',
	    '/': 'q19',
	    '.': 'q20',
	    '(': 'q21',
	    ')': 'q22',
	    ':': 'q23',
	}
	global state
	state = entrada[char]
	
def q1(x):
    x= x + 7
    print x

def q2(x):
    x= x - 2
    print x
    

#Procesamos el archivo    
with open('/your/path/file') as f:
    for line in f:
        tokens.add(process(line))    
    
#letras = string.ascii_lowercase
#letras = string.join(map(chr, range(97, 123)),'\',\'') #or list(map(chr, range(ord('a'), ord('z')+1)))
def process(line):
	estados = {
	    'q0': a,
	    'q1': b,
	    'q2': c,
	    'q3': a,
	    'q4': a,
	    'q5': a,
	    'q6': a,
	    'q7': a,
	    'q8': a,
	    'q9': a,
	    'q10': a,
	    'q11': a,
	    'q12': a,
	    'q13': a,
	    'q14': a,
	    'q15': a,
	    'q16': a,
	    'q17': a,
	    'q18': a,
	    'q19': a,
	    'q20': a,
	    'q21': a,
	    'q22': a,
	    'q23': a,
	    'q24': a,
	    'q25': a,
	    'q26': a,
	    'q27': a,
	    'q28': a,
	    'q29': a,
	    'q30': a,
	    'q31': a,
	}
	for i in xrange(line.length):
		x = line[i]
		print "El estado es: " + state
		print "X es: " + repr(x)
		valor = estados[state](x)
    #x = x+1
	#print estados


print "Que hermoso switch que hice en Python"


    
