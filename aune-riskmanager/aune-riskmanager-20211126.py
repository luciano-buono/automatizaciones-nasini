#!/usr/bin/env python
# coding: utf-8

# In[11]:


#DESCRIPCION
# Trabajo en pandas para facilitar 
# la suma de primas diferencias de riskmanager y datos de aune

##IMPORTS
from argparse import ArgumentParser
import csv
import os, glob, sys
import pandas as pd
from pathlib import Path


# In[12]:


def load_files():
    EXTENSIONS_ALLOWED = ['*.xls','*.xlsx','*.csv']
    files_grabbed = []
    for files in EXTENSIONS_ALLOWED:
        files_grabbed.extend(glob.glob(files))
    return files_grabbed

def select_file(files, keyword):
    for f in files:
        if keyword in f:
            return f
    return None
def process_aune(file, output_file, keyword):
    if not file:
        return "File not found"
    with open(f"{file}", 'r', newline='') as f,     open(f"{output_file}.csv", 'w', newline='') as output_file:
        reader = csv.reader(f, delimiter=';')
        writer = csv.writer(output_file, delimiter= ';')
        flag = False
        print(file,reader)
        for row in reader:
            if keyword in row:
                flag = True
            if flag:
                writer.writerow(row)
                if not row:
                    break



# In[13]:


def diferencias(file,file2):
    # Tabla Diferencias. Suma por Comitente y moneda de liquidación "Dif. DÃ­a" (fila N)
    #Leemos la tabla sacada arriba con pandas
    if (not file) or (not file2):
        return "File not found"
    df = pd.read_csv(file,skiprows=1,quoting=csv.QUOTE_NONE,delimiter=';',decimal=",")
    df2 = pd.read_excel(file2)
    mergedStuff = pd.merge(df, df2, on=['Producto'], how='inner')
    #Sumamos por comitenente y moneda
    df_diferencias = mergedStuff.groupby(['Comitente','Moneda de liquidación '],as_index=False)[['Dif. Día']].sum()
    return df_diferencias

def primas(file,file2):
    # Tabla Primas. Suma por Comitente y moneda de liquidación "Dif. DÃ­a" (fila N)
    #Leemos la tabla sacada arriba con pandas
    if (not file) or (not file2):
        return "File not found"
    df = pd.read_csv(file,skiprows=1,quoting=csv.QUOTE_NONE,delimiter=';',decimal=",")
    df2 = pd.read_excel(file2)
    mergedStuff = pd.merge(df, df2, on=['Producto'], how='inner')
    #Sumamos por comitenente y moneda
    df_primas = mergedStuff.groupby(['Comitente','Moneda de liquidación '],as_index=False)[['Primas Día']].sum()
    return df_primas


# In[21]:


def gvRegistryAccount(file):
    #Leer gvRegistryAccount.xls. Archivo de AP5
    #Skipeamos 1 linea porque aune siempre tiene la 1linea vacia
    if (not file):
        return "File not found"
    df = pd.read_excel(file)
    df = df[df["Estado"]=="Activo"]
    df = df[['Cuenta', 'Comitente CVSA']]
    return df


# In[22]:


def aune(file):
    if (not file):
        return "File not found"
    df_aune = pd.read_excel(file, skiprows=1)
    #Drop la ultima fila, ya que es el total y no sirve
    df_aune.drop(df_aune.tail(1).index,inplace=True)
    #Extraemos el nro entre corchetes de la co Cuenta para compararla desp
    df_aune['Comitente CVSA'] =  df_aune.Cuenta.str.extract('.*\[(.*)\].*')
    #Pasamos CVSA a float para poder hacer el merge
    df_aune["Comitente CVSA"] = pd.to_numeric(df_aune["Comitente CVSA"])
    #Valor de USD Garantia ROFEX. Ver como obtenerlo automaticamente no hardcodeado
    USD_Rofex = float(input("Ingrese valor USD Garantia ROFEX"))
    #Necesito el opuesto de los valores, multiplico por -1
    INVERTIR_SIGNO = -1
    df_aune['Aune Total Pesificado'] = df_aune['Total']*USD_Rofex*INVERTIR_SIGNO
    # Solo dejamos las dos columnas que necesitamos
    df_aune_slim = df_aune[['Comitente CVSA', 'Aune Total Pesificado']]
    return df_aune_slim


# In[19]:


def mergeDFs(df_diferencias,df_primas,gvRegistryAccount, df_aune):
    #Merge Diferencias y Primas por Comitente y Moneda.
    mergedStuff = pd.merge(df_diferencias, df_primas, on=['Comitente','Moneda de liquidación '], how='inner')
    #Cambiamos el nombre
    mergedStuff = mergedStuff.rename(columns={"Comitente": "Cuenta"})
    
    #Correlacionamos los comitenes de AP5 a su numero en AUNE
    mergedStuff3 = pd.merge(mergedStuff,gvRegistryAccount, on=['Cuenta'], how='inner')
    
    #Separamos la tabla entre ARS y USDL
    mergedStuff3_ars = mergedStuff3[mergedStuff3['Moneda de liquidación '] == 'ARS']
    mergedStuff3_usdl = mergedStuff3[mergedStuff3['Moneda de liquidación '] == 'USDL']
    
    #Merge tabla de USDL coon aune-slim
    mergedStuff4 = pd.merge(mergedStuff3_usdl,df_aune, on=['Comitente CVSA'], how='outer')
    #Llenamos los NaN con 0
    mergedStuff4 = mergedStuff4.fillna(0)
    
    # Hacemos el total
    mergedStuff4['Super Total'] = mergedStuff4['Dif. Día']+mergedStuff4['Primas Día']+mergedStuff4['Aune Total Pesificado']
    mergedStuff4
    
    #Hacemos 0 los positivos del Super Total
    for i in mergedStuff4.iloc[:,mergedStuff4.columns.get_loc("Super Total"):mergedStuff4.columns.get_loc("Super Total")+4]<0:
        for index, j in enumerate(mergedStuff4[i]):
            if j>0:
                mergedStuff4.at[index, i] = 0
    mergedStuff4
    
    #Agarramos los ARS de Diferencias y Primas
    mergedStuff3_ars = mergedStuff3_ars.rename(columns={"Dif. Día": "Dif. Día ars", "Primas Día": "Primas ars"})
    mergedStuff3_ars
    mergedStuff3_ars = mergedStuff3_ars[['Comitente CVSA', 'Dif. Día ars', 'Primas ars']]
    mergedStuff3_ars
    
    #Agregamos las columnas de Dif. Día ars y Primas ars
    mergedStuff5 = pd.merge(mergedStuff3_ars, mergedStuff4, on=['Comitente CVSA'], how='outer')
    mergedStuff5 = mergedStuff5.fillna(0)
    mergedStuff5
    
    #Sumamos a Super Total los Dif. Día ars	Primas ars
    mergedStuff5['Super Total'] = mergedStuff5['Dif. Día ars'] + mergedStuff5['Primas ars'] + mergedStuff5['Super Total']
    mergedStuff5
    
    #Saco columnas innecesarias
    df_final = mergedStuff5[['Comitente CVSA','Super Total']]
    df_final= df_final[df_final !=0]
    df_final = df_final.dropna()
    return df_final


# In[17]:


def remove_GELD(df_final):
    #Eliminar los comitentes de GELD de df_final
    # AUNE	Codigo Cuenta
    COMITENTES_GELD= [10187,10188,10195,10196,10122,10305,10121,10123]
    df_final_bool =df_final.isin({'Comitente CVSA': COMITENTES_GELD})
    REMOVE_GELD = df_final_bool.index[df_final_bool["Comitente CVSA"]].tolist()
    df_final = df_final.drop(REMOVE_GELD)
    df_final.to_csv('resumen_de_cuenta.csv', sep=';',header=True, index=False, decimal=',')
    print("Total:",df_final['Super Total'].sum())
    return df_final


# In[23]:


files = load_files()
print(files)
process_aune(select_file(files, 'Cartera'),"diferencias","Listado de Productos con Interes Abierto, discriminado por comitente")   
process_aune(select_file(files, 'Cartera'),"primas","Listado de Productos con Interes Abierto, discriminado por comitente")    
df_diferencias = diferencias(select_file(files, 'diferencias'),select_file(files, 'Productos por moneda'))
df_primas = primas(select_file(files, 'primas'),select_file(files, 'Productos por moneda'))
gvRegistryAccount = gvRegistryAccount(select_file(files, 'gvRegistry'))
df_aune = aune(select_file(files, 'export'))
df_final = mergeDFs(df_diferencias,df_primas,gvRegistryAccount, df_aune)
remove_GELD(df_final)

