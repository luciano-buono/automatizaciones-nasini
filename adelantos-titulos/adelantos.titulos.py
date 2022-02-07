from cgi import print_form
import datetime
from email import header
from os import sep
import pandas as pd

current_date_with_our = datetime.datetime.now().replace(microsecond=0).strftime("%Y%m%d%H%M%S")
current_date = datetime.datetime.now().replace(second=0, microsecond=0).strftime("%Y%m%d")
current_date_day_month = datetime.datetime.now().replace(second=0, microsecond=0).strftime("%m%d")
print(current_date_with_our)

def create_CompraInmediata(df):
    amount_lines = len(df.index)

    with open('ComprasInmediata.txt', 'w') as outfile:
        outfile.write(f"00Aftfaot    {current_date}0000000{amount_lines+1}\n")
        outfile.write(f"0{current_date_day_month}FTFAOT0062\n")
        for idx in df.index:
            especie = df["Especie"][idx]
            cant = df["Cantidad"][idx]
            comitente = df["Comitente"][idx]
            outfile.write(f"1'I'E'7062'000010000'{especie:{' '}<{5}}       '       {cant:{' '}>{10}}'0062'0000{comitente:{' '}>{5}}'N'00'{current_date_day_month}'{current_date_day_month}'N\n")
        outfile.write(f"00Aftfaot    {current_date}0000000{amount_lines+1}\n")

def edit_CompraDifererida(df_excel):
    with open('compras diferidas 04-02.txt', 'r') as infile, open('compras diferidas 04-02-edited.txt', 'w') as outfile:
        df = pd.read_csv(infile, sep= "'", header=None, skiprows=2, skipfooter=1)
        #5 especie #6cant #8comitente
        # print(df)
        comitentes = list(df[8])
        # print(comitentes)
        a = df[8].isin(list(df_excel["Comitente"]))
        # print(a)
        df1 = df
        df1["isin"] = df[8].isin(list(df_excel["Comitente"]))
        print(df1)

def read_excel(file):
    df = pd.read_excel(file)
    return df
    

def main():
    df = read_excel(file='adel.xlsx')
    create_CompraInmediata(df)
    edit_CompraDifererida(df)

if __name__ == "__main__":
    main()