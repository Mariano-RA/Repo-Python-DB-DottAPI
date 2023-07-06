import pandas as pd
import csv
import json


#Direccion archivos en Windows
listadoEikon = 'Eik/Listado/listadoEik.xlsx'
listadoCsv = 'Eik/Listado/listadoEik.csv'
listadoJson = 'Eik/Json/listadoJson.json'

def convertirACSV():
    # Leer el archivo XLSX
    df = pd.read_excel(listadoEikon)

    # Guardar como CSV
    df.to_csv(listadoCsv, index=False)


def encontrar_valor(diccionario, clave):
    if clave in diccionario:
        return diccionario[clave]
    else:
        return "No existe una categoria para este producto"
    
#Diccionario de Eikon
diccionario = {
    "ACCESORIOS":"accesorios",
"ACCESORIOS PARA NOTEBOOK":"accesorios",
"ACCESS POINT":"redes",
"ADAPTADORES USB INALAMBRICOS":"redes",
"ALL IN ONE":"pc",
"AURICULARES":"auriculares",
"AURICULARES BLUETOOTH":"auriculares",
"BATERIAS":"accesorios",
"CABLES":"cables",
"CABLES AUDIO":"cables",
"CABLES DE CORRIENTE":"cables",
"CABLES HDMI":"cables",
"CABLES USB":"cables",
"CABLES VGA":"cables",
"CABLES Y ADAPTADORES VARIOS":"cables",
"CABLES Y CONECTORES UTP - RED":"cables",
"CAMARAS WEB":"webcams",
"CARD READER":"memorias",
"CARTUCHOS EPSON ALTERNATIVOS":"impresion",
"CARTUCHOS EPSON ORIGINALES":"impresion",
"CARTUCHOS HP ALTERNATIVOS":"impresion",
"CARTUCHOS HP ORIGINALES":"impresion",
"CARTUCHOS KODAK ALTERNATIVOS":"impresion",
"COMBO MOUSE+TECLADO INALAMBRICO":"teclados",
"CONVERSORES":"accesorios",
"CONVERTIDORES SMART":"accesorios",
"COOLER FAN":"coolers",
"DISCOS INTERNOS":"discos",
"DISCOS INTERNOS SSD":"discos",
"DISCOS RIGIDOS EXTERNOS":"discos",
"ESTABILIZADORES DE TENSION":"electro",
"FUENTES PARA MONITORES":"monitores",
"FUENTES PARA NOTEBOOK":"notebooks",
"FUENTES VARIAS":"fuentes",
"GABINETES CON KIT":"gabinetes",
"JOYSTICK/GAMEPAD/VOLANTES":"gamer",
"MEMORIAS PARA COMPUTADORAS":"rams",
"MEMORIAS PARA NOTEBOOK":"rams",
"MESAS PARA COMPUTADORAS":"electro",
"MICROPROCESADORES":"procesadores",
"MONITORES":"monitores",
"MONITORES OUTLET":"monitores",
"MONITORES PARA EQUIPOS":"monitores",
"MOTHERBOARD":"mother",
"MOUSE":"mouse",
"MOUSE GAMING":"mouse",
"NOTEBOOK":"notebooks",
"OUTLET":"accesorios",
"PAD MOUSE":"mouse",
"PARLANTES":"parlantes",
"PARLANTES BLUETOOTH":"parlantes",
"PARLANTES PORTATILES BLUETOOTH":"parlantes",
"PEN DRIVE":"memorias",
"PILAS":"accesorios",
"PLACAS DE VIDEO":"vga",
"PLACAS PCI INALAMBRICAS":"redes",
"PRODUCTOS DE CONECTIVIDAD":"redes",
"PRODUCTOS SABRENT":"redes",
"RED NETWORK":"redes",
"REPUESTOS":"accesorios",
"ROUTER INALAMBRICO":"redes",
"SILLAS NIBIO":"sillas",
"SISTEMAS OPERATIVOS":"accesorios",
"SOFTWARE":"accesorios",
"SOPORTES":"soportes",
"TABLETS LENOVO":"tablets",
"TABLETS VARIAS":"tablets",
"TARJETAS DE MEMORIA":"memorias",
"TECLADOS":"teclados",
"TECLADOS GAMER":"teclados",
"TELEFONIA":"celulares",
"TONER BROTHER ALTERNATIVOS":"impresion",
"TONER HP ALTERNATIVOS":"impresion",
"TONER HP ORIGINALES":"impresion",
"TONER SAMSUNG ALTERNATIVOS":"impresion",
"UNIDADES OPTICAS":"accesorios",
"UPS":"electro",
"VARIOS":"accesorios",
"BROTHER":"impresion",
"SOPORTES Y ACCESORIOS":"accesorios",
"MICROFONOS":"microfonos",
"PILAS Y CARGADORES":"electro",
}



def crearJson():
    # Abre el archivo CSV en modo lectura con la codificación adecuada
    with open(listadoCsv, 'r') as file:
        # Crea un objeto lector CSV
        csv_reader = csv.reader(file, delimiter=',')

        # Crea una lista para almacenar los datos
        data = []


        #"Codigo","Descripcion","lista1","Tipo","IVA","ROS","MZA","CBA","LUG", "Grupo","Rubro","Part Number","Tipo"
        # Lee cada fila del archivo CSV (ignorando la primera fila de encabezados)
        next(csv_reader)  # Ignora la primera fila de encabezados
        for row in csv_reader:
            descripcion = row[1]
            categoria = row[6]
            precio = row[3]
            

            # Crea un diccionario con los datos de cada registro
            registro = {
                'detalle': descripcion,
                'categoria': encontrar_valor(diccionario, categoria),
                'precioFinal': round(( float(precio) * 1.1),2)
            }

            # Agrega el diccionario a la lista de datos
            data.append(registro)

    # Convierte la lista de datos a formato JSON
    # json_data = json.dumps(data, indent=4)

    with open(listadoJson, 'w') as jf: 
        json.dump(data, jf, ensure_ascii=False, indent=2)


convertirACSV()
crearJson()