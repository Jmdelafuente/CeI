'Nested contexts trees for implementing nested scopes (static or dynamic)'

from collections import MutableMapping
from itertools import chain, imap

class Contexto(MutableMapping):
    ''' Nested contexts -- a chain of mapping objects.

    c = Contexto()           Crear contexto root
    d = c.new_child()       Crear contexto hijo anidado. Inherente a enable_nonlocal
    e = c.new_child()       Hijo de c, independiente de d
    e.root                  Root -- exactamente como los globals de Python
    e.map                   Diccionario del contexto actual -- como los locales de Python
    e.parent                Clausura de contextos -- exactamente como los nonlocals de Python

    d['x']                  Recuperar el primer valor para la clave x en la cadena de contextos
    d['x'] = 1              Setter para el valor en el contexto actual
    del['x']                Eliminar para el contexto actual
    list(d)                 Todos los valores anidados
    k in d                  Chequear todos los valores anidados
    len(d)                  Cantidad de valores anidados
    d.items()               TODOS los valores anidados

    Mutations (such as sets and deletes) are restricted to the current context
    when "enable_nonlocal" is set to False (the default).  So c[k]=v will always
    write to self.map, the current context.

    But with "enable_nonlocal" set to True, variable in the enclosing contexts
    can be mutated.  For example, to implement writeable scopes for nonlocals:

        nonlocals = c.parent.new_child(enable_nonlocal=True)
        nonlocals['y'] = 10     # overwrite existing entry in a nested scope

    To emulate Python's globals(), read and write from the the root context:

        globals = c.root        # look-up the outermost enclosing context
        globals['x'] = 10       # assign directly to that context

    To implement dynamic scoping (where functions can read their caller's
    namespace), pass child contexts as an argument in a function call:

        def f(ctx):
            ctx.update(x=3, y=5)
            g(ctx.new_child())

        def g(ctx):
            ctx['z'] = 8                    # write to local context
            print ctx['x'] * 10 + ctx['y']  # read from the caller's context

    '''
    def __init__(self, enable_nonlocal=False, parent=None):
        'Create a new root context'
        self.parent = parent
        self.enable_nonlocal = enable_nonlocal
        self.map = {}
        self.maps = [self.map]
        if parent is not None:
            self.maps += parent.maps

    def new_child(self, enable_nonlocal=None):
        'Make a child context, inheriting enable_nonlocal unless specified'
        enable_nonlocal = self.enable_nonlocal if enable_nonlocal is None else enable_nonlocal
        return self.__class__(enable_nonlocal=enable_nonlocal, parent=self)

    @property
    def root(self):
        'Return root context (highest level ancestor)'
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

