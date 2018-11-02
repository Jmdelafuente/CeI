#!/usr/bin/env python
# coding=utf-8

'''#Authors: Bonet Peinado Daiana, de la Fuente Juan M.
#Year: 2018
#License: GNU GPLv3. See LICENSE file for more information.'''

import fnmatch
import argparse
import os
import analizadorLexico
from tabla import Tabla

#from analizadorLexico import lexema

# Variables globales

# Bandera de modo verboso
global verbose

# Preanalisis procesado
global preanalisis
global preanalisisAnterior
preanalisis = ""
preanalisisAnterior = ""

# Posicion del token analizado
global posicion
posicion = 0

# Definicion de palabras palabras reservadas
global palabrasReservadas
palabrasReservadas = ["BEGIN", "BOOLEAN", "END", "WHILE", "TRUE", "FALSE", "IF", "ELSE",
                      "PROGRAM", "DO", "THEN", "FUNCTION", "INTEGER", "PROCEDURE", "READ", "VAR", "WRITE"]


# Variables para Analisis Semántico
# Tabla de Simbolos y entrada actual
global tablaSimbolos
tablaSimbolos = None
global tablaActual
tablaActual = None
global identificadoresActuales
identificadoresActuales = list()


## Generación de Código Intermedio
global codigo
codigo = ""
global dirVariable
dirVariable = 1
global nivel
nivel = 1
global etiqueta
etiqueta = 0
global definicionVariables,esParametro
definicionVariables=0
esParametro = False
# Definicion de casos posibles


def digitos():
    ret = "VOID"
    global codigo
    if verbose:
        print("-->digitos")
    if(preanalisis == "numero"):
        # Almaceno el valor del numero encontrado
        numero = analizadorLexico.lexema
        match("numero")
        codigo += "APCT "+str(numero)+"\n"
        ret = "INTEGER"
    elif (preanalisis == "operador_aritmetico"):
        # Almaceno el valor del operador encontrado
        operador = analizadorLexico.lexema
        match("operador_aritmetico")
        # Almaceno el valor del numero encontrado
        numero = analizadorLexico.lexema
        match("numero")
        # MEPA: Calculo de la operacion unaria
        if(operador == "-"): # Si es un menor unario existe codigo relacionado
            operador = "UMEN \n"
        else: # Si es un + unario, no es necesario aplicar operacion
            operador = ""
        codigo += "APCT "+str(numero)+"\n"
        codigo += operador
        ret = "INTEGER"
    else:
        reportar("Error de Sintaxis: se esperaba un numero, - o + ",
                 preanalisis, "digitos")
    if verbose:
        print("<--digitos")
    return ret


def identificador():
    global identificadoresActuales
    global preanalisis
    ret = "VOID"
    if verbose:
        print("-->identificador")
    if(preanalisis == "identificador"):
        # Se añade el identificador a la lista de identificadores pendientes
        identificadoresActuales.append(analizadorLexico.lexema)
        # Sintactico
        match('identificador')
        ret = "VOID"
    else:
        reportar("Error de Sintaxis: se esperaba un identificador valido",
                 preanalisis, "identificador")
    if verbose:
        print("<--identificador")
    return ret


def declaracionVariables():
    global codigo,definicionVariables
    ret = "VOID"
    if verbose:
        print("-->declaracionVariables")
    if(preanalisis == 'var'):
        match('var')
        ret = listaVariables()
        if definicionVariables and not esParametro:
            codigo += "RMEM "+str(definicionVariables)+"\n"
        definicionVariables=0
    else:
        reportar("Error de Sintaxis: se esperaba VAR",
                 preanalisis, "declaracionVariables")
    if verbose:
        print("<--declaracionVariables")
    return ret


def listaVariables():
    ret = "VOID"
    if verbose:
        print("-->listaVariables")
    if(preanalisis == "identificador"):
        ret = listaIdentificador()
        match("dos_puntos")
        if not(tipoVariables() == ret):
            #ret = "Error"
            reportar("Error en los identificadores de la definición. ",
                     preanalisis, "listaVariables", "Semantico")
        match('punto_coma')
        if not(listaVariablesRep() == ret):
            reportar("Error en los identificadores de la definición.  ",
                     preanalisis, "listaVariables", "Semantico")
            #ret = "Error"
    else:
        reportar("Error de Sintaxis: se esperaba un identificador valido",
                 preanalisis, "listaVariables")
    if verbose:
        print("<--listaVariables")
    return ret


def listaVariablesRep():
    global identificadoresActuales
    ret = "VOID"
    if verbose:
        print("-->listaVariablesRep")
    if(preanalisis == "identificador"):
        # Semantico:Si se definen mas variables, es necesario re-comenzar la lista
        identificadoresActuales = []
        # Sintactico
        ret = listaVariables()
    elif verbose:
        print('\033[93m' + "> Lambda") + '\033[0m'
    if verbose:
        print("<--listaVariablesRep")
    return ret


def listaIdentificador():
    ret = "VOID"
    if verbose:
        print("-->listaIdentificador")
    if(preanalisis == "identificador"):
        ret = identificador()
        if not(listaIdentificadorRep() == ret):
            reportar("Error en los identificadores de la definición. ",
                     preanalisis, "listaIdentificador", "Semantico")
            #ret = "Error"
    else:
        reportar("Error de Sintaxis: se esperaba un identificador valido",
                 preanalisis, "listaIdentificador")
    if verbose:
        print("<--listaIdentificador")
    return ret


def listaIdentificadorRep():
    ret = "VOID"
    if verbose:
        print("-->listaIdentificadorRep")
    if preanalisis == "coma":
        match("coma")
        ret = identificador()
        if not listaIdentificadorRep() == ret:
            reportar("Error en los identificadores de la definición. ",
                     preanalisis, "listaIdentificadorRep", "Semantico")
            #ret = "Error"
    elif verbose:
        print('\033[93m' + "> Lambda") + '\033[0m'
    if verbose:
        print("<--listaIdentificadorRep")
    return ret


def tipoVariables():
    global codigo,definicionVariables
    ret = "VOID"
    if verbose:
        print("-->tipoVariable")
    if(preanalisis == "integer"):
        # # MEPA: reservamos el espacio para la variable
        # codigo += "RMEM "+str(len(identificadoresActuales))+"\n"
        # Semantico: se añade el tipo a los identificadores almacenados
        definicionVariables += len(identificadoresActuales)
        generarEntradas(preanalisis)
        # Sintactico
        match("integer")
    elif(preanalisis == "boolean"):
        # Semantico: se añade el tipo a la lista de variables definida
        definicionVariables += len(identificadoresActuales)
        generarEntradas(preanalisis)
        # Sintactico
        match("boolean")
    else:
        reportar("Error de Sintaxis: se esperaba INTEGER o BOOLEAN",
                 preanalisis, "tipoVariables")
    if verbose:
        print("<--tipoVariable")
    return ret


def sentenciaCompuesta():
    ret = "VOID"
    if verbose:
        print("-->sentenciaCompuesta")
    if(preanalisis == "begin"):
        match("begin")
        ret = compuesta()
        match("end")
        match("punto_coma")
    else:
        reportar("Error de Sintaxis: se esperaba BEGIN",
                 preanalisis, "sentenciaCompuesta")
    if verbose:
        print("<--sentenciaCompuesta")
    return ret


def compuesta():
    ret = "VOID"
    if verbose:
        print("-->compuesta")
    case1 = {'write', 'while', 'read', 'if'}
    if ((preanalisis == "identificador") or (preanalisis in case1)):
        ret = sentencia()
        sentenciaOptativa()
    elif (preanalisis == "begin"):
        ret = sentenciaCompuesta()
        compuesta()
    elif verbose:
        print('\033[93m' + "> Lambda") + '\033[0m'
    if verbose:
        print("<--compuesta")
    return ret


def sentenciaOptativa():
    ret = "VOID"
    if verbose:
        print("-->sentenciaOptativa")
    if(preanalisis == "punto_coma"):
        match("punto_coma")
        # sentenciaOptativa2()
        ret = compuesta()
    elif verbose:
        print('\033[93m' + "> Lambda") + '\033[0m'
    if verbose:
        print("<--sentenciaOptativa")
    return ret


def no():
    ret = "VOID"
    if verbose:
        print("-->no")
    if(preanalisis == "not"):
        match("not")
        ret = "BOOLEAN"
    elif verbose:
        print('\033[93m' + "> Lambda") + '\033[0m'
    if verbose:
        print("<--no")
    return ret


def sentencia():
    global codigo
    ret = "VOID"

    if verbose:
        print("-->sentencia")
    if(preanalisis == "if"):
        ret = ifthen()
    elif(preanalisis == 'while'):
        ret = mientras()
    elif(preanalisis == 'write'):
        match("write")
        match("parentesis_a")
        expresionGeneral()
        match("parentesis_c")
        # MEPA: Salida estandar
        codigo += "IMPR \n"
    elif(preanalisis == "read"):
        match("read")
        match("parentesis_a")
        identificador()
        try:
            id = identificadoresActuales.pop()
            tablaActual[id]

            # MEPA: Leer valor por entrada estandar
            codigo += "LEER \n"
            # MEPA: Asignar valor leido a la variable correspondiente
            nivel = tablaActual[id]["nivel"]
            direccion = tablaActual[id]["direccion"]
            codigo += "APVL "+ str(direccion) +", "+str(nivel)+"\n"
        except KeyError:
            reportar("Se esperaba un identificador valido. ",
                     preanalisis, "sentencia", "Semantico")
            #ret = "Error"
        except IndexError:
            reportar("Se esperaba un identificador valido. ",
                     preanalisis, "sentencia")
        match("parentesis_c")
    elif(preanalisis == "identificador"):
        identificador()
        id = identificadoresActuales.pop()
        ret = asignacionollamada(id)
        try:
            if not ret == (tablaActual[id]["tipo"].upper()):
                reportar("El identificador " + repr(id) + " no es del tipo correcto.", tablaActual[id]["tipo"], "sentencia", "Semantico")
                #ret = "Error"
        except KeyError:
            reportar("El identificador " + repr(id) + " no esta definido. ",
                     preanalisis, "generarVariables", "Semantico")
            #ret = "Error"
    else:
        reportar("Error de Sintaxis: se esperaba READ, WRITE, IF, WHILE o Identificador Valido",
                 preanalisis, "sentencia")
    if verbose:
        print("<--sentencia")
    return ret


def asignacionollamada(id):
    global codigo
    #SEMANTICO: Verificacion de existencia
    try:
        ret = tablaActual[id]["tipo"].upper()
    except KeyError:
        reportar("El identificador " + repr(id) + " no esta definido. ",
                 preanalisis, "generarVariables", "Semantico")
        ret = "VOID"
    #Modo Verboso
    if verbose:
        print("-->asignacionollamada")
    if preanalisis == "asignacion":
        #SEMANTICO: Verificacion que sea una variable o el retorno de una funcion
        try:
            if tablaActual[id]["atributo"] not in {"variable","retorno"}:
                reportar("La asignación no es correcta. El identificador " + repr(id) + " no es asignable. Debe ser una variable ", id, "sentencia", "Semantico")
        except KeyError:
            reportar("El identificador " + repr(id) + " no esta definido. ",
                     preanalisis, "generarVariables", "Semantico")
        match("asignacion")
        ret2 = expresionGeneral()
        if (ret != ret2) and ret != "VOID":
            reportar("La asignación no es correcta. El identificador " + repr(id) + " no es del tipo correcto.", id, "sentencia", "Semantico")
        #MEPA: asignamos el valor final a la variable
        variableAsignacion = tablaActual[id]["direccion"]
        variableNivel = tablaActual[id]["nivel"]
        codigo += "ALVL "+str(variableNivel)+","+str(variableAsignacion)+"\n"
    elif preanalisis == "parentesis_a":
        parametros = None
        idLlamada = None
        try:
            if (tablaActual[id]["atributo"] == "retorno"):
                parametros = tablaActual.parent[id]["parametros"].copy()
                idLlamada = tablaActual.parent[id]
            else:
                idLlamada = tablaActual[id]
                parametros = tablaActual[id]["parametros"].copy()
        except KeyError as ex:
            print ex
            reportar("El identificador " + repr(id) + " no esta definido. ",
            preanalisis, "generarVariables", "Semantico")
        except UnboundLocalError:
            reportar("El identificador " + repr(id) + " no es subprograma. ",
            preanalisis, "generarVariables", "Semantico")
        ret = llamada(parametros,idLlamada)
    #elif preanalisis == "punto_coma":
    #    match("punto_coma")
    #else:
    #    reportar("Error de sintaxis: se esperaba :=, (, o ;",
    #             preanalisis, "asignacionollamada")

    else:
        print "LLEGUEEEEEEEEEEEEE"
        try:
            codigo += "APVL "+str(variableNivel)+","+str(variableAsignacion)+"\n"
            parametros = None
            idLlamada = None
            if (tablaActual[id]["atributo"] == "retorno"):
                parametros = tablaActual.parent[id]["parametros"].copy()
                idLlamada = tablaActual.parent[id]
            elif tablaActual[id]["atributo"] in {"procedure","function"}:
                idLlamada = tablaActual[id]
                parametros = tablaActual[id]["parametros"].copy()
        except KeyError:
            reportar("El identificador " + repr(id) + " no esta definido. ",
            preanalisis, "generarVariables", "Semantico")
        except UnboundLocalError:
            reportar("El identificador " + repr(id) + " no es subprograma. ",
            preanalisis, "generarVariables", "Semantico")
        if parametros:
            reportar("Error: Cantidad de parametros incorrecto. Se esperaba(n) " +
                     str(len(parametros)) + " parametro(s)", preanalisis, "llamada", "Semantico")
        if verbose:
            print('\033[93m' + "> Lambda") + '\033[0m'
    if verbose:
        print("<--asignacionollamada")
    return ret


def expresionAritmetica():
    ret = "VOID"
    if verbose:
        print("-->expresionAritmetica")
    case1 = {"write", "true", "false", "read",
             "parentesis_a", "operador_aritmetico"}
    if (preanalisis == "identificador") or (preanalisis == "numero") or (preanalisis in case1):
        ret = termino()
        ret = expresionAritmetica1(ret)
    else:
        reportar("Error de sintaxis: se esperaba READ, WRITE, TRUE, FALSE, Identificador valido o digitos",
                 preanalisis, "expresionAritmetica")
    if verbose:
        print("<--expresionAritmetica")
    return ret


def expresionAritmetica1(ret):
    global codigo
    #print repr(analizadorLexico.nroLinea)+"ret"+"--------------------------------------------->>>"+repr(ret)
    if verbose:
        print("-->expresionAritmetica1")
    if preanalisis == "operador_aritmetico":
        operador = analizadorLexico.lexema
        match("operador_aritmetico")
        ret2 = termino()
        #print repr(analizadorLexico.nroLinea)+"ret2"+"--------------------------------------------->>>"+repr(ret2)
        if not(ret == "INTEGER" and ret2 == "INTEGER"):
            reportar("El operador "+operador+" se encuentra definido para tipos INTEGER. ",
                     preanalisis, "expresionAritmetica1", "Semantico")
            #ret = "Error"
        # MEPA: Se genera el codigo para la operacion
        if(operador == "+"):
            codigo += "SUMA \n"
        else:
            codigo += "SUST \n"
        ret = expresionAritmetica1(ret2)
    elif verbose:
        print('\033[93m' + "> Lambda") + '\033[0m'
    if verbose:
        print("<--expresionAritmetica1")
    return ret


def termino():
    ret = "VOID"
    if verbose:
        print("-->termino")
    case1 = {"write", "true", "false", "read",
             "operador_aritmetico", "parentesis_a"}
    if((preanalisis == "identificador") or (preanalisis == "numero") or (preanalisis in case1)):
        ret = factor()
        ret = termino1(ret)
    else:
        reportar("Error de Sintaxis: se esperaba WRITE,READ,TRUE,FALSE,Identificador valido o Digitos",
                 preanalisis, "expresionAritmetica1")
    if verbose:
        print("<--termino")
    return ret


def termino1(ret):
    global codigo
    if verbose:
        print("-->termino1")
    if preanalisis == "operador_termino":
        operador = analizadorLexico.lexema
        match("operador_termino")
        if factor() != "INTEGER" or ret != "INTEGER":
            # No son de tipo compatible
            reportar("Tipo Incompatible: el operador "+ str(operador) +" se encuentra definido para tipos INTEGER. ",
                     preanalisis, "termino1", "Semantico")
            #ret = "Error
        # MEPA: codigo para la * y /
        if(operador == "*"):
            codigo += "MULT \n"
        else:
            codigo += "DIVI \n"
        ret = termino1(ret)
    elif verbose:
        print('\033[93m' + "> Lambda") + '\033[0m'
    if verbose:
        print("<--termino1")
    return ret


def factor():
    ret = "VOID"
    parametros = None
    identificadorActual=""
    global codigo
    if verbose:
        print("-->factor")
    if (preanalisis == "identificador"):
        identificador()
        try:
            identificadorActual = identificadoresActuales.pop()
            id = tablaActual[identificadorActual]
        except KeyError:
            reportar("Error: el identificador " + repr(identificadorActual) +
                     " no se encuentra definido. ", preanalisis, "termino1", "Semantico")
            #ret = "Error"
        try:
            if id["atributo"] in {"function", "procedure"}:
                parametros = id["parametros"].copy()
            elif id["atributo"] == "retorno":
                id = tablaActual.parent[identificadorActual]
                parametros = id["parametros"].copy()
            ret = llamada(parametros,id)
        except KeyError:
            ret = llamada(None,id)
        except UnboundLocalError:
            reportar("Error: el identificador " + repr(identificadorActual) +
                     " no se encuentra definido. ", preanalisis, "termino1", "Semantico")
            ret = llamada()
    elif (preanalisis == "write"):
        match("write")
        match("parentesis_a")
        expresionGeneral()
        match("parentesis_c")
        # MEPA: Salida estandar
        codigo += "IMPR \n"
    elif (preanalisis == "read"):
        match("read")
        match("parentesis_a")
        identificador()
        try:
            id = identificadoresActuales.pop()
            ret = tablaActual[id]["tipo"].upper()
            # MEPA: Leer valor por entrada estandar
            codigo += "LEER \n"
            # MEPA: Asignar valor leido a la variable correspondiente
            nivel = tablaActual[id]["nivel"]
            direccion = tablaActual[id]["direccion"]
            codigo += "APVL "+ str(direccion) +", "+str(nivel)+"\n"
        except KeyError:
            reportar("Error: el identificador " + str(id) +
                     "no existe. ", preanalisis, "termino1", "Semantico")
            ret = "ERROR"
        match("parentesis_c")
    elif preanalisis == "numero" or preanalisis == "operador_aritmetico":
        ret = digitos()
    elif preanalisis == "true":
        match("true")
        codigo += "APCT 1"
        ret = "BOOLEAN"
    elif preanalisis == "false":
        match("false")
        codigo += "APCT 0"
        ret = "BOOLEAN"
    elif preanalisis == "parentesis_a":
        match("parentesis_a")
        ret = expresionGeneral()
        match("parentesis_c")
    else:
        reportar(
            "Error de sintaxis: se esperaba WRITE,READ,TRUE,FALSE,DIGITO,NOT,( o Identificador valido", preanalisis, "factor")
    if verbose:
        print("<--factor")
    return ret


def operadorRelacional():
    ret = "VOID"
    if verbose:
        print("-->operadorRelacional")
    if preanalisis == "operador_relacional":
        match("operador_relacional")
    else:
        reportar("Error de sintaxis: se esperaba un operador relacional <,<=,=>,>,<> o =",
                 preanalisis, "operadorRelacional")
    if verbose:
        print("<--operadorRelacional")
    return ret


def programa():
    ret = "VOID"
    global tablaSimbolos
    global tablaActual
    global identificadoresActuales
    global codigo,etiqueta
    if verbose:
        print("-->programa")
    if preanalisis == "program":
        # Semantico:Creación de la Tabla de Simbolos y actualización de la tabla actual
        tablaSimbolos = Tabla()
        tablaActual = tablaSimbolos
        # Sintactico
        match("program")
        # MEPA inicio de programa
        codigo += "INPP \n"
        # Sintactico
        identificador()
        # Semantico: Generamos la entrada para el nombre de Program
        generarEntradas("program")
        # Sintactico
        match("punto_coma")
        declaracionVariableOpt()
        # programaRepPyf()
        # MEPA: etiqueta main
        etiqueta += 1
        etMain = etiqueta
        codigo += "DSVS L"+str(etMain)+"\n"
        declaracionPyfRep()
        match("begin")
        # MEPA: salto incondicional al begin main
        codigo+="L"+str(etMain)+" NADA \n"
        #programaRepSentencia()
        compuesta()
        #ret2 = sentenciaCompuesta()
        match("end")
        match("punto")
        #if not(ret3 == "VOID" and ret1 == "VOID" and ret2 == "VOID"):
        #    reportar("Existen multiples errores semanticos dentro del programa. ",
        #             preanalisis, "programa", "Semantico")
            #ret = "Error"
    else:
        reportar("Error de sintaxis: debe comenzar con la sentencia PROGRAM Identificador",
                 preanalisis, "programa")
    if verbose:
        print("<--programa")
        print repr(tablaSimbolos)
        return ret
    #MEPA: Finalizacion del programa
    codigo+= "PARA \n"


def declaracionVariableOpt():
    ret = "VOID"
    if verbose:
        print("-->declaracionVariablesOpt")
    if preanalisis == "var":
        ret = declaracionVariables()
    elif verbose:
        print('\033[93m' + "> Lambda") + '\033[0m'
    if verbose:
        print("<--declaracionVariablesOpt")
    return ret


# def programaRepSentencia():
#     ret = "VOID"
#     if verbose:
#         print("-->programaRepSentencia")
#     caso1 = {"begin", "read", "write", "while", "if"}
#     if (preanalisis in caso1) or (preanalisis == "identificador"):
#         ret = compuesta()
#         programaRepSentencia()
#         # if not programaRepSentencia() == ret:
#         #ret = "Error"
#     elif verbose:
#         print('\033[93m' + "> Lambda") + '\033[0m'
#     if verbose:
#         print("<--programaRepSentencia")
#     return ret


def expresionGeneral():
    global codigo
    ret2 = "VOID"
    if verbose:
        print("-->expresionGeneral")
    caso1 = {'false', 'true', 'parentesis_a',
             'operador_aritmetico', 'write', 'read', 'not'}  # ,'and'}
    if((preanalisis == "identificador") or (preanalisis == "numero") or (preanalisis in caso1)):
        # compararAnd()
        ret = no()
        ret2 = expresionAritmetica()
        ret2 = expresionRelacional(ret2)
        ret2 = compararAnd(ret2)
        ret2 = expresionGeneral1(ret2)
        if ret == "BOOLEAN":
            # MEPA: Generación del NOT
            codigo += "NEGA \n"
            if ret2!="BOOLEAN":
                reportar("Tipo Incompatible: el operador NOT se encuentra definido para tipos BOOLEAN. ", preanalisis, "expresionGeneral1", "Semantico")
    else:
        reportar("Error de sintaxis: se esperaba WRITE,READ,NOT,TRUE,FALSE,(,-,Digito o Identificador valido", preanalisis, "expresionGeneral")
    if verbose:
        print("<--expresionGeneral")
    #print repr(analizadorLexico.nroLinea)+repr(ret)
    return ret2


def expresionGeneral1(ret):
    global codigo
    if verbose:
        print("-->expresionGeneral1")
    if preanalisis == "or":
        match("or")
        if not(expresionGeneral() == "BOOLEAN" and ret == "BOOLEAN"):
            reportar("Tipo Incompatible: el operador OR se encuentra definido para tipos BOOLEAN. ",
                     preanalisis, "expresionGeneral1", "Semantico")
            #ret = "Error"
        else:
            ret = "BOOLEAN"
        # MEPA: generacion de OR
        codigo += "DISJ \n"
    elif verbose:
        print('\033[93m' + "> Lambda") + '\033[0m'
    if verbose:
        print("<--expresionGeneral1")
    return ret


def expresionRelacional(ret):
    global codigo
    if verbose:
        print("-->expresionRelacional")
    if(preanalisis == "operador_relacional"):
        operador = analizadorLexico.lexema
        operadorRelacional()
        if ret != "INTEGER" or expresionAritmetica() != "INTEGER":
            reportar("Tipo Incompatible: el operador "+ operador +" se encuentra definido para tipo INTEGER. ",
                     preanalisis, "expresionRelacional", "Semantico")
            #ret = "Error"
        else:
            ret = "BOOLEAN"
        # MEPA: Generacion de codigo de relacionales
        if(operador == "<"):
            codigo += "CMME \n"
        elif(operador == ">"):
            codigo += "CMMA \n"
        elif(operador == "="):
            codigo += "CMIG \n"
        elif(operador == "<>"):
            codigo += "CMDG \n"
        elif(operador == "<="):
            codigo += "CMNI \n"
        elif(operador == ">="):
            codigo += "CMYI \n"
    elif verbose:
        print('\033[93m' + "> Lambda") + '\033[0m'
    if verbose:
        print("<--expresionRelacional")
    return ret


def compararAnd(ret):
    global codigo
    if verbose:
        print("-->compararAnd")
    if preanalisis == "and":
        match("and")
        ret3 = no() #MEPA: ver if proximo a la llamada recursiva
        ret2 = expresionAritmetica()
        ret2 = expresionRelacional(ret2)
        if ret != "BOOLEAN" or ret2 != "BOOLEAN":
            reportar("Tipo Incompatible: el operador AND se encuentra definido para tipos BOOLEAN. ",
            preanalisis, "compararAnd", "Semantico")
        # if not(expresionRelacional(ret2) == ret):
        #ret = "Error"
        # MEPA: evaluación del NOT si corresponde
        if(ret3 == "BOOLEAN"): #Si ret3 no es void, se proceso un NOT
            codigo += "NEGA \n"
        # MEPA: generacion de la conjuncion
        codigo += "CONJ \n"
        compararAnd(ret)
        if ret3 == "BOOLEAN" and ret != "BOOLEAN":
                reportar("Tipo Incompatible: el operador NOT se encuentra definido para tipos BOOLEAN. ",preanalisis, "compararAnd", "Semantico")
    elif verbose:
        print('\033[93m' + "> Lambda") + '\033[0m'
    if verbose:
        print("<--compararAnd")
    return ret


def ifthen():
    global etiqueta,codigo
    ret = "VOID"
    if verbose:
        print("-->ifthen")
    if preanalisis == "if":
        match("if")
        if not(expresionGeneral() == "BOOLEAN"):
            reportar("Error: Tipo Incompatible: la condicion del IF debe ser de tipo BOOLEAN. ",
                     preanalisis, "ifthen", "Semantico")
            #ret = "Error"
        match("then")
        #Mepa: Desviar si es Falso
        etiqueta += 1
        codigo += 'DSVF L'+ str(etiqueta) + '\n'
        ret = ifthen1(etiqueta)
    else:
        reportar("Error de sintaxis: se esperaba IF expresion THEN",
                 preanalisis, "ifthen")
    if verbose:
        print("<--ifthen")
    return ret


def ifthen1(etiAnterior):
    ret = "VOID"
    if verbose:
        print("-->ifthen1")
    caso2 = {"read", "write", "while", "if"}
    if preanalisis == "begin":
        match("begin")
        ret = compuesta()
        match("end")
        alternativa(etiAnterior)
        #if not alternativa() == ret:
        #    reportar("Error: existen errores semanticos en las expresiones",
        #             preanalisis, "ifthen1", "Semantico")
            #ret = "Error"
    elif ((preanalisis in caso2) or (preanalisis == "identificador")):
        ret = sentencia()
        alternativa(etiAnterior)
        #if not alternativa() == ret:
        #    reportar("Error: existen errores semanticos en las expresiones",
        #             preanalisis, "ifthen1", "Semantico")
            #ret = "Error"
    else:
        reportar("Error de sintaxis: se esperaba WRITE,READ,WHILE,IF,BEGIN o Identificador valido",
                 preanalisis, "ifthen1")
    if verbose:
        print("<--ifthen1")
    return ret

def alternativa(etiAnterior):
    global etiqueta,codigo
    ret = "VOID"
    if verbose:
        print("-->alternativa")
    if (preanalisis == "punto_coma"):
        match("punto_coma")
        #Mepa: No tiene ELSE
        codigo +='L'+ str(etiqueta)+' NADA \n'
    elif (preanalisis == "else"):
        match("else")
        #Mepa: Desvia siempre
        etiqueta += 1
        codigo += 'DSVS L' + str(etiqueta) + '\n'
        #Mepa: Tiene ELSE
        codigo += 'L'+ str(etiAnterior)+' NADA \n'
        ret = compuesta()
        #Mepa: No tiene ELSE
        codigo += 'L' + str(etiqueta)+' NADA \n'
    else:
        reportar("Error de sintaxis: se esperaba ; o ELSE",
                 preanalisis, "alternativa")
    if verbose:
        print("<--alternativa")
    return ret


def mientras():
    global codigo
    global etiqueta
    ret = "VOID"
    if verbose:
        print("-->mientras")
    if (preanalisis == "while"):
        match("while")
        #MEPA: Se define la vuelta del WHILE
        etiqueta +=1
        etiRepetitiva = etiqueta
        codigo += 'L' + str(etiqueta) + ' NADA \n'
        ret = expresionGeneral()

        if  ret != "BOOLEAN":
            reportar("Error de Tipo: la condicion del WHILE debe ser de tipo BOOLEAN.",
                     preanalisis, "mientras", "Semantico")
            #ret = "Error"
        match("do")
        #MEPA: Si la condicion es falsa
        etiqueta += 1
        etiFalso = etiqueta
        codigo += 'DSVF L' + str(etiqueta) + '\n'
        ret = sentenciaCompuesta()
        #MEPA: Definicion del salto del mientras
        codigo += 'DSVS L' + str(etiRepetitiva) + '\n'

        #MEPA: Codigo a realizar cuando finaliza la repetitiva
        codigo += 'L'+str(etiFalso) + ' NADA \n'
        #sentenciaCompuesta()
    else:
        reportar("Error de sintaxis: se esperaba WHILE",
                 preanalisis, "mientras")
    if verbose:
        print("<--mientras")
    return ret


def declaracionPyf():
    global tablaActual
    global identificadoresActuales
    # MEPA: variables para la generación de código intermedio
    global codigo,nivel,dirVariable,etiqueta,esParametro

    ret = "VOID"
    nombreSubprograma = ""
    if verbose:
        print("-->declaracionPyf")
    if preanalisis == "procedure":
        # Sintactico
        match("procedure")
        identificador()
        try:
            # Semantico: Generar entrada en la Tabla para el procedimiento
            # guardamos temporalmente el nombre del subprograma
            nombreSubprograma = identificadoresActuales[0]
            # generamos la entrada en la Tabla de Simbolos para el subprograma
            generarEntradas("void")
            tablaActual[nombreSubprograma].update({"atributo":"procedure","nivel":nivel})
            # Semantico: Cambio de ambito: de Program a Procedure -lectura de parametros-
            # generamos un contexto para guardar los parametros
            tablaActual = tablaActual.new_child()
            # MEPA: definicion de parametros no reserva memoria
            esParametro = True
            # Sintactico
            ret = parametrosFormales()
            esParametro = False
            # Semantico: Los parametros deben figurar como variables en el contexto del procedure que es el nuevo actual
            # guardamos los parametros en la Tabla de Simbols del padre
            tablaActual.parent[nombreSubprograma].update(
                {"parametros": tablaActual.map.copy()})
            # MEPA: Modificacion de desplazamiento correspondiente para los parametrosReales
            iesimoParametro=1
            parametros = tablaActual.parent[nombreSubprograma]["parametros"]
            n = len(parametros)
            for parametro in parametros:
                tablaActual[parametro]["direccion"]=-(n + 3 - iesimoParametro)
                iesimoParametro += 1

            #MEPA: Se modifica el contador de variables
            dirVariable = 1
            # MEPA: Asignacion de etiqueta
            etiqueta += etiqueta + 1
            tablaActual.parent[nombreSubprograma].update(
                {"etiqueta": 'L'+str(etiqueta)})
            #MEPA: Entra al procedimiento de nivel 'K'
            nivel += 1
            codigo += tablaActual.parent[nombreSubprograma]["etiqueta"] + " ENPR "+str(nivel)+"\n"
            # Sintactico
            match("punto_coma")
            ret1 = declaracionVariableOpt()
            ret2 = declaracionPyfRep()
            # ret3 = sentenciaCompuesta()
            match("begin")
            #ret3 = programaRepSentencia()
            ret3 = compuesta()
            match("end")
            match("punto_coma")
            if not(ret == "VOID" and ret1 == "VOID" and ret2 == "VOID" and not(ret3 == "ERROR")):
                reportar("Error: existen errores semanticos en la definicion del PROCEDURE " +
                         str(nombreSubprograma), preanalisis, "declaracionPyf", "Semantico")
                #ret = "Error"
            # MEPA: Liberar memoria de variables locales
            codigo += "LMEM "+ str(len(tablaActual)-len(tablaActual.parent[nombreSubprograma]["parametros"]))+ "\n"
            #MEPA: Se retorna al nivel superior
            nivel-=1
            codigo += "RTPR "+ str(nivel)+","+str(len(tablaActual.parent[nombreSubprograma]["parametros"]))+ "\n"
            # Semantico: Cambio de contexto: desapilo la tabla procedure
            identificadoresActuales = []
            tablaActual = tablaActual.parent
        except IndexError:
            reportar("Error: existen errores semanticos en la definicion del PROCEDURE " +
                     str(nombreSubprograma), preanalisis, "declaracionPyf", "Semantico")
    elif preanalisis == "function":
        # Sintactico
        # codigo += "RMEM 1 \n"
        match("function")
        identificador()
        try:
            # Semantico: Generar entrada en la Tabla para el procedimiento y almacenar el nombre de la funcion para su variable ret
            # guardamos temporalmente el nombre del subprograma
            nombreSubprograma = identificadoresActuales[0]
            variableRetorno = identificadoresActuales
            generarEntradas("function")
            tablaActual[nombreSubprograma].update({"atributo":"function","nivel":nivel})
            # Semantico: Cambio de contexto: de Program a Function
            tablaActual = tablaActual.new_child()
            # MEPA: definicion de parametros no reserva memoria
            esParametro = True
            # Sintactico
            ret1 = parametrosFormales()
            esParametro = False
            # MEPA: Modificacion de desplazamiento correspondiente para los parametrosReales
            iesimoParametro=1
            parametros = tablaActual.parent[nombreSubprograma]["parametros"]
            n = len(parametros)
            for parametro in parametros:
                tablaActual[parametro]["direccion"]=-(n + 3 - iesimoParametro)
                iesimoParametro += 1
            # Semantico: Los parametros deben figurar como variables en el contexto del procedure que es el nuevo actual
            # guardamos los parametros en la Tabla de Simbols del padre
            tablaActual.parent[nombreSubprograma].update(
                {"parametros": tablaActual.map.copy()})
            match("dos_puntos")
            # Semantico: Definimos la variable de retorno para ser insertada con su tipo de Variable
            identificadoresActuales = variableRetorno
            # Sintactico
            ret = tipoVariables()
            #Semantico: definimos la variable con el nombre del subprograma como "retorno"
            tablaActual[nombreSubprograma]["atributo"]="retorno"
            # MEPA: Modifico la direccion de la variable de retorno de la funcion a la correspodiente -(n + 3)
            tablaActual[nombreSubprograma]["direccion"]= - (len(tablaActual.parent[nombreSubprograma]["parametros"]) + 3)
            #Semantico: asignacion de tipo y atributo de la funcion en la tabla de simbolos
            tipoFuncion = tablaActual[nombreSubprograma]["tipo"]
            tablaActual.parent[nombreSubprograma].update({"atributo":"function"})
            tablaActual.parent[nombreSubprograma].update({"tipo":tipoFuncion})
            match("punto_coma")
            #MEPA: Se modifica el contador de variables
            dirVariable = 1            #MEPA: Se retorna al nivel superior
            codigo += "RTPR "+ str(nivel)+","+str(len(tablaActual.parent[nombreSubprograma]["parametros"]))+ "\n"
            # MEPA: Asignacion de etiqueta
            etiqueta += etiqueta + 1
            tablaActual.parent[nombreSubprograma].update(
                {"etiqueta": 'L'+str(etiqueta)})
            #MEPA: Entra al procedimiento de nivel 'K'
            nivel += 1
            codigo += tablaActual.parent[nombreSubprograma]["etiqueta"] + " ENPR "+str(nivel)+"\n"
            #SINTACTICO - SEMANTICO
            ret1 = declaracionVariableOpt()
            ret2 = declaracionPyfRep()
            # ret3 = sentenciaCompuesta()
            match("begin")
            #ret3 = programaRepSentencia()
            ret3 = compuesta()
            match("end")
            match("punto_coma")
            if not(ret1 == "VOID" and ret2 == "VOID" and not(ret3 == "ERROR")):
                reportar("Error: existen errores semanticos en la definicion del FUNCTION " +
                         str(nombreSubprograma), preanalisis, "declaracionPyf", "Semantico")
                #ret = "Error"
            # MEPA: Libero memoria
            codigo += "LMEM "+ str(len(tablaActual)-len(tablaActual.parent[nombreSubprograma]["parametros"]))+ "\n"
            #MEPA: Se retorna al nivel superior
            nivel -= 1
            codigo += "RTPR "+ str(nivel)+" "+str(len(tablaActual.parent[nombreSubprograma]["parametros"]))+ "\n"
            # Semantico: Cambio de contexto: desapilo la tabla de function
            identificadoresActuales = []
            tablaActual = tablaActual.parent
        except IndexError:
            reportar("Error: existen errores semanticos en la definicion del PROCEDURE " +
                     str(nombreSubprograma), preanalisis, "declaracionPyf", "Semantico")
    else:
        reportar("Error de sintaxis: se esperaba PROCEDURE o FUNCTION",
                 preanalisis, "declaracionPyf")
    if verbose:
        print("<--declaracionPyf")

    return ret


def parametrosFormales():
    global definicionVariables
    ret = "VOID"
    if verbose:
        print("-->parametrosFormales")
    if preanalisis == "parentesis_a":
        match("parentesis_a")
        ret = listaIdentificador()
        match("dos_puntos")
        tipoVariables()
        # if not(tipoVariables() == ret):
        #ret = "Error"
        parametrosFormalesRep()
        # if not(parametrosFormalesRep() == "VOID"):
        #ret = "Error"
        match("parentesis_c")
        definicionVariables = 0
    elif verbose:
        print('\033[93m' + "> Lambda") + '\033[0m'
    if verbose:
        print("<--parametrosFormales")
    return ret

# def declaracionVariablesRep():
# 	ret = "VOID"
# 	if(verbose):
# 		print("-->declaracionVariablesRep")
# 	if ( preanalisis == "var"):
# 		ret = declaracionVariables()
# 	elif verbose:
# 		print('\033[93m'+"> Lambda")+'\033[0m'
# 	if(verbose):
# 		print("<--declaracionVariablesRep")
# 	return ret


def declaracionPyfRep():
    ret = "VOID"
    if(verbose):
        print("-->declaracionPyfRep")
    if (preanalisis == "function" or preanalisis == "procedure"):
        ret = declaracionPyf()
        if not(declaracionPyfRep() == ret):
            reportar("Error: " + preanalisis + " semanticamente incorrecto ",
                     preanalisis, "parametrosReales", "Semantico")
            ret == "ERROR"
    elif verbose:
        print('\033[93m' + "> Lambda") + '\033[0m'
    if(verbose):
        print("<--declaracionPyfRep")
    return ret


def parametrosFormalesRep():
    ret = "VOID"
    if(verbose):
        print("-->parametrosFormalesRep")
    if (preanalisis == "punto_coma"):
        match("punto_coma")
        listaIdentificador()
        match("dos_puntos")
        tipoVariables()
        parametrosFormalesRep()
    elif verbose:
        print('\033[93m' + "> Lambda") + '\033[0m'
    if(verbose):
        print("<--parametrosFormalesRep")
    return ret


def parametrosReales(parametros):
    ret = "VOID"
    if verbose:
        print("-->parametrosReales")
    if (preanalisis == "coma"):
        match("coma")
        ret = expresionGeneral()
        try:
            parametroActual = parametros.popitem(False)
            identificadorActual = parametroActual[0]
            tipoActual = parametroActual[1]["tipo"].upper()
            if ret != tipoActual:
                    # Tipo de parametro incorrecto
                reportar("Error: El parametro formal " + repr(identificadorActual) + " es de tipo incorrecto. Se esperaba " +
                         tipoActual, preanalisis, "parametrosReales", "Semantico")
                ret = "ERROR"
        except IndexError:
            # Cantidad de parametros incorrecta
            reportar("Error: Cantidad de parametros incorrecto. Se esperaban " +
                     str(len(parametros)) + " parametros más ", preanalisis, "llamada", "Semantico")
            ret = "ERROR"
        except AttributeError:
            reportar("Error: Cantidad de parametros incorrecto. No se esperaban parametros", preanalisis, "llamada", "Semantico")
            ret = "ERROR"
        except KeyError: #Si no requiere parametros y sin embargo tiene
            reportar("Error: Cantidad de parametros incorrecto. No se esperaban más parametros", preanalisis, "llamada", "Semantico")
            ret = "ERROR"
        parametrosReales(parametros)
        # except IndexError:
        # 	#Cantidad de parametros incorrecta
        # 	ret="ERROR"
    elif verbose:
        print('\033[93m' + "> Lambda") + '\033[0m'
    else:
        if parametros:
            reportar("Error: Cantidad de parametros incorrecto. Se esperaban " +
                 str(len(parametros)) + " parametros más", preanalisis, "llamada", "Semantico")
            ret = "ERROR"
    if verbose:
        print("<--parametrosReales")
    return ret


def llamada(parametros=None,id = None):
    global codigo
    #Semantico: tipo del identificador
    ret = "VOID" if id == None else id["tipo"].upper()
    if verbose:
        print("-->llamada")
    #print repr(parametros) + " en linea " + str(analizadorLexico.nroLinea) + " con preanalisis " + repr(preanalisis)
    if preanalisis == "parentesis_a":
        try:
            # MEPA: si es una funcion reserva la posicion para variableRetorno
            if id["atributo"]=="function": #Si es una funcion
                codigo += "RMEM 1 \n" #reservamos la memoria para el retorno
            match("parentesis_a")
            ret2 = expresionGeneral()
            # Vieja posicion del try
            parametroActual = parametros.popitem(False)
            identificadorActual = parametroActual[0]
            tipoActual = parametroActual[1]["tipo"].upper()
            if ret2 != tipoActual:
                # Tipo de parametro incorrecto
                reportar("Error: El parametro formal " + repr(identificadorActual) + " es de tipo incorrecto. Se esperaba " +
                         tipoActual, preanalisis, "llamada", "Semantico")
                ret = "ERROR"
        except IndexError:
            # Cantidad de parametros incorrecta
            reportar("Error: Cantidad de parametros incorrecto. Se esperaba(n) " +
                     str(len(parametros)) + " parametro(s)", preanalisis, "llamada", "Semantico")
            ret = "ERROR"
        except AttributeError: #Si parametros = None, es decir se invoco llamada sin parametros
            reportar("Error: Cantidad de parametros incorrecto. No se esperaban parametros", preanalisis, "llamada", "Semantico")
            ret = "ERROR"
        except KeyError: #Si no requiere parametros y sin embargo tiene
            reportar("Error: Cantidad de parametros incorrecto. No se esperaban parametros", preanalisis, "llamada", "Semantico")
            ret = "ERROR"
        parametrosReales(parametros)
        match("parentesis_c")
        # MEPA: codigo de la llamada a la funcion
        etiqueta = id["etiqueta"]
        codigo += "LLPR "+etiqueta+ "\n"
    elif verbose:
        print('\033[93m' + "> Lambda") + '\033[0m'
    else:
        # MEPA: acceso a variable
        codigo += "APVL "+str(id["nivel"])+","+str(id["direccion"])+"\n"
        if parametros:
            reportar("Error: Cantidad de parametros incorrecto. Se esperaban " +
                 str(len(parametros))+" parametros más ", preanalisis, "llamada", "Semantico")
            ret = "ERROR"
    if verbose:
        print("<--llamada")
    return ret

# Procedimiento Match dado en la teoria


def match(t):
    global preanalisis
    global preanalisisAnterior
    global nroLinea

    if(preanalisis == t):
        if(verbose):
            print '\033[93m' + ">Match:" + str(preanalisis) + '\033[0m'
        preanalisisAnterior = preanalisis
        preanalisis = analizadorLexico.siguientePreanalisis()
        if(verbose):
            print '\033[1m' + ">Preanalisis:" + str(preanalisis) + '\033[0m'
    else:
        reportarMatch("[" + str(analizadorLexico.nroLinea) + "] " +
                      "Error de sintaxis, no se esperaba ", preanalisis, preanalisisAnterior, "match")


def reportar(tipoError, simbolo, metodo, tipoReporte="Sintactico"):
    global error
    global preanalisisAnterior
    global nroLinea
    if tipoReporte == "Sintactico" and analizadorLexico.lexemaAnterior is None:
        err = "[" + str(analizadorLexico.nroLinea) + "] " + tipoError + " en la expresion " + \
            repr(analizadorLexico.lexema) + " \n"
    elif tipoReporte == "Sintactico":
            err = "[" + str(analizadorLexico.nroLinea) + "] " + tipoError + " en la expresion " + \
                repr(analizadorLexico.lexema) + " despues de " + \
                repr(analizadorLexico.lexemaAnterior) + "\n"
    elif tipoReporte == "Semantico":
        err = "[" + str(analizadorLexico.nroLinea) + "] " + tipoError + "\n"
    if(args.standalone):
        print err
        exit(0)
    else:
        if(err):
            filtered = fnmatch.filter(error, tipoError + "\n")
            filtered += fnmatch.filter(error, "*[" + str(analizadorLexico.nroLinea) + "*")
            if not filtered:
                error.append(err)
            # error = list(set(error))
            # print '\033[91m' + "ERRORES DETECTADOS: " + repr(len(error))
            # print '\033[93m' + "[Nro de Linea] Descripcion del error" + '\033[0m'
            # # Ordenamos los errores por linea donde aparecen
            # error.sort()
            # for e in error:
            #     print e
            # os.system('kill %d' % os.getpid())


def reportarMatch(tipoError, simbolo, simboloanterior, metodo):
    global error
    # if(simboloanterior == preanalisis):
    #     err = tipoError + " " + \
    #         repr(preanalisis) + \
    #         ". El archivo debe finalizar con END seguido de punto." + "\n"
    # else:
    err = tipoError + " " + repr(analizadorLexico.lexema) + \
            " despues de " + repr(analizadorLexico.lexemaAnterior) + "\n"
    if(args.standalone):
        print err
        exit(0)
    else:
        filtered = fnmatch.filter(error, "*" + tipoError + "\n")
        filtered += fnmatch.filter(error, "*[" + str(analizadorLexico.nroLinea) + "*")
        if not filtered:
            error.append(err)


def between(value, a, b):
    # Find and validate before-part.
    pos_a = value.find(a)
    if pos_a == -1:
        return ""
    # Find and validate after part.
    pos_b = value.rfind(b)
    if pos_b == -1:
        return ""
    # Return middle part.
    adjusted_pos_a = pos_a + len(a)
    if adjusted_pos_a >= pos_b:
        return ""
    return value[adjusted_pos_a:pos_b]


def main():
    # Error
    global error
    error = []

    # Tokens
    global tokens
    tokens = []

    global nroLinea
    global preanalisis

    archivo = args.archivo
    archivo += ".tokens"
    # Procesamos el archivo linea por linea
    nroLinea = 1
    with open(archivo) as f:
        for line in f:
            linea = between(line, '[', ',')
            linea = linea[1:-1]
            if(linea != ''):
                tokens.append(linea.lower())
    f.close()

    # Comenzamos a procesar los tokens encontrados sabiendo que un programa Pascal comienza con la sentencia program
    if(posicion < len(tokens)):
        preanalisis = tokens[posicion]
        if(verbose):
            print(
                '\033[93m' + "-------->TRAZA DE EJECUCION DE LA GRAMATICA:" + '\033[0m')
        programa()
        print('\033[93m' + "Fin de la ejecucion" + '\033[0m')
    # Salida de Tokens
    if(args.verbose_mode):
        print tokens


def procesar():
    global preanalisis
    global error
    global codigo
    # Comenzamos a procesar los tokens encontrados sabiendo que un programa Pascal comienza con la sentencia program
    preanalisis = analizadorLexico.siguientePreanalisis()
    #if(verbose):
    #    print("-------->TRAZA DE EJECUCION DE LA GRAMATICA:")
    programa()
    # Salida de Tokens
    # if(args.verbose_mode):atom://teletype/portal/0155257b-a858-44b3-9e90-e45c9bfb27c7
    #        print tokens

    if(error):
        error = list(set(error))
        print '\033[91m' + "ERRORES DETECTADOS: " + repr(len(error))
        print '\033[93m' + "[Nro de Linea] Descripcion del error" + '\033[0m'
        # Ordenamos los errores por linea donde aparecen y los imprimimos
        error.sort()
        for e in error:
            print e
        # Terminar la ejecucion
        os.system('kill %d' % os.getpid())
    else:
        print "Analisis finalizado. No hay errores detectados"
    #Salida temporal: Codigo MEPA
    print codigo
# DEFINICIONES SEMANTICO


def generarEntradas(tipo):
    #Variables globales de la tabla de simbolos actual
    global identificadoresActuales,tablaActual
    #Variables gloables de MEPA
    global dirVariable,nivel
    # Añadir cada identificador a la tabla con el tipo asociado
    for identificador in identificadoresActuales:
        # si el identificador existe: añadimos el error
        try:
            tablaActual.map[identificador]
            reportar("Identificador " + repr(identificador) + " ya fue definido anteriormente",
                     identificador, "generarVariables", "Semantico")
        # El identificador no existe
        except KeyError:
            # Appendamos en la tabla el identificador
            tablaActual[identificador] = {"tipo": tipo , "atributo": "variable", "direccion": dirVariable, "nivel":nivel}
            dirVariable += 1
            if(verbose):
                print('\033[92m' + "[SEMANTICO] Nueva entrada: " +
                      repr(identificador) + " : " + repr(tipo) + '\033[0m')
    # Ya se guardaron todos los identificadores en la tabla de simbolos
    identificadoresActuales = []


if __name__ == '__main__':
    # Definicion de argumentos y pasaje de parametros.
    parser = argparse.ArgumentParser(
        description="Analizador Sintactico de Pascal Reducido. \n Para propositos educativos. See LICENSE. \n Bonet Peinado - de la Fuente \n UNCo - FAI 2018 \n USO: analizador ArchivoPascal.pas \n Mas opciones:")
    parser.add_argument(
        "archivo", help="Ruta relativa del fichero a analizar sintacticamente.", type=str)
    parser.add_argument("-verbose_mode", "-v",
                        help="Flag para modo Verboso con todas las impresiones de control.", action='store_true')
    parser.add_argument(
        "-standalone", "-s", help="Flag para funcionamiento por separado del aplicativo.", action='store_true')
    args = parser.parse_args()
    verbose = args.verbose_mode
    # Si funciona como un analizador sintáctico-semántico independiente
    if(args.standalone):
        main()
    else:
        # Si funciona como parte de un compilador de una pasada
        procesar()
