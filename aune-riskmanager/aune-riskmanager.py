#!/usr/bin/env python
# coding: utf-8

# In[1]:


#DESCRIPCION
# Trabajo en pandas para facilitar 
# la suma de primas diferencias de riskmanager y datos de aune

##IMPORTS
from argparse import ArgumentParser
import csv
import os, glob, sys
import pandas as pd


# In[2]:


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
file_extension_sorted = []
for f in file:
    if 'Productos por moneda' in f:
        file_sorted.append(f)
        filename_sorted.append(os.path.splitext(f)[0])
        file_extension_sorted.append(os.path.splitext(f)[1])
for f in file:
    if 'Cartera' in f:
        file_sorted.append(f)
        filename_sorted.append(os.path.splitext(f)[0])
        file_extension_sorted.append(os.path.splitext(f)[1])
for f in file:
    if 'export -' in f:
        file_sorted.append(f)
        filename_sorted.append(os.path.splitext(f)[0])
        file_extension_sorted.append(os.path.splitext(f)[1])
for f in file:
    if 'gvRegistryAccount' in f:
        file_sorted.append(f)
        filename_sorted.append(os.path.splitext(f)[0])
        file_extension_sorted.append(os.path.splitext(f)[1])
#Revisamos orden
# for f in file_sorted:
#     print (f)

##MAIN
#Leemos el archivo traido de AUNE y sacamos Tabla Diferencias Tabla Primas
with open(file_sorted[1]) as file_cartera,         open(f'diferencias{file_extension_sorted[1]}', 'w', newline='') as file_cartera_diferencias,        open(f'primas{file_extension_sorted[1]}', 'w', newline='') as file_cartera_primas:
    start1 = 0
    end1 = 0
    flag1 = False
#     print(file_cartera)
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


# In[3]:


# Tabla Diferencias. Suma por Comitente y moneda de liquidación "Dif. DÃ­a" (fila N)

#Leemos la tabla sacada arriba con pandas
file = "diferencias.csv"
df = pd.read_csv(file,skiprows=1,quoting=csv.QUOTE_NONE,delimiter=';',decimal=",")
file2 = "Productos por moneda.xlsx"
df2 = pd.read_excel(file2)
mergedStuff = pd.merge(df, df2, on=['Producto'], how='inner')
#Sumamos por comitenente y moneda
df_diferencias = mergedStuff.groupby(['Comitente','Moneda de liquidación '],as_index=False)[['Dif. Día']].sum()


# In[4]:


# Tabla Primas. Suma por Comitente y moneda de liquidación "Primas" (fila L)

file3 = "primas.csv"
df = pd.read_csv(file3,skiprows=1,quoting=csv.QUOTE_NONE,delimiter=';',decimal=",")
file2 = "Productos por moneda.xlsx"
df2 = pd.read_excel(file2)
mergedStuff = pd.merge(df, df2, on=['Producto'], how='inner')
#Sumamos por comitenente y moneda
df_primas = mergedStuff.groupby(['Comitente','Moneda de liquidación '],as_index=False)[['Primas']].sum()


# In[5]:


#Leer gvRegistryAccount.xls. Archivo de AP5
#Skipeamos 1 linea porque aune siempre tiene la 1linea vacia

file6 = file_sorted[3]
df_ap5 = pd.read_excel(file6)
df_ap5_slim = df_ap5[['Cuenta', 'Comitente CVSA']]


# In[6]:


#Leer export - 2021-07-23T152241.834.xlsx. Archivo de AUNE
#Skipeamos 1 linea porque aune siempre tiene la 1linea vacia

file4 = file_sorted[2]
df_aune = pd.read_excel(file4, skiprows=1)
#Drop la ultima fila, ya que es el total y no sirve
df_aune.drop(df_aune.tail(1).index,inplace=True)
#Extraemos el nro entre corchetes de la co Cuenta para compararla desp
df_aune['Comitente CVSA'] =  df_aune.Cuenta.str.extract('.*\[(.*)\].*')
#Pasamos CVSA a float para poder hacer el merge
df_aune["Comitente CVSA"] = pd.to_numeric(df_aune["Comitente CVSA"])
#Valor de USD Garantia ROFEX. Ver como obtenerlo automaticamente no hardcodeado
USD_Rofex = float(input("Ingrese valor USD Garantia ROFEX: "))
#Necesito el opuesto de los valores, multiplico por -1
INVERTIR_SIGNO = -1
df_aune['Aune Total Pesificado'] = df_aune['Total']*USD_Rofex*INVERTIR_SIGNO
# Solo dejamos las dos columnas que necesitamos
df_aune_slim = df_aune[['Comitente CVSA', 'Aune Total Pesificado']]
df_aune_slim


# In[7]:


#Merge Diferencias y Primas por Comitente y Moneda.
mergedStuff = pd.merge(df_diferencias, df_primas, on=['Comitente','Moneda de liquidación '], how='inner')
#Cambiamos el nombre
mergedStuff = mergedStuff.rename(columns={"Comitente": "Cuenta"})
mergedStuff


# In[8]:


#Correlacionamos los comitenes de AP5 a su numero en AUNE
mergedStuff3 = pd.merge(mergedStuff,df_ap5_slim, on=['Cuenta'], how='inner')
mergedStuff3


# In[9]:


#Separamos la tabla entre ARS y USDL
mergedStuff3_ars = mergedStuff3[mergedStuff3['Moneda de liquidación '] == 'ARS']
mergedStuff3_usdl = mergedStuff3[mergedStuff3['Moneda de liquidación '] == 'USDL']


# In[10]:


#Merge tabla de USDL coon aune-slim
mergedStuff4 = pd.merge(mergedStuff3_usdl,df_aune_slim, on=['Comitente CVSA'], how='outer')
#Llenamos los NaN con 0
mergedStuff4 = mergedStuff4.fillna(0)


# In[11]:


# Hacemos el total
mergedStuff4['Super Total'] = mergedStuff4['Dif. Día']+mergedStuff4['Primas']+mergedStuff4['Aune Total Pesificado']
mergedStuff4


# In[12]:


#Hacemos 0 los positivos del Super Total
for i in mergedStuff4.iloc[:,mergedStuff4.columns.get_loc("Super Total"):mergedStuff4.columns.get_loc("Super Total")+4]<0:
    for index, j in enumerate(mergedStuff4[i]):
        if j>0:
            mergedStuff4.at[index, i] = 0
mergedStuff4


# In[13]:


#Agarramos los ARS de Diferencias y Primas
mergedStuff3_ars = mergedStuff3_ars.rename(columns={"Dif. Día": "Dif. Día ars", "Primas": "Primas ars"})
mergedStuff3_ars
mergedStuff3_ars = mergedStuff3_ars[['Comitente CVSA', 'Dif. Día ars', 'Primas ars']]
mergedStuff3_ars


# In[14]:


#Agregamos las columnas de Dif. Día ars y Primas ars
mergedStuff5 = pd.merge(mergedStuff3_ars, mergedStuff4, on=['Comitente CVSA'], how='outer')
mergedStuff5 = mergedStuff5.fillna(0)
mergedStuff5


# In[15]:


#Sumamos a Super Total los Dif. Día ars	Primas ars
mergedStuff5['Super Total'] = mergedStuff5['Dif. Día ars'] + mergedStuff5['Primas ars'] + mergedStuff5['Super Total']

mergedStuff5


# In[24]:


#Saco columnas innecesarias
df_final = mergedStuff5[['Comitente CVSA','Super Total']]
df_final


# In[31]:


df_final= df_final[df_final !=0]
df_final = df_final.dropna()
df_final


# In[20]:


df_final.to_csv('resumen_de_cuenta.csv', sep=';',header=True, index=False, decimal=',')


# In[32]:


print("Total:",df_final['Super Total'].sum())

