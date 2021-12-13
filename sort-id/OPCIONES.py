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



#Abre el archivo y corre sort usando la funcion sort_id como key
with open(file) as in_file, open(f'{out_file_name}-sorted{file_extension}', 'w') as out_file:
    contents = in_file.readlines()
    contents.sort(key=sort_id)

    print(f"{file} tiene {len(contents)} lineas\n")

    #Borrar los anteriores al delete_from
    delete_from = input("A partir de que ID borrar? (Vacio para no borrar)")
    print('En caso de borrar, separa la salida en dos')
    delete_from_flag = True
    amount_of_lines = 0
    for line in contents:
        if delete_from:
            if delete_from_flag:
                print(f"Borrando desde: {delete_from}\n")
                delete_from_flag = False
            line_fields = line.strip().split('"')
            id = int(line_fields[0])
            if id> int(delete_from):
                amount_of_lines += 1
                out_file.write(f'{line}')
        else:
            if delete_from_flag:
                print("No borrando nada\n")
                delete_from_flag = False
            out_file.write(f'{line}')

    if delete_from:
        print(f"{out_file_name}-sorted{file_extension} tiene {amount_of_lines} lineas")
    
# with open(f'{out_file_name}-sorted{file_extension}', 'r') as f,\
#      open(f'{out_file_name}-1sorted{file_extension}','w') as f1,\
#          open(f'{out_file_name}-2sorted{file_extension}','w') as f2:
#     #Lo parto a la mitad
#     contents = f.readlines()
#     print(amount_of_lines)
#     for i,line in enumerate(contents):
#         if i < amount_of_lines/2:
#             f1.write(f'{line}')
#         if i >= amount_of_lines/2:
#             f2.write(f'{line}')
#         if i == amount_of_lines-1:
#             print(f"{out_file_name}-sorted{file_extension} ultima linea: {line}")



def split_file():
    splitLen = 2000         # X lines per file
    outputBase = f'{out_file_name}-sorted' # output.1.txt, output.2.txt, etc.

    # This is shorthand and not friendly with memory
    # on very large files (Sean Cavanagh), but it works.
    input = open(f'{out_file_name}-sorted{file_extension}', 'r').read().split('\n')

    at = 1
    for lines in range(0, len(input), splitLen):
        # First, get the list slice
        outputData = input[lines:lines+splitLen]

        # Now open the output file, join the new slice with newlines
        # and write it out. Then close the file.
        output = open(outputBase + str(at) + '.DAT', 'w')
        output.write('\n'.join(outputData))
        output.close()

        # Increment the counter
        at += 1



split_file()