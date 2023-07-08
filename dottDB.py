import json
import pandas as pd
import sqlite3


#Direccion Windows
listadosJson = {
    "air": "Repo-Python-DB-DottAPI/nuevosScripts/Air/Json/listadoAir.json",
    "eikon": "Repo-Python-DB-DottAPI/nuevosScripts/Eik/Json/listadoJson.json",
    "elit": "Repo-Python-DB-DottAPI/nuevosScripts/Elit/Json/listadoJson.json",
    "nb":"Repo-Python-DB-DottAPI/nuevosScripts/Nb/Json/listadoJson.json",
}

direccionAchivosJson = {
    "jsonDolar": "Repo-Python-DB-DottAPI/dataDolar.json",
    "direccionDB":"Repo-Python-DB-DottAPI/productosDB.sqlite"
}

# Lectura del archivo JSON
with open(listadosJson["air"]) as f:
    listadoAir = json.load(f)

    
with open(listadosJson["eikon"]) as f:
    listadoEik = json.load(f)

with open(listadosJson["elit"]) as f:
    listadoElit = json.load(f)

with open(listadosJson["nb"]) as f:
    listadoNb = json.load(f)

listaProductos = listadoAir + listadoEik + listadoElit + listadoNb


# Nombre de la tabla en la base de datos SQLite
nombre_tabla = 'Productos'
nombre_tabla_2 = 'Dolares'

# Conexión a la base de datos SQLite
conexion = sqlite3.connect(direccionAchivosJson['direccionDB'])

# Creación de la tabla en la base de datos SQLite
cursor = conexion.cursor()
cursor.execute(f'DROP TABLE IF EXISTS {nombre_tabla}')
cursor.execute(f'CREATE TABLE {nombre_tabla} (id integer PRIMARY KEY AUTOINCREMENT, proveedor text, producto text, categoria text, precio float)')
cursor.execute(f'DROP TABLE IF EXISTS {nombre_tabla_2}')
cursor.execute(f'CREATE TABLE {nombre_tabla_2} (id integer PRIMARY KEY AUTOINCREMENT, precioDolar float, precioTarjeta float)')


with open(direccionAchivosJson['jsonDolar']) as g:
    datos_dolar = json.load(g)

# Almacenamiento de los datos en la base de datos SQLite
for dato in listaProductos:
    if dato['precioFinal'] is not None:
        cursor.execute(f"INSERT INTO {nombre_tabla} (proveedor, producto, categoria, precio) VALUES (?, ?,?, ?)", (dato['proveedor'], dato['detalle'], dato['categoria'], dato['precioFinal']))

for dato in datos_dolar:
    cursor.execute(f"INSERT INTO {nombre_tabla_2} ( precioDolar, precioTarjeta) VALUES ( ?, ?)", (dato['precioDolar'], dato['precioTarjeta']))


# Confirmación de los cambios y cierre de la conexión a la base de datos
conexion.commit()
conexion.close()