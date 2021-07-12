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
import pandas as pd

##INPUTS

#1) Pide input file y genera el outfile name
# parser = ArgumentParser()
# parser.add_argument('-f','--file', type=str, required=True)
# file = parser.parse_args()

#2) usa el ultimo archivo modificado como entrada. Acepta multiples formatos
extensions_allowed = ['xls','xlsx']
#Cant de inputs
input_amount = ''
input_amount = input("Cant de archivos de entrada? (Default:1)")
if input_amount:
    input_amount = int(input_amount)
else:
    input_amount = 1
list_of_files = []
file, filename, file_extension = [], [], []
try:
    #Busca todos los archivos con las extensiones pasadas
    for i in range(len(extensions_allowed)):
        list_of_files += glob.glob(r'*.'+extensions_allowed[i])
    #Comprueba que input_amount no sea mayor al tamaño de la lista
    if input_amount > len(list_of_files):
        print(f"No hay {input_amount} files en la carpeta {os.getcwdb()}")    
        sys.exit(1)
    #Sorted list of latest inputs
    sorted_files = sorted(list_of_files, key=os.path.getctime)
    for i in range(input_amount):
        file.append(sorted_files[-(i+1)])
        print(f"Leyendo archivo: {file[i]}\n ")
        #Get the extension of file and the root
        filename.append(os.path.splitext(file[i])[0])
        file_extension.append(os.path.splitext(file[i])[1])
        out_file_name = filename[i]
except ValueError as err:
    print(f"ERROR No hay {file_extension} en el directorio actual ({os.getcwdb()})")
    sys.exit(1)

#MAIN
print(file[0])
df = pd.read_excel(file[0], skiprows=1)
df2 = df[df['Información'].str.contains("Subasta")]
df3 = df2.groupby(['Cuenta']).sum()
#Segundo dataframe/archivo
if input_amount > 1:
    print(file[1])
    df4 = pd.read_excel(file[1], skiprows=1)
    df5 = df4[df4['Información'].str.contains("Subasta")]
    df6 = df5.groupby(['Cuenta']).sum()
    #Unimos ambos dataframes
    frames = [df3, df6]
    df3 = pd.concat(frames)
#Guardamos el csv
print(f'Output: {out_file_name}-edited.csv ')
df3.to_csv(out_file_name+'-edited.csv', sep=';',header=True, index=True, decimal=',') #guarda en csv