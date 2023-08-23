from flask import Flask, request, jsonify
from openpyxl import load_workbook
from openpyxl.formula.translate import Translator
from openpyxl.utils import get_column_letter
from openpyxl.utils import FORMULAE

import pandas as pd
import csv
import json
import os

app = Flask(__name__)

# Direccion archivos
listadosTemporales = 'Repo-Python-DB-DottAPI\\archivosPorCargar\\temporales\\'
listadoCsv = 'Repo-Python-DB-DottAPI\\archivosPorCargar\\csv\\'
listadoJson = 'Repo-Python-DB-DottAPI\\archivosPorCargar\\archivosJson\\'
diccionarios = 'Repo-Python-DB-DottAPI\\nuevosScripts\\diccionarios\\diccionarios.json'

# Función para encontrar un valor en el dicc¶ionario


def encontrar_valor(diccionario, clave):
    if clave in diccionario:
        return diccionario[clave]
    else:
        return "No existe una categoría para este producto"

# Función para obtener un diccionario


def obtenerDiccionario(nombreDiccionario):
    with open(diccionarios) as diccionariosOpen:
        diccionariosJson = json.load(diccionariosOpen)
    diccionarioBuscado = diccionariosJson[nombreDiccionario]
    return diccionarioBuscado


@app.route('/procesar_archivo_air', methods=['POST'])
def procesar_archivo_air():

    archivo = request.files['file']

    if archivo.filename == '':
        return jsonify({'error': 'No se ha seleccionado un archivo'}), 400

    # Guardar el archivo temporalmente
    archivo.save(listadosTemporales+"air.csv")

    # Función para crear el archivo JSON
    def crearArchivoJson():
        data = []
        with open(listadosTemporales+"air.csv", 'r') as file:
            csv_reader = csv.reader(file, delimiter=',')
            next(csv_reader)  # Ignora la primera fila de encabezados
            for row in csv_reader:
                if row[2] != "A":
                    descripcion = row[1]
                    rubro = row[10]
                    iva = row[4]
                    precio = row[2]
                    registro = {
                        'proveedor': 'air',
                        'producto': descripcion,
                        'categoria': encontrar_valor(obtenerDiccionario('air'), rubro),
                        'precio': round((float(precio) * (1 + (float(iva) / 100)) * 1.1))
                    }
                    data.append(registro)

        with open(listadoJson+"air.json", 'w') as jf:
            json.dump(data, jf, ensure_ascii=False, indent=2)

    # Ejecutar el proceso de creación del JSON
    crearArchivoJson()

    return jsonify({'message': 'Archivo CSV procesado y JSON creado correctamente'})


@app.route('/procesar_archivo_eikon', methods=['POST'])
def procesar_archivo_eikon():

    archivo = request.files['file']

    if archivo.filename == '':
        return jsonify({'error': 'No se ha seleccionado un archivo'}), 400

    # Guardar el archivo temporalmente
    archivo.save(listadosTemporales+'temp_eikon.xlsx')

    # Resto del proceso para procesar archivos Eikon
    df = pd.read_excel(listadosTemporales+'temp_eikon.xlsx')
    # Se utilizan los índices 0, 1 y 2 para las primeras tres filas
    df = df.drop([0, 1, 2])
    df.reset_index(drop=True, inplace=True)
    # Guardar como CSV
    df.to_csv(listadoCsv+'listadoEik.csv', index=False)

    with open(listadoCsv+'listadoEik.csv', 'r') as file:
        # Crea un objeto lector CSV
        csv_reader = csv.reader(file, delimiter=',')

        # Crea una lista para almacenar los datos
        data = []

        next(csv_reader)  # Ignora la primera fila de encabezados
        for row in csv_reader:

            descripcion = row[1]
            categoria = row[6]
            precio = row[3]

            # Crea un diccionario con los datos de cada registro
            registro = {
                'proveedor': 'eikon',
                'producto': descripcion,
                'categoria': encontrar_valor(obtenerDiccionario('eikon'), categoria),
                'precio': round((float(precio) * 1.1))
            }

            # Agrega el diccionario a la lista de datos
            data.append(registro)

    # Convierte la lista de datos a formato JSON
    # json_data = json.dumps(data, indent=4)

    with open(listadoJson+'listadoEik.json', 'w') as jf:
        json.dump(data, jf, ensure_ascii=False, indent=2)

    return jsonify({'message': 'Archivo Eikon procesado correctamente'})


@app.route('/procesar_archivo_elit', methods=['POST'])
def procesar_archivo_elit():

    archivo = request.files['file']

    if archivo.filename == '':
        return jsonify({'error': 'No se ha seleccionado un archivo'}), 400

    # Guardar el archivo temporalmente
    archivo.save(listadosTemporales+'temp_elit.xlsx')

    # Resto del proceso para procesar archivos Eikon
    df = pd.read_excel(listadosTemporales+'temp_elit.xlsx')

    df.to_csv(listadoCsv+'listadoElit.csv', index=False)

    # Abre el archivo CSV en modo lectura con la codificación adecuada
    with open(listadoCsv+'listadoElit.csv', 'r') as file:
        # Crea un objeto lector CSV
        csv_reader = csv.reader(file, delimiter=',')

        # Crea una lista para almacenar los datos
        data = []

        # Lee cada fila del archivo CSV (ignorando la primera fila de encabezados)

        next(csv_reader)  # Ignora la primera fila de encabezados
        for row in csv_reader:
            descripcion = row[1]
            categoria = row[5]
            precio = row[7]
            iva = row[8]
            ivaInterno = row[9]

            # Crea un diccionario con los datos de cada registro
            registro = {
                'proveedor': 'elit',
                'producto': descripcion,
                'categoria': encontrar_valor(obtenerDiccionario('elit'), categoria),
                'precio': round((float(precio) * (1 + (float(iva) + float(ivaInterno))/100) * 1.1))
            }

            # Agrega el diccionario a la lista de datos
            data.append(registro)

    with open(listadoJson+'listadoElit.json', 'w') as jf:
        json.dump(data, jf, ensure_ascii=False, indent=2)

    return jsonify({'message': 'Archivo Elit procesado correctamente'})


@app.route('/procesar_archivo_hdc', methods=['POST'])
def procesar_archivo_hdc():

    def obtenerTipoIva(clave):
        # Diccionario con tipo de IVA
        tipoIva = {
            "002-I.V.A. 10.5 %": 10.5,
            "001-I.V.A. 21 %": 21,
            "005-Impuestos Internos": 21
        }
        if clave in tipoIva:
            return tipoIva[clave]

    archivo = request.files['file']

    if archivo.filename == '':
        return jsonify({'error': 'No se ha seleccionado un archivo'}), 400

    # Guardar el archivo temporalmente
    archivo.save(listadosTemporales+'temp_hdc.xlsx')

    # Resto del proceso para procesar archivos Eikon
    df = pd.read_excel(listadosTemporales+'temp_hdc.xlsx')

    df.to_csv(listadoCsv+'listadoHdc.csv', index=False)

    # Abre el archivo CSV en modo lectura con la codificación adecuada
    with open(listadoCsv+'listadoHdc.csv', 'r', encoding="utf-8") as file:
        # Crea un objeto lector CSV
        csv_reader = csv.reader(file, delimiter=',')

        # Crea una lista para almacenar los datos
        data = []

        # Lee cada fila del archivo CSV (ignorando la primera fila de encabezados)

        next(csv_reader)  # Ignora la primera fila de encabezados

        for row in csv_reader:
            if row[7]:
                descripcion = row[5]
                if row[3]:
                    categoria = row[3]
                else:
                    categoria = row[2]
                precio = row[7]
                iva = obtenerTipoIva(row[8])

                # Crea un diccionario con los datos de cada registro
                registro = {
                    "proveedor": "hdc",
                    'producto': descripcion,
                    'categoria': encontrar_valor(obtenerDiccionario('hdc'), categoria),
                    'precio': round(float(precio) * (1+float(iva)/100) * 1.1)
                }

                # Agrega el diccionario a la lista de datos
                data.append(registro)

    with open(listadoJson+'listadoHdc.json', 'w') as jf:
        json.dump(data, jf, ensure_ascii=False, indent=2)

    return jsonify({'message': 'Archivo HDC procesado correctamente'})


@app.route('/procesar_archivo_invid', methods=['POST'])
def procesar_archivo_invid():

    archivo = request.files['file']

    if archivo.filename == '':
        return jsonify({'error': 'No se ha seleccionado un archivo'}), 400

    # Guardar el archivo .xls en el directorio
    archivo.save(listadosTemporales + 'temp_invid.xlsx')

    df = pd.read_excel(listadosTemporales+'temp_invid.xlsx')

    # Se utilizan los índices 0, 1 y 2 para las primeras tres filas
    df = df.drop([0, 1, 2, 3, 4, 5, 6, 7, 8])
    df.reset_index(drop=True, inplace=True)
    df.to_excel(listadosTemporales + 'temp_invid.xlsx', index=False)

    # Cargar el libro de trabajo
    book = load_workbook(listadosTemporales + 'temp_invid.xlsx')
    sheet = book.active
    # Cambia esta fórmula según tus necesidades

    sheet['I3'] = "categoria"
    # # Define la fórmula
    # formula = '=IF(LEN(H4)<2,"",IF(AND(LEN(A2)<2,LEN(C2)<2),B2,I3))'
    # # Obtén la letra de la columna 'I'
    # column_letter = get_column_letter(9)  # 9 es el número de la columna 'I'

    # # Aplica la fórmula en las celdas de la columna 'I' (desde la fila 5 en adelante)
    # for row_num in range(4, sheet.max_row + 1):
    #     formula = f'=IF(LEN(H{row_num})<2,"",IF(AND(LEN(A{row_num-2})<2,LEN(C{row_num-2})<2),B{row_num-2},{column_letter}{row_num-1}))'
    #     cell_reference = f'{column_letter}{row_num}'
    #     sheet[cell_reference] = formula

    def transform_formula(h_value, a_value, c_value, b_value, i_value):
        if h_value is None:
            return ""
        if len(h_value) < 2:
            return ""
        if a_value is None or c_value is None:
            return ""
        if len(a_value) < 2 and len(c_value) < 2:
            return b_value
        return i_value

    # Iterar a través de las filas de la columna "I"
    # Suponiendo que tus datos comienzan desde la fila 2 y hay 9 columnas
    for fila in sheet.iter_rows(min_row=2, max_col=9, max_row=sheet.max_row):
        h3 = fila[7].value  # Columna H
        a1 = fila[0].value  # Columna A
        c1 = fila[2].value  # Columna C
        b1 = fila[1].value  # Columna B
        i1 = fila[8].value  # Columna I

        resultado = transform_formula(h3, a1, c1, b1, i1)

        # Asignar el resultado a la columna I en la misma fila
        # Si el resultado es una cadena vacía, asignar None
        fila[8].value = resultado if resultado != "" else None

    # Crea una lista para almacenar los datos de las celdas
    book.save(listadosTemporales + 'temp_invid_test.xlsx')

    # Guardar como CSV
    df.to_csv(listadoCsv+'listadoInvid.csv', index=False)

    with open(listadoCsv+'listadoInvid.csv', 'r') as file:
        # Crea un objeto lector CSV
        csv_reader = csv.reader(file, delimiter=',')

        # Crea una lista para almacenar los datos
        data = []

        # Lee cada fila del archivo CSV (ignorando la primera fila de encabezados)

        next(csv_reader)  # Ignora la primera fila de encabezados
        for row in csv_reader:
            if (row[3] != "" and row[3] != "Nro. de Parte"):
                descripcion = row[1]
                categoria = row[8]
                precio = float(row[5])
                iva = (1 + (float(row[6])/100)) * (1 + (float(row[7])/100))

                # Crea un diccionario con los datos de cada registro
                registro = {
                    'proveedor': "invid",
                    'producto': descripcion,
                    'categoria': encontrar_valor(obtenerDiccionario('invid'), categoria),
                    'precio': round((precio * iva * 1.1))
                }

                # Agrega el diccionario a la lista de datos

                data.append(registro)

    with open(listadoJson+'listadoInvid.json', 'w') as jf:
        json.dump(data, jf, ensure_ascii=False, indent=2)

    return jsonify({'message': 'Archivo invid procesado correctamente'})


if __name__ == '__main__':
    app.run(debug=True)
