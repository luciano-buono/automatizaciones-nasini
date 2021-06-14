#Toma un .csv como data y le modifica  "ClientAccountID" y "Exchange"
#Toma el archivo.dat mas reciente de la carpeta donde se encuentra el
#workspace, se puede modificas para que pida que archivo tomar

from argparse import ArgumentParser
import csv
import os, glob,sys

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


# Abre el archivo y corre sort usando la funcion sort_id como key
with open(file) as in_file, open(f'{out_file_name}-sorted{file_extension}', 'w', newline='') as out_file:
    reader = csv.reader(in_file)
    writer = csv.writer(out_file, quoting=csv.QUOTE_ALL)
    for row in reader:
        # print(row)
        if "AccountAlias" == row[0]:
            row[0] = "ClientAccountID" 
            row[4] = "Exchange"
            writer.writerow(row)
            break
    # print("-----------------------")
    for row in reader:
        # print(row)
        if "AccountAlias" != row[0]: 
            writer.writerow(row)

