import json

# Lectura del archivo JSON
with open("/home/do0t/Documents/Proyectos-GIT/Repo-Python-DB-DottAPI/nuevosScripts/Air/Json/listadoAir.json") as f:
    listadoAir = json.load(f)


with open("/home/do0t/Documents/Proyectos-GIT/Repo-Python-DB-DottAPI/nuevosScripts/Eik/Json/listadoJson.json") as f:
    listadoEik = json.load(f)

with open("/home/do0t/Documents/Proyectos-GIT/Repo-Python-DB-DottAPI/nuevosScripts/Elit/Json/listadoJson.json") as f:
    listadoElit = json.load(f)


with open("/home/do0t/Documents/Proyectos-GIT/Repo-Python-DB-DottAPI/nuevosScripts/Nb/Json/listadoJson.json") as f:
    listadoNb = json.load(f)


with open("/home/do0t/Documents/Proyectos-GIT/Repo-Python-DB-DottAPI/test.json", 'w') as jf: 
        json.dump(listadoAir + listadoEik + listadoElit + listadoNb, jf, ensure_ascii=False, indent=2)