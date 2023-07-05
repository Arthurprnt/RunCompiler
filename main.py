import datetime, json, os, pygame, shutil, zipfile
from btpygame import pygameimage, pygamebutton, collide

home_directory = os.path.expanduser('~')
if not(os.path.exists(home_directory + "/.runcompiler/")):
    os.mkdir(home_directory + "/.runcompiler/")
if os.path.isfile(home_directory + "/.runcompiler/options.json"):
    optionschecked = True
else:
    f = open(home_directory + "/.runcompiler/options.json", "w")
    f.writelines(["{\n",
                  '\t"multipath": "your multimc path, ex: C:/MultiMC",\n',
                  '\t"zippath": "the folder you want the zip to be created, ex: C:/Runs",\n',
                  '\t"saveformat": "saves name format, ex: Random Speedrun #*"\n',
                  '}'
    ])
    f.close()
    optionschecked = False

instancename = "RSG_3"
add5runs = True

def mooveWorldFiles():
    f = open(home_directory + "/.runcompiler/options.json")
    data = json.load(f)
    multipath = data["multipath"]
    zippath = data["zippath"]
    saveformat = data["saveformat"]
    f.close()
    for (dirpath, dirnames, filenames) in os.walk(multipath + "/instances/" + instancename + "/.minecraft/saves"):
        validsaves = []
        for d in dirnames:
            if d.startswith(saveformat.replace("*", "")):
                validsaves.append(d)
        savetomoove = validsaves.pop(-1)
        break
    if not (os.path.exists(zippath + "/temp")):
        os.mkdir(zippath + "/temp")
    os.chdir(multipath + "/instances/" + instancename + "/.minecraft/saves/")
    shutil.copytree(savetomoove, zippath + f"/temp/WorldFiles/{savetomoove}")
    if add5runs:
        last5runs = []
        for i in range(5):
            last5runs.append(validsaves.pop(-1))
        for run in last5runs:
            shutil.copytree(run, zippath + f"/temp/Last5Worlds/{run}")

def mooveLogs():
    f = open(home_directory + "/.runcompiler/options.json")
    data = json.load(f)
    multipath = data["multipath"]
    zippath = data["zippath"]
    f.close()
    latest = datetime.datetime.fromtimestamp(os.path.getmtime(multipath + "/instances/" + instancename + "/.minecraft/logs/latest.log"))
    latestdate = str(latest).split(" ", len(str(latest)))[0]
    for (dirpath, dirnames, filenames) in os.walk(multipath + "/instances/" + instancename + "/.minecraft/logs"):
        todayslogs = []
        for d in filenames:
            d_datestamp = datetime.datetime.fromtimestamp(os.path.getmtime(multipath + "/instances/" + instancename + "/.minecraft/logs/" + d))
            if str(d_datestamp).startswith(latestdate):
                todayslogs.append(d)
        break
    if not (os.path.exists(zippath + "/temp")):
        os.mkdir(zippath + "/temp")
    if not (os.path.exists(zippath + "/temp/Logs")):
        os.mkdir(zippath + "/temp/Logs")
    os.chdir(multipath + "/instances/" + instancename + "/.minecraft/logs/")
    for l in todayslogs:
        shutil.copy(l, zippath + f"/temp/Logs/{l}")

def mooveFullMinecraft():
    f = open(home_directory + "/.runcompiler/options.json")
    data = json.load(f)
    multipath = data["multipath"]
    zippath = data["zippath"]
    f.close()
    shutil.copytree(multipath + "/instances/" + instancename + "/.minecraft", zippath + "/temp/FullDotMinecraft/.minecraft")

def zipit():
    f = open(home_directory + "/.runcompiler/options.json")
    data = json.load(f)
    zippath = data["zippath"]
    f.close()
    zip_file = zipfile.ZipFile(zippath + "/Verification.zip", 'w', zipfile.ZIP_DEFLATED)
    for (dirpath, dirnames, filenames) in os.walk(zippath + "/temp"):
        folderstozip = []
        for f in dirnames:
            folderstozip.append(zippath + "/temp/" + f)
        break
    for folder in folderstozip:
        for dirpath, dirnames, filenames in os.walk(folder):
            for filename in filenames:
                zip_file.write(
                    os.path.join(dirpath, filename),
                    os.path.relpath(os.path.join(dirpath, filename), os.path.join(folderstozip[0], '..')))
    zip_file.close()
    shutil.rmtree(zippath + "/temp")


mooveWorldFiles()
mooveLogs()
mooveFullMinecraft()
zipit()