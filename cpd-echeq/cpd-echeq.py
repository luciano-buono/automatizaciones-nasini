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
file_extension = ['xlsx','xls']
list_of_files = []
try:
    list_of_files += glob.glob(r'*.'+file_extension[0])
    list_of_files += glob.glob(r'*.'+file_extension[1])
    file = max(list_of_files, key=os.path.getmtime)
    print(f"Leyendo archivo: {file}\n ")
    #Get the extension of file
    filename, file_extension = os.path.splitext(file)
    out_file_name = filename
except ValueError as err:
    print(f"ERROR No hay {file_extension} en el directorio actual (${os.getcwdb()})")
    sys.exit(1)

##MAIN
df = pd.read_excel(file, skiprows=1)
df2 = df[df['Información'].str.contains("Subasta")]
df3 = df2.groupby(['Cuenta']).sum()
df4 = df3.reset_index()
#Guardamos el csv
print(f'Output: {out_file_name}-edited.csv ')
df4.to_csv(out_file_name+'-edited.csv', sep=';',header=True, index=False, decimal=',') #guarda en csv