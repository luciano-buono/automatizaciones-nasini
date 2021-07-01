import glob
import os,sys
from numpy.lib.shape_base import column_stack
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

#TODO

##

#usa el ultimo archivo modificado como entrada
#Lee tantos xls como xlsx
name_of_file = '*.xls*'
try:
    list_of_files = glob.glob(name_of_file)
    file = max(list_of_files, key=os.path.getmtime)
    print(f"Leyendo archivo: {file} ")
except ValueError as err:
    print(f"ERROR No hay {name_of_file} en el directorio actual ({os.getcwdb()})")
    sys.exit(1)


df = pd.read_excel(file, converters={'CUIT':str, 'CUIT DEL COMITENTE': str,'SUBCUENTA COMITENTE': int, 'IMPORTE': float})

df['C']=1
df['D']='No garantizado'
df['E']='no'
df['F']='no'
df['K']='si'
df['L']='CVSA'
df['N']='ECHEQ'


df2 = df[['CUIT','CUIT DEL COMITENTE','C','D','E','F','SUBCUENTA COMITENTE','FECHA DE EMISION','FECHA DE PAGO','IMPORTE','K','L','ID','N']] # Armado de archivo

#Formato de ciut xx-xxxxx-x
df2['CUIT'] = df['CUIT'].str.slice(stop=2)+'-'+df['CUIT'].str.slice(start=2, stop=-1)+'-'+df['CUIT'].str.slice(start=-1)
df2['CUIT DEL COMITENTE']= df['CUIT DEL COMITENTE'].str.slice(stop=2)+'-'+df['CUIT DEL COMITENTE'].str.slice(start=2, stop=-1)+'-'+df['CUIT DEL COMITENTE'].str.slice(start=-1)
# Pasamos las fechas al formato d/m/a
df2['FECHA DE EMISION'] = pd.to_datetime(df2['FECHA DE EMISION'], dayfirst=True).dt.date
df2['FECHA DE PAGO'] = pd.to_datetime(df2['FECHA DE PAGO'], dayfirst=True).dt.date
df2['FECHA DE EMISION'] = pd.to_datetime(df2['FECHA DE EMISION']).dt.strftime('%d/%m/%Y')
df2['FECHA DE PAGO'] = pd.to_datetime(df2['FECHA DE PAGO']).dt.strftime('%d/%m/%Y')
#Agregamos columnas vacias al iniciio
columnas = ['1','2','3','4','5','6','7','8']
df2 = df2.reindex(columns =  columnas +df2.columns.tolist())

#Guardamos el csv
df2.to_csv('EpymeExportado.csv', sep=';',header=False, index=False, decimal=',') #guarda en csv