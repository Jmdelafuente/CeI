#!/usr/bin/env python

#Authors: Bonet Peinado Daiana, de la Fuente Juan M.
#Year: 2018
#License: GNU GPLv3. See LICENSE file for more information.



import Aplicativo
import analizador
import argparse



#Definicion de argumentos y pasaje de parametros.

parser = argparse.ArgumentParser(description="Analizador Sintactico de Pascal Reducido")
parser.add_argument("archivo", help="Ruta relativa del fichero a analizar sintacticamente.", type=str)
parser.add_argument("verbose_mode", help="True para modo Verboso con impresiones de control.",nargs='?', default=False, type=bool)
args = parser.parse_args()

analizador(args.archivo,args.verbose_mode)
archivo = args.archivo
archivo+=".tokens"
Aplicativo.main(archivo,args.verbose_mode)
