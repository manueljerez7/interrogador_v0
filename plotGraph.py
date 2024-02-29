import pandas as pd
import matplotlib.pyplot as plt
from zipfile import ZipFile
import os

def plotGraph(archivo_zip, nombre_csv, indice_columna):
    # Descomprime el archivo zip
    with ZipFile(archivo_zip, 'r') as zip_ref:
        zip_ref.extractall()

    # Lee el archivo CSV con pandas sin nombres de columnas
    df = pd.read_csv(nombre_csv, header=None)

    # Extrae la columna especificada por índice
    columna_data = df.iloc[:, indice_columna]

    # Crea la gráfica con matplotlib
    plt.plot(columna_data)
    plt.xlabel('Numero de muestra')
    plt.ylabel(f'Temperatura [ºC]')
    plt.title(f'Temperatura')
    plt.show()

    # Borra todos los archivos CSV al final de la ejecución
    archivos_csv = [archivo for archivo in os.listdir() if archivo.endswith(".csv")]
    for archivo_csv in archivos_csv:
        os.remove(archivo_csv)
