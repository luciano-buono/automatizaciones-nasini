# %%
from cgi import print_form
import datetime
from email import header
from os import sep
import pandas as pd
import os
#Yo edito el diferido
#Creo el inmediato
current_date_1 = datetime.datetime.now().replace(microsecond=0).strftime("%Y%m%d%H%M%S")
current_date_2 = datetime.datetime.now().replace(second=0, microsecond=0).strftime("%y%m%d")
current_date_3 = datetime.datetime.now().replace(second=0, microsecond=0).strftime("%d%m")

def create_CompraInmediata(df):
    amount_lines = len(df.index)
    with open('inmediata-edit.txt', 'w') as outfile:
        outfile.write(f"00Aftfaot{current_date_1:>18}{amount_lines+1:09d}\n")
        outfile.write(f"0{current_date_2}FTFAOT0062\n")
        for idx in df.index:
            especie = df["Especie"][idx]
            cant = df["Cantidad"][idx]
            comitente = df["Comitente"][idx]
            outfile.write(f"1'I'E'7062'000010000'{especie:05}       '{cant:{' '}>{13}}000000'0062'{comitente:09}'N'00'{current_date_3}'    'N\n")
        outfile.write(f"99Aftfaot{current_date_1:>18}{amount_lines+1:09d}\n")
        
    WINDOWS_LINE_ENDING = b'\r\n'
    UNIX_LINE_ENDING = b'\n'
    with open('inmediata-edit.txt', 'rb') as open_file:
        content = open_file.read()
    content = content.replace(UNIX_LINE_ENDING,WINDOWS_LINE_ENDING)

    with open('inmediata-edit.txt', 'wb') as open_file:
        open_file.write(content)

# %%
def read_excel(file):
    dtypes = {
        "Comitente": "int",
        "Especie": "int",
        "Cantidad": "float",
        "Diferido": "float",
        "Compra total": "float",
    }
    df = pd.read_excel(file,dtype=dtypes)
    return df
def main():
    df_excel = read_excel(file='ADELANTOS.xlsx')
    create_CompraInmediata(df_excel)
    # edit_CompraDifererida(df_excel)

if __name__ == "__main__":
    main()

# %%
df_excel = read_excel(file='ADELANTOS.xlsx')
df_excel.info()

# %%
with open('diferida.txt', 'r') as infile:
    headers = [
        "0",
        "1",
        "2",
        "3",
        "4",
        "Especie",
        "Cantidad",
        "7",
        "Comitente",
        "9",
        "10",
        "11",
        "12",
        "13",
    ]
    dtypes = {
        "0": "str",
        "1": "str",
        "2": "str",
        "3": "str",
        "4": "str",
        "Especie": "int",
        "Cantidad": "float",
        "7": "str",
        "Comitente": "int",
        "9": "str",
        "10": "str",
        "11": "str",
        "12": "str",
        "13": "str",
    }
    df = pd.read_csv(infile, sep= "'", header=None, names=headers, skiprows=2, skipfooter=1, dtype=dtypes)


# %%
df_merge = pd.merge(df, df_excel, on=['Comitente',"Especie"], how='outer')

# %%
df_merge

# %%
#If NAN dropeo row (drop donde no hay match de comitente)
df_merge = df_merge[df_merge['Cantidad_x'].notna()]


# %%
df_merge

# %%
#if diferido=0 dropeo row
df_merge = df_merge[df_merge['Diferido']!=0]
df_merge

# %%
import math
df_merge["Cantidad_x"] = df_merge.apply(lambda x: x["Diferido"] if not math.isnan(x["Diferido"]) else x["Cantidad_x"], axis=1 ) #df_merge[df_merge["Cantidad_x"]:df_merge["Diferido"].notna()]

# %%
df_merge

# %%
df_merge2 = df_merge[[
            "0",
            "1",
            "2",
            "3",
            "4",
            "Especie",
            "Cantidad_x",
            "7",
            "Comitente",
            "9",
            "10",
            "11",
            "12",
            "13",
        ]]
df_merge2

# %%
outfile = "diferida-edit1.txt"
df_merge2.to_csv(outfile,sep="'",header=None, index=False)

# %%
amount_lines = len(df_merge.index)
with open('diferida-edit1.txt','r') as infile, open('diferida-edit.txt', 'w') as outfile:
    save = infile.read()
    
    outfile.write(f"00Aftfaot{current_date_1:>18}{amount_lines+1:09d}\n")
    outfile.write(f"0{current_date_2}FTFAOT0062\n")
    outfile.write(save)
    outfile.write(f"99Aftfaot{current_date_1:>18}0000000{amount_lines+1:09d}\n")

WINDOWS_LINE_ENDING = b'\r\n'
UNIX_LINE_ENDING = b'\n'
with open('diferida-edit.txt', 'rb') as open_file:
    content = open_file.read()
content = content.replace(UNIX_LINE_ENDING,WINDOWS_LINE_ENDING)

with open('diferida-edit.txt', 'wb') as open_file:
    open_file.write(content)
os.remove("diferida-edit1.txt")


