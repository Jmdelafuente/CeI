# coding=utf-8
'Arboles de contextos anidados para implementar alcances anidados (estaticos o dinamicos)'

from collections import MutableMapping
from itertools import chain, imap

class Tabla(MutableMapping):
    ''' Tabla que permite Ambientes anidados -- una cadena de objetos.

    c = Tabla()             Crear tabla root
    d = c.new_child()       Crear tabla hijo anidado. Inherente a enable_nonlocal
    e = c.new_child()       Hijo de c, independiente de d
    e.root                  Root -- exactamente como los globals de Python
    e.map                   Diccionario de la tabla actual -- como los locales de Python
    e.parent                Clausura de tablas -- exactamente como los nonlocals de Python

    d['x']                  Recuperar el primer valor para la clave x en la cadena de contextos
    d['x'] = 1              Setter para el valor en la tabla actual
    del['x']                Eliminar para la tabla actual
    list(d)                 Todos los valores anidados
    k in d                  Chequear todos los valores anidados
    len(d)                  Cantidad de valores anidados
    d.items()               TODOS los valores anidados

    Las modificaciones (como sets y deletes) están restringidas a la tabla actual 
    cuando "enable_nonlocal" está establecido en False (valor predeterminado). 
    Entonces c[k]=v siempre escribe en self.map, en la tabla actual.

    Pero con "enable_nonlocal" establecido en True, la variable en la clausura de la tabla
	se pueden modificar. Por ejemplo, para implementar ambientes editables para nonlocals:
	
        nonlocals = c.parent.new_child(enable_nonlocal=True)
        nonlocals['y'] = 10     #sobrescribir la entrada existente en un ambiente anidado # overwrite existing entry in a nested scope

	Para emular los valores globals() de Python, leer y modificar desde la tabla raíz:
    
        globals = c.root        #buscar la tabla más externa #look-up the outermost enclosing context
        globals['x'] = 10       # asignar directamente a ese tabla #assign directly to that context

    Para implementar el alcance dinámico (donde las funciones pueden leer el 
    espacio de nombres de su intermediario), las tablas secundarias se pasan como un 
    argumento en una llamada a función:

        def f(ctx):
            ctx.update(x=3, y=5)
            g(ctx.new_child())

        def g(ctx):
            ctx['z'] = 8                    # Escribir en la tabla local #write to local context
            print ctx['x'] * 10 + ctx['y']  # Leer desde la tabla que llama #read from the caller's context

    '''
    def __init__(self, enable_nonlocal=False, parent=None):
        'Crear nuevo contexto Raiz'
        self.parent = parent
        self.enable_nonlocal = enable_nonlocal
        self.map = {}
        self.maps = [self.map]
        if parent is not None:
            self.maps += parent.maps

    def new_child(self, enable_nonlocal=None):
        'Generar nuevo hijo, hereda el valor de enable_nonlocal por defecto'
        enable_nonlocal = self.enable_nonlocal if enable_nonlocal is None else enable_nonlocal
        return self.__class__(enable_nonlocal=enable_nonlocal, parent=self)

    @property
    def root(self):
        'Getter para el ambente raiz (el ancestro mas externo)'
        return self if self.parent is None else self.parent.root

    def __getitem__(self, key):
        for m in self.maps:
            if key in m:
                break
        return m[key]

    def __setitem__(self, key, value):
        if self.enable_nonlocal:
            for m in self.maps:
                if key in m:
                    m[key] = value
                    return
        self.map[key] = value

    def __delitem__(self, key):
        if self.enable_nonlocal:
            for m in self.maps:
                if key in m:
                    del m[key]
                    return
        del self.map[key]

    def __len__(self, len=len, sum=sum, imap=imap):
        return sum(imap(len, self.maps))

    def __iter__(self, chain_from_iterable=chain.from_iterable):
        return chain_from_iterable(self.maps)

    def __contains__(self, key, any=any):
        return any(key in m for m in self.maps)

    def __repr__(self, repr=repr):
        return ' -> '.join(imap(repr, self.maps))


