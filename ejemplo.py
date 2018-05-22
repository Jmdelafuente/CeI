import string
import random

def a(x):
    x= x * 5
    print x

def b(x):
    x= x + 7
    print x

def c(x):
    x= x - 2
    print x
    
x=1
#letras = string.ascii_lowercase
#letras = string.join(map(chr, range(97, 123)),'\',\'') #or list(map(chr, range(ord('a'), ord('z')+1)))
letras =  "\'"+(string.join(map(chr, range(97, 123)),'\',\'')).replace("\"","'")+"'"
estados = {
    'a': a,
    'b': b,
    'c': c,
    'd': a,
    'e': a,
    'f': a,
    'g': a,
    'h': a,
    'i': a,
    'j': a,
    'k': a,
    'l': a,
    'm': a,
    'n': a,
    'o': a,
    'p': a,
    'q': a,
    'r': a,
    's': a,
    't': a,
    'u': a,
    'v': a,
    'w': a,
    'x': a,
    'y': a,
    'z': a,
    '+': a,
    '-': a,
    '*': a,
    '/': a,
    '=': a,
    ':=': a,
}
print estados

for i in xrange(10):
    state= random.choice('abc')
    print "El estado es: " + state
    print "X es: " + repr(x)


    valor = estados[state](x)
    #x = x+1
print "Que hermoso switch que hice en Python"


    
