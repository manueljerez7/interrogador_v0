import zipfile
import os

def zip(nombre_zip,archivos_a_zippear):
    # Crear el archivo zip
    with zipfile.ZipFile(nombre_zip, 'w') as zip_file:
        for archivo in archivos_a_zippear:
            # Añadir cada archivo al zip
            zip_file.write(archivo)

    # Eliminar los archivos originales después de crear el zip
    for archivo in archivos_a_zippear:
        os.remove(archivo)

    print(f'Archivos zipeados y eliminados. Archivo zip: {nombre_zip}')