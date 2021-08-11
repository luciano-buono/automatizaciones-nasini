#DESCRIPCION
# Trabajo en pandas para facilitar 
# la suma de primas diferencias de riskmanager y datos de aune


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
extensions_allowed = ['xls','xlsx','csv']
#Cant de inputs
input_amount = 5
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

#Ordenamos los archivos
file_sorted = []
filename_sorted = []
for f in file:
    if 'Productos por moneda' in f:
        file_sorted.append(f)
        filename_sorted.append(os.path.splitext(f)[0])
for f in file:
    if 'Cartera' in f:
        file_sorted.append(f)
        filename_sorted.append(os.path.splitext(f)[0])
for f in file:
    if 'export -' in f:
        file_sorted.append(f)
        filename_sorted.append(os.path.splitext(f)[0])
for f in file:
    if 'gvRegistryAccount' in f:
        file_sorted.append(f)
        filename_sorted.append(os.path.splitext(f)[0])
#Revisamos orden
for f in file_sorted:
    print (f)

##MAIN
#Leemos el archivo traido de AUNE y sacamos Tabla Diferencias Tabla Primas
with open(file[1]) as file_cartera, \
        open(f'diferencias{file_extension[1]}', 'w', newline='') as file_cartera_diferencias,\
        open(f'primas{file_extension[1]}', 'w', newline='') as file_cartera_primas:
    start1 = 0
    end1 = 0
    flag1 = False
    reader = csv.reader(file_cartera, delimiter=';')
    orders = list(reader)
    writer = csv.writer(file_cartera_diferencias, delimiter= ';')
    for row in orders:
        #Busco la tabla de Diferencias
        if "Listado de Productos con Interes Abierto, discriminado por comitente" in row:
            # print (reader.line_num)
            start1 = reader.line_num
            flag1 = True
        if flag1:
            # print(row)
            writer.writerow(row)
            if not row:
                end = reader.line_num
                # print (end)
                break
    #Leemos el archivo y sacamos Primas    
    start2 = 0
    end2 = 0
    flag2 = False    
    reader2 = csv.reader(file_cartera, delimiter=';')
    writer2 = csv.writer(file_cartera_primas, delimiter= ';')
    for row in orders:
        #Busco la tabla de Diferencias
        if "Listado de Portfolio detallado, discriminando segun origen: Portfolio Anterior (PA), operado en la Rueda (R) y operaciones Simuladas (S)" in row:
            # print (reader2.line_num)
            start2 = reader2.line_num
            flag2 = True
        if flag2:
            # print(row)
            writer2.writerow(row)
            if not row:
                end = reader2.line_num
                # print (end)
                break

#-----------Comienzo de procesado de datos con pandas-----------------#
