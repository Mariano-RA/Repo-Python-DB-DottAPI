import csv
import json

def encontrar_valor(diccionario, clave):
    if clave in diccionario:
        return diccionario[clave]
    else:
        return "No existe una categoria para este producto"

# Ejemplo de uso
diccionarioCategorias = {"569": "electro",
"001-0001": "impresion",
"001-0010": "accesorios",
"001-0011": "impresion",
"001-0014": "pc",
"001-0015": "sillas",
"001-0016": "discos",
"001-0020": "accesorios",
"001-0030": "cables",
"001-0032": "auriculares",
"001-0040": "accesorios",
"001-0050": "impresion",
"001-0054": "electro",
"001-0055": "redes",
"001-0060": "impresion",
"001-0070": "accesorios",
"001-0071": "accesorios",
"001-0100": "accesorios",
"001-0101": "accesorios",
"001-0110": "accesorios",
"001-0131": "accesorios",
"001-0134": "discos",
"001-0140": "accesorios",
"001-0150": "accesorios",
"001-0160": "electro",
"001-0168": "proyector",
"001-0170": "impresion",
"001-0190": "gabinetes",
"001-0200": "accesorios",
"001-0212": "electro",
"001-0231": "accesorios",
"001-0251": "impresion",
"001-0252": "impresion",
"001-0254": "impresion",
"001-0255": "impresion",
"001-0257": "impresion",
"001-0258": "impresion",
"001-0260": "impresion",
"001-0279": "impresion",
"001-0280": "rams",
"001-0282": "memorias",
"001-0290": "electro",
"001-0300": "redes",
"001-0304": "camaras",
"001-0305": "webcams",
"001-0309": "webcams",
"001-0310": "redes",
"001-0320": "monitores",
"001-0330": "procesadores",
"001-0331": "mother",
"001-0332": "coolers",
"001-0333": "pc",
"001-0335": "accesorios",
"001-0340": "mouse",
"001-0351": "auriculares",
"001-0355": "parlantes",
"001-0360": "notebooks",
"001-0363": "accesorios",
"001-0368": "tablets",
"001-0370": "impresion",
"001-0420": "accesorios",
"001-0430": "accesorios",
"001-0432": "redes",
"001-0455": "accesorios",
"001-0480": "impresion",
"001-0490": "impresion",
"001-0500": "accesorios",
"001-0510": "accesorios",
"001-0520": "accesorios",
"001-0521": "accesorios",
"001-0522": "procesadores",
"001-0523": "rams",
"001-0524": "discos",
"001-0525": "discos",
"001-0526": "discos",
"001-0527": "discos",
"001-0529": "fuentes",
"001-0530": "teclados",
"001-0531": "accesorios",
"001-0540": "electro",
"001-0555": "accesorios",
"001-0556": "fuentes",
"001-0557": "accesorios",
"001-0558": "accesorios",
"001-0560": "accesorios",
"001-0565": "camaras",
"001-0580": "electro",
"001-0590": "rams",
"001-0600": "impresion",
"001-0601": "camaras",
"001-0602": "impresion",
"001-0603": "impresion",
"001-0604": "impresion",
"001-0605": "impresion",
"001-0606": "impresion",
"001-0608": "impresion",
"001-0609": "impresion",
"001-0612": "redes",
"001-0613": "impresion",
"001-0620": "accesorios",
"001-0998": "notebooks",
"001-1001": "impresion",
"001-1055": "cables",
"001-1259": "electro",
"001-1260": "electro",
"001-1261": "pc",
"001-1510": "gamer",
"001-3560": "electro",
"001-3561": "accesorios",
"001-3562": "celulares",
"001-900": "electro",
"001-980": "electro",
"002-0015": "pc",
"002-0021": "pc",
"002-0137": "discos",
"002-0280": "rams",
"002-0281": "memorias",
"002-0299": "accesorios",
"002-0320": "monitores",
"002-0361": "notebooks",
"002-0368": "tablets",
"002-0510": "accesorios",
"002-0553": "vga",
"002-0670": "accesorios",
"002-0997": "pc",
"003-0099": "accesorios",
"003-0367": "accesorios",
"003-0800": "electro",
"003-1000": "electro",
"904-0152": "electro",
"907-1555": "smartwatch",
"908-957": "electro",
"001-0371": "impresion",
"001-0460": "impresion",
"001-0460": "impresion",
"001-0528": "redes",
"IT-T4E": "soportes",
"IT-TS5C": "soportes",
"IT-TSL42": "soportes",
"IT-TSL42": "soportes",
"IT-T4E": "soportes",
"002-1262": "pc",
"001-0390": "impresion",
"001-0610": "impresion",
"001-0220": "impresion",
"001-0607": "impresion",
"IT-DST": "soportes",
"IT-FMC44": "soportes",
"IT-ETS44": "soportes",
"IT-F22": "soportes",
"IT-T22": "soportes",
}


# Abre el archivo CSV en modo lectura con la codificación adecuada
with open('Air/Listado/articulos.csv', 'r') as file:
    # Crea un objeto lector CSV
    csv_reader = csv.reader(file, delimiter=',')

    # Crea una lista para almacenar los datos
    data = []


    #"Codigo","Descripcion","lista1","Tipo","IVA","ROS","MZA","CBA","LUG", "Grupo","Rubro","Part Number","Tipo"
    # Lee cada fila del archivo CSV (ignorando la primera fila de encabezados)
    next(csv_reader)  # Ignora la primera fila de encabezados
    for row in csv_reader:
        descripcion = row[1]
        rubro = row[10]
        iva = row[4]
        precio = row[2]
        

        # Crea un diccionario con los datos de cada registro
        registro = {
            'detalle': descripcion,
            'categoria': encontrar_valor(diccionarioCategorias, rubro),
            'precioFinal': round( (float(precio) * (1 + (float(iva)/100)) * 1.1),2)
        }

        # Agrega el diccionario a la lista de datos
        data.append(registro)

# Convierte la lista de datos a formato JSON
# json_data = json.dumps(data, indent=4)

with open('Air/Json/listadoAir.json', 'w') as jf: 
    json.dump(data, jf, ensure_ascii=False, indent=2)
