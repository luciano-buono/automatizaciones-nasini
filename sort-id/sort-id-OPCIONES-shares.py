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
    return share

def delete_by_ID(contents,out_file,out_file_name, file_extension):
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
            amount_of_lines += 1
            if delete_from_flag:
                print("No borrando nada\n")
                delete_from_flag = False
            out_file.write(f'{line}')

    if delete_from:
        print(f"{out_file_name}-sorted{file_extension} tiene {amount_of_lines} lineas")
    return amount_of_lines

def delete_by_share(contents,out_file):
    #Borrar los anteriores al delete_from
    share = input("Ingrese las especies separadas por coma. Se borrara todas las especies menos las escritas (Vacio para no borrar)")
    shares = share.split(",")
    shares = [x.strip(' ') for x in shares]
    amount_of_lines = 0
    for line in contents:
        if any(s in line for s in shares):
            amount_of_lines += 1
            out_file.write(line) 
    return amount_of_lines

#Pide input file y genera el outfile name
# parser = ArgumentParser()
# parser.add_argument('-f','--file', type=str, required=True)
# file = parser.parse_args()


def readfile():
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

    return file,out_file_name,file_extension


def procesar(file,out_file_name,file_extension):
    #Abre el archivo y corre sort usando la funcion sort_id como key
    with open(file) as in_file, open(f'{out_file_name}-sorted{file_extension}', 'w') as out_file:
        contents = in_file.readlines()

        print(f"{file} tiene {len(contents)} lineas\n")

        contents.sort(key=sort_id)
        # amount_of_lines = delete_by_ID(contents,out_file,out_file_name, file_extension)
        amount_of_lines = delete_by_share(contents,out_file)
        return amount_of_lines

def split_two_files(file,out_file_name,file_extension, amount_of_lines):
    with open(f'{out_file_name}-sorted{file_extension}', 'r') as f,\
        open(f'{out_file_name}-1sorted{file_extension}','w') as f1,\
            open(f'{out_file_name}-2sorted{file_extension}','w') as f2:
        #Lo parto a la mitad
        contents = f.readlines()
        print(f"Separando las {amount_of_lines} a la mitad")
        for i,line in enumerate(contents):
            if i < amount_of_lines/2:
                f1.write(f'{line}')
            if i >= amount_of_lines/2:
                f2.write(f'{line}')
            if i == amount_of_lines-1:
                print(f"{out_file_name}-sorted{file_extension} ultima linea: {line}")


def main():
    file,out_file_name,file_extension=readfile()
    amount_of_lines = procesar(file,out_file_name,file_extension)
    # split_two_files(file,out_file_name,file_extension, amount_of_lines)


main()    

