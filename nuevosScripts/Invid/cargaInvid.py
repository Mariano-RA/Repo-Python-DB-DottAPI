
import csv
import json

#Direccion archivos en Windows
listadoCsv = 'Nb/Listado/listadoNB.csv'
listadoJson = 'Nb/Json/listadoJson.json'


#Direccion archivos en Linux
listadoCsv = 'Nb/Listado/listadoNB.csv'
listadoJson = 'Nb/Json/listadoJson.json'



def encontrar_valor(diccionario, clave):
    if clave in diccionario:
        return diccionario[clave]
    else:
        return "No existe una categoria para este producto"
    
def obtenerDiccionario(nombreDiccionario):
    with open('Repo-Python-DB-DottAPI/nuevosScripts/diccionarios/diccionarios.json') as diccionariosJson:
        # Carga los datos del archivo en un diccionario
        diccionarios = json.load(diccionariosJson)

    # Accede a los diccionarios individuales por su clave
    diccionarioBuscado = diccionarios[''+nombreDiccionario]

    # Ahora puedes trabajar con los diccionarios como desees
    return diccionarioBuscado




def crearJson():
    # Abre el archivo CSV en modo lectura con la codificación adecuada
    with open(listadoCsv, 'r',encoding="utf8") as file:
        # Crea un objeto lector CSV
        csv_reader = csv.reader(file, delimiter=';')

        # Crea una lista para almacenar los datos
        data = []


        # Lee cada fila del archivo CSV (ignorando la primera fila de encabezados)

        #"CODIGO";"ID FABRICANTE";"CATEGORIA";"DETALLE";"IMAGEN";"IVA";"STOCK";"GARANTIA";"MONEDA";"PRECIO";"PRECIO FINAL";"COTIZACION DOLAR";"PRECIO PESOS SIN IVA";"PRECIO PESOS CON IVA";"ATRIBUTOS"
        
        next(csv_reader)  # Ignora la primera fila de encabezados
        for row in csv_reader:
            descripcion = row[3]
            categoria = row[2]
            precio = row[10]
            

            # Crea un diccionario con los datos de cada registro
            registro = {
                'detalle': descripcion,
                'categoria': encontrar_valor(obtenerDiccionario('invid'), categoria),
                'precioFinal': round( (float(precio) * 1.1),2)
            }

            
            # Agrega el diccionario a la lista de datos
            data.append(registro)


    with open(listadoJson, 'w') as jf: 
        json.dump(data, jf, ensure_ascii=False, indent=2)


crearJson()