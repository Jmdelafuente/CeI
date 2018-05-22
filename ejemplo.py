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
for i in xrange(10):
    state= random.choice('abc')
    print "El estado es: " + state
    print "X es: " + repr(x)
    result = {
        'a': a,
        'b': b,
        'c': c,
    }
    valor = result[state](x)
    x = x+1
print "Que hermoso switch que hice en Python"


    
print repr(result['a'](1))
