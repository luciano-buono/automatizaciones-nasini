##IMPORTS
from argparse import ArgumentParser
import csv
import os, glob, sys
import pandas as pd

##INPUTS

#1) Pide input file y genera el outfile name
# parser = ArgumentParser()
# parser.add_argument('-f','--file', type=str, required=True)
# file = parser.parse_args()

#2) usa el ultimo archivo modificado como entrada. Acepta multiples formatos
extensions_allowed = ['DAT']
#Cant de inputs
input_amount = 2
#Comentar si solo es 1
# input_amount = input("Cant de archivos de entrada? (Default:1)") 
if not input_amount:
    input_amount = 1
else:
    input_amount = int(input_amount)
# -----
list_of_files = []
file, filename, file_extension = [], [], []
try:
    #Busca todos los archivos con las extensiones pasadas
    for i in range(len(extensions_allowed)):
        list_of_files += glob.glob(r'*.'+extensions_allowed[i])
    #Comprueba que input_amount no sea mayor al tamaño de la lista
    if input_amount > len(list_of_files):
        print(f"Hay {len(list_of_files)} archivos en  {os.getcwdb()}")    
    #Sorted list of latest inputs
    sorted_files = sorted(list_of_files, key=os.path.getctime)
    for i in range(len(list_of_files)):
        file.append(sorted_files[-(i+1)])
        print(f"Leyendo archivo: {file[i]}\n ")
        #Get the extension of file and the root
        filename.append(os.path.splitext(file[i])[0])
        file_extension.append(os.path.splitext(file[i])[1])
        out_file_name = filename[i]
except ValueError as err:
    print(f"ERROR No hay {file_extension} en el directorio actual ({os.getcwdb()})")
    sys.exit(1)



file_sorted = []
filename_sorted = []
for f in file:
    if 'OFERTASO' in f:
        file_sorted.append(f)
        filename_sorted.append(os.path.splitext(f)[0])
for f in file:
    if 'OPERSEC' in f:
        file_sorted.append(f)
        filename_sorted.append(os.path.splitext(f)[0])

#numero de comitente a buscar
comitente = int(input("Ingrese nro de comitente: "))

#Main
with open(file_sorted[0]) as file0, \
        open(file_sorted[1]) as file1,\
        open(f'{filename_sorted[0]}-{comitente}{file_extension[0]}', 'w', newline='') as file0_final,\
        open(f'{filename_sorted[1]}-{comitente}{file_extension[1]}', 'w', newline='') as file1_final:
    
    file0_contents = file0.readlines()
    for row in file0_contents:
        if f' {comitente}"' in row:
            file0_final.write(f'{row}')
    file1_contents = file1.readlines()
    for row in file1_contents:
        if f'"{comitente} ' in row:
            file1_final.write(f'{row}')