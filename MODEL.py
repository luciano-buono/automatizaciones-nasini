##DESCRIPCION
#El script toma un .dat donde los campos estan separados por comillas (")
#y luego organiza cada linea en base al parametro pasado (tiempo,acciones,
#ID,comitente)
#Toma el archivo.dat mas reciente de la carpeta donde se encuentra el
#workspace, se puede modificas para que pida que archivo tomar

##IMPORTS
from argparse import ArgumentParser
import csv
import os, glob, sys

##INPUTS
#usa el ultimo archivo modificado como entrada
name_of_file = 'OPCIONES.DAT'
try:
    list_of_files = glob.glob(name_of_file)
    file = max(list_of_files, key=os.path.getmtime)
    print(f"Leyendo archivo: {file} ")
except ValueError as err:
    print(f"ERROR No hay {name_of_file} en el directorio actual ({os.getcwdb()})")
    sys.exit(1)
#Get the extension of file
filename, file_extension = os.path.splitext(file)
out_file_name = filename

##MAIN