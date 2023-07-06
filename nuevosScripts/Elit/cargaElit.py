import pandas as pd
import csv
import json


#Direccion archivos en Windows
listadoElit = 'Elit/Listado/listadoElit.xlsx'
listadoCsv = 'Elit/Listado/listadoEik.csv'
listadoJson = 'Elit/Json/listadoJson.json'

def convertirACSV():
    # Leer el archivo XLSX
    df = pd.read_excel(listadoElit)

    # Guardar como CSV
    df.to_csv(listadoCsv, index=False)


def encontrar_valor(diccionario, clave):
    if clave in diccionario:
        return diccionario[clave]
    else:
        return "No existe una categoria para este producto"
    
#Diccionario de Eikon
diccionario = {
    "Accesorios":"accesorios",
"Accesorios Seguridad":"accesorios",
"All In One":"pc",
"Auriculares":"auriculares",
"Botellas de Tinta":"impresion",
"Cables":"cables",
"Camaras IP":"camaras",
"Camaras Web":"webcams",
"Camaras Wifi":"camaras",
"Cartuchos de Tinta":"impresion",
"Cd":"accesorios",
"Cintas":"impresion",
"Coolers":"coolers",
"Discos Externos":"discos",
"Discos Externos SSD":"discos",
"Discos Internos":"discos",
"Discos Internos SSD":"discos",
"Dvd":"accesorios",
"Estabilizadores":"electro",
"Fuentes":"fuentes",
"Fundas":"accesorios",
"Gabinetes":"gabinetes",
"Impresoras de Sistema Continuo":"impresion",
"Impresoras Inkjet":"impresion",
"Impresoras Laser":"impresion",
"Impresoras Multifunción":"impresion",
"Memorias Flash":"memorias",
"Memorias PC":"rams",
"Microfonos":"microfonos",
"Monitores":"monitores",
"Motherboards":"mother",
"Mouses":"mouse",
"Notebooks Consumo":"notebooks",
"Notebooks Corporativo":"notebooks",
"Parlantes":"parlantes",
"PC de Escritorio":"pc",
"Pen Drive":"memorias",
"Placas de Red":"redes",
"Procesadores":"procesadores",
"Protectores":"electro",
"Resmas":"impresion",
"Routers":"redes",
"Sillas":"sillas",
"Smart Home":"electro",
"Soportes":"soportes",
"Tabletas Digitalizadoras":"tablet",
"Teclados":"teclados",
"Toners":"impresion",
"Ups":"electro",
"Baterias":"accesorios",
"Memorias Notebook":"accesorios",
"Escaner":"impresion",
"Volantes":"gamer",
"Memorias Notebook":"rams",
"Placas de Video":"vga",
"Joysticks":"gamer",
}



def crearJson():
    # Abre el archivo CSV en modo lectura con la codificación adecuada
    with open(listadoCsv, 'r') as file:
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
                'detalle': descripcion,
                'categoria': encontrar_valor(diccionario, categoria),
                'precioFinal': round((float(precio) * (1 + (float(iva)+ float(ivaInterno))/100) * 1.1),2)
            }

            
            # Agrega el diccionario a la lista de datos
            data.append(registro)


    with open(listadoJson, 'w') as jf: 
        json.dump(data, jf, ensure_ascii=False, indent=2)


convertirACSV()
crearJson()