# Tabla Diferencias. Suma por Comitente y moneda de liquidación "Dif. DÃ­a" (fila N)

#Leemos la tabla sacada arriba con pandas
diferencia = "diferencias.csv"
df = pd.read_csv(diferencia,skiprows=1,quoting=csv.QUOTE_NONE,delimiter=';',decimal=",")
moneda = "Productos por moneda.xlsx"
df2 = pd.read_excel(moneda)
mergedStuff = pd.merge(df, df2, on=['Producto'], how='inner')
#Sumamos por comitenente y moneda
df_diferencias = mergedStuff.groupby(['Comitente','Moneda de liquidación '],as_index=False)[['Dif. Día']].sum()

# Tabla Primas. Suma por Comitente y moneda de liquidación "Primas" (fila L)

primas = "primas.csv"
df = pd.read_csv(primas,skiprows=1,quoting=csv.QUOTE_NONE,delimiter=';',decimal=",")
df2 = pd.read_excel(moneda)
mergedStuff = pd.merge(df, df2, on=['Producto'], how='inner')
#Sumamos por comitenente y moneda
df_primas = mergedStuff.groupby(['Comitente','Moneda de liquidación '],as_index=False)[['Primas']].sum()

#Leer gvRegistryAccount.xls. Archivo de AP5
#Skipeamos 1 linea porque aune siempre tiene la 1linea vacia

file6 = "gvRegistryAccount.xls"
df_ap5 = pd.read_excel(file6)
df_ap5_slim = df_ap5[['Cuenta', 'Comitente CVSA']]

#Leer export - 2021-07-23T152241.834.xlsx. Archivo de AUNE
#Skipeamos 1 linea porque aune siempre tiene la 1linea vacia

file_aune = file[2]
df_aune = pd.read_excel(file_aune, skiprows=1)
#Drop la ultima fila, ya que es el total y no sirve
df_aune.drop(df_aune.tail(1).index,inplace=True)
#Extraemos el nro entre corchetes de la co Cuenta para compararla desp
df_aune['Comitente CVSA'] =  df_aune.Cuenta.str.extract('.*\[(.*)\].*')
#Pasamos CVSA a float para poder hacer el merge
df_aune["Comitente CVSA"] = pd.to_numeric(df_aune["Comitente CVSA"])
#Valor de USD Garantia ROFEX. Ver como obtenerlo automaticamente no hardcodeado
USD_Rofex = 96.5900
df_aune['Aune Total Pesificado'] = df_aune['Total']*USD_Rofex
# Solo dejamos las dos columnas que necesitamos
df_aune_slim = df_aune[['Comitente CVSA', 'Aune Total Pesificado']]
df_aune_slim


#Merge Diferencias y Primas por Comitente y Moneda.
mergedStuff = pd.merge(df_diferencias, df_primas, on=['Comitente','Moneda de liquidación '], how='inner')
#Cambiamos el nombre
mergedStuff = mergedStuff.rename(columns={"Comitente": "Cuenta"})
mergedStuff

#Correlacionamos los comitenes de AP5 a su numero en AUNE
mergedStuff3 = pd.merge(mergedStuff,df_ap5_slim, on=['Cuenta'], how='inner')
mergedStuff3


#Separamos la tabla entre ARS y USDL
mergedStuff3_ars = mergedStuff3[mergedStuff3['Moneda de liquidación '] == 'ARS']
mergedStuff3_usdl = mergedStuff3[mergedStuff3['Moneda de liquidación '] == 'USDL']


#Merge tabla de USDL coon aune-slim
mergedStuff4 = pd.merge(mergedStuff3_usdl,df_aune_slim, on=['Comitente CVSA'], how='outer')
#Llenamos los NaN con 0
mergedStuff4 = mergedStuff4.fillna(0)


# Hacemos el total
mergedStuff4['Super Total'] = mergedStuff4['Dif. Día']+mergedStuff4['Primas']+mergedStuff4['Aune Total Pesificado']
mergedStuff4


#Hacemos 0 los positivos del Super Total
for i in mergedStuff4.iloc[:,mergedStuff4.columns.get_loc("Super Total"):mergedStuff4.columns.get_loc("Super Total")+4]<0:
    for index, j in enumerate(mergedStuff4[i]):
        if j>0:
            mergedStuff4.at[index, i] = 0
mergedStuff4


#Agarramos los ARS de Diferencias y Primas
mergedStuff3_ars = mergedStuff3_ars.rename(columns={"Dif. Día": "Dif. Día ars", "Primas": "Primas ars"})
mergedStuff3_ars = mergedStuff3_ars[['Comitente CVSA', 'Dif. Día ars', 'Primas ars']]
mergedStuff3_ars


#Sumamos los ARS en Dif dia Y primas
mergedStuff5 = pd.merge(mergedStuff3_ars, mergedStuff4, on=['Comitente CVSA'], how='outer')
mergedStuff5 = mergedStuff5.fillna(0)
mergedStuff5


#Sumamos a Super Total los Dif. Día ars	Primas ars
mergedStuff5['Super Total'] = mergedStuff5['Dif. Día ars'] + mergedStuff5['Primas ars'] + mergedStuff5['Super Total']

mergedStuff5


df_final = mergedStuff5[['Comitente CVSA','Super Total']]
df_final



df_final['Super Total'].sum()