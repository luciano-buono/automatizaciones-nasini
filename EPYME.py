import glob
import os
from numpy.lib.shape_base import column_stack
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'


# list_of_files = glob.glob(r"C:\Users\danyb\OneDrive\Escritorio\Python\*.xls") # * means all if need specific format then *.csv
list_of_files = glob.glob(r'*.xls') # * means all if need specific format then *.csv
latest_file = max(list_of_files, key=os.path.getmtime)

df = pd.read_excel(latest_file, converters={'CUIT':str, 'CUIT DEL COMITENTE': str,'SUBCUENTA COMITENTE': int, 'IMPORTE': float})

df['C']=1
df['D']='No garantizado'
df['E']='no'
df['F']='no'
df['K']='si'
df['L']='CVSA'
df['N']='ECHEQ'


df2 = df[['CUIT','CUIT DEL COMITENTE','C','D','E','F','SUBCUENTA COMITENTE','FECHA DE EMISION','FECHA DE PAGO','IMPORTE','K','L','ID','N']] # Armado de archivo


df2['CUIT'] = df['CUIT'].str.slice(stop=2)+'-'+df['CUIT'].str.slice(start=2)+'-'+df['CUIT'].str.slice(start=-1)
df2['CUIT DEL COMITENTE']= df['CUIT DEL COMITENTE'].str.slice(stop=2)+'-'+df['CUIT DEL COMITENTE'].str.slice(start=2)+'-'+df['CUIT DEL COMITENTE'].str.slice(start=-1)
df2['FECHA DE EMISION'] = pd.to_datetime(df2['FECHA DE EMISION']).dt.date
df2['FECHA DE PAGO'] = pd.to_datetime(df2['FECHA DE PAGO']).dt.date

df2['FECHA DE EMISION'] = pd.to_datetime(df2['FECHA DE EMISION']).dt.strftime('%d/%m/%Y')
df2['FECHA DE PAGO'] = pd.to_datetime(df2['FECHA DE PAGO']).dt.strftime('%d/%m/%Y')

columnas = ['1','2','3','4','5','6','7','8']
df2 = df2.reindex(columns =  columnas +df2.columns.tolist())


df2.to_csv('EpymeExportado.csv', sep=';',header=False, index=False) #guarda en csv

