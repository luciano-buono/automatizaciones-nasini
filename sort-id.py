#El script toma un .dat donde los campos estan separados por comillas (")
#y luego organiza cada linea en base al parametro pasado (tiempo,acciones,
#ID,comitente)
#Toma el archivo.dat mas reciente de la carpeta donde se encuentra el
#workspace, se puede modificas para que pida que archivo tomar

from argparse import ArgumentParser
import csv
import os, glob, sys

def sort_id(line):
    #Get the end of the ID
    line_fields = line.strip().split('"')
    # print(line_fields)
    #Sort by ID
    id = int(line_fields[0])
    #Sort by time
    time = int(line_fields[6])
    #Sort by shares
    share = line_fields[3]
    #Sort by comietente
    comitente = line_fields[8]
    return id

#Pide input file y genera el outfile name
# parser = ArgumentParser()
# parser.add_argument('-f','--file', type=str, required=True)
# file = parser.parse_args()


#usa el ultimo archivo modificado como entrada
try:
    list_of_files = glob.glob(r'*.DAT') # * means all if need specific format then *.csv
    file = max(list_of_files, key=os.path.getmtime)
    print(f"Leyendo archivo: {file}\n ")
except ValueError as err:
    print(f"ERROR No hay .dat en el directorio actual (${os.getcwdb()})")
    sys.exit(1)


#Get the extension of file
filename, file_extension = os.path.splitext(file)
out_file_name = filename



#Abre el archivo y corre sort usando la funcion sort_id como key
with open(file) as in_file, open(f'{out_file_name}-sorted{file_extension}', 'w') as out_file:
    contents = in_file.readlines()
    contents.sort(key=sort_id)

    #Borrar los anteriores al delete_from
    delete_from = input("A partir de que ID borrar? (Vacio para no borrar)")
    delete_from_flag = True
    for line in contents:
        if delete_from:
            if delete_from_flag:
                print(f"Borrando desde: {delete_from}")
                delete_from_flag = False
            line_fields = line.strip().split('"')
            id = int(line_fields[0])
            if id> int(delete_from):
                out_file.write(f'{line}')
        else:
            if delete_from_flag:
                print("No borrando nada")
                delete_from_flag = False
            out_file.write(f'{line}')

