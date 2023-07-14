import datetime, json, os, pygame, shutil, zipfile
import math

from tkinter.filedialog import askdirectory
from btpygame import pygameimage, pygamebutton, collide, showtext

home_directory = os.path.expanduser('~')
if not(os.path.exists(home_directory + "/.runscompiler/")):
    os.mkdir(home_directory + "/.runscompiler/")
if os.path.isfile(home_directory + "/.runscompiler/options.json"):
    optionschecked = True
else:
    f = open(home_directory + "/.runscompiler/options.json", "w")
    f.writelines(["{\n",
                  '\t"multipath": "your multimc path (ex: C:/MultiMC)",\n',
                  '\t"zippath": "the folder you want the zip to be created (ex: C:/Runs)",\n',
                  '\t"instformat": "instances name format (ex: RSG_*)", \n',
                  '\t"saveformat": "saves name format (ex: Random Speedrun #*)"\n',
                  '}'
    ])
    f.close()
    optionschecked = False

def locateSave():
    f = open(home_directory + "/.runscompiler/options.json")
    data = json.load(f)
    multipath = data["multipath"]
    instformat = data["instformat"]
    saveformat = data["saveformat"]
    f.close()
    for (dirpath, dirnames, filenames) in os.walk(multipath + "/instances/"):
        # Find all instances
        validintances = []
        for d in dirnames:
            if d.startswith(instformat.replace("*", "")):
                # Find all saves
                validintances.append(d)
        break
    pb = {
        "time": math.inf,
        "inst": None,
        "savename": None
    }
    for inst in validintances:
        for (dirpath, dirnames, filenames) in os.walk(multipath + "/instances/" + inst + "/.minecraft/saves/"):
            for d in dirnames:
                if d.startswith(saveformat.replace("*", "")):
                    fsigt = open(multipath + "/instances/" + inst + "/.minecraft/saves/" + d + "/speedrunigt/record.json")
                    igtdata = json.load(fsigt)
                    if igtdata["is_completed"]:
                        if igtdata["retimed_igt"] < pb["time"]:
                            pb["time"] = igtdata["retimed_igt"]
                            pb["inst"] = inst
                            pb["savename"] = d
                    fsigt.close()
            break
    return pb

def mooveWorldFiles():
    f = open(home_directory + "/.runscompiler/options.json")
    data = json.load(f)
    multipath = data["multipath"]
    zippath = data["zippath"]
    saveformat = data["saveformat"]
    f.close()
    for (dirpath, dirnames, filenames) in os.walk(multipath + "/instances/" + locatedrun['inst'] + "/.minecraft/saves"):
        validsaves = []
        for d in dirnames:
            if d.startswith(saveformat.replace("*", "")):
                validsaves.append(d)
        break
    if not (os.path.exists(zippath + "/temp")):
        os.mkdir(zippath + "/temp")
    shutil.copytree(multipath + "/instances/" + locatedrun['inst'] + "/.minecraft/saves/" + locatedrun["savename"], zippath + f"/temp/WorldFiles/{locatedrun['savename']}")
    runpb = int(locatedrun["savename"].replace(saveformat.replace("*", ""), ""))
    last5runs = []
    for i in range(runpb-5, runpb):
        if os.path.exists(multipath + "/instances/" + locatedrun['inst'] + "/.minecraft/saves/" + saveformat.replace("*", str(i)) + "/"):
            last5runs.append(saveformat.replace("*", str(i)))
    for run in last5runs:
        shutil.copytree(multipath + "/instances/" + locatedrun['inst'] + "/.minecraft/saves/" + run, zippath + f"/temp/Last5Worlds/{run}")

def mooveLogs():
    f = open(home_directory + "/.runscompiler/options.json")
    data = json.load(f)
    multipath = data["multipath"]
    zippath = data["zippath"]
    f.close()
    latest = datetime.datetime.fromtimestamp(os.path.getmtime(multipath + "/instances/" + locatedrun['inst'] + "/.minecraft/logs/latest.log"))
    latestdate = str(latest).split(" ", len(str(latest)))[0]
    for (dirpath, dirnames, filenames) in os.walk(multipath + "/instances/" + locatedrun['inst'] + "/.minecraft/logs"):
        todayslogs = []
        for d in filenames:
            d_datestamp = datetime.datetime.fromtimestamp(os.path.getmtime(multipath + "/instances/" + locatedrun['inst'] + "/.minecraft/logs/" + d))
            if str(d_datestamp).startswith(latestdate):
                todayslogs.append(d)
        break
    if not (os.path.exists(zippath + "/temp")):
        os.mkdir(zippath + "/temp")
    if not (os.path.exists(zippath + "/temp/Logs")):
        os.mkdir(zippath + "/temp/Logs")
    for l in todayslogs:
        shutil.copy(multipath + "/instances/" + locatedrun['inst'] + "/.minecraft/logs/" + l, zippath + f"/temp/Logs/{l}")

def mooveServerSide():
    f = open(home_directory + "/.runscompiler/options.json")
    data = json.load(f)
    multipath = data["multipath"]
    zippath = data["zippath"]
    f.close()
    if os.path.exists(multipath + "/instances/" + locatedrun['inst'] + "/.minecraft/verification-zips/"):
        pass
        #ServerSideRng is down so I'll add it later

def mooveFullMinecraft():
    f = open(home_directory + "/.runscompiler/options.json")
    data = json.load(f)
    multipath = data["multipath"]
    zippath = data["zippath"]
    f.close()
    shutil.copytree(multipath + "/instances/" + locatedrun['inst'] + "/.minecraft", zippath + "/temp/FullDotMinecraft/.minecraft")

def zipit():
    f = open(home_directory + "/.runscompiler/options.json")
    data = json.load(f)
    zippath = data["zippath"]
    f.close()
    zip_file = zipfile.ZipFile(zippath + f"/Verification_for_{pbtime.replace(':', '', len(pbtime))}_pb.zip", 'w', zipfile.ZIP_DEFLATED)
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

pygame.init()
screen = pygame.display.set_mode((500, 520))
pygame.display.set_caption('RunsCompiler by DraquoDrass')
pygame.display.set_icon(pygame.image.load('assets/icon.png'))
clock = pygame.time.Clock()
running = True
stat = 0
goodrun = None

background = pygameimage(pygame.image.load("assets/background.png"), (0, 0))
btn_find = pygamebutton(pygame.image.load("assets/find.png"), pygame.image.load("assets/find_t.png"), (122, 10))
btn_yes = pygamebutton(pygame.image.load("assets/yes.png"), pygame.image.load("assets/yes_t.png"), (101, 140))
btn_no = pygamebutton(pygame.image.load("assets/no.png"), pygame.image.load("assets/no_t.png"), (304, 140))
btn_compile = pygamebutton(pygame.image.load("assets/zip.png"), pygame.image.load("assets/zip_t.png"), (62, 270))
btn_options = pygamebutton(pygame.image.load("assets/options.png"), pygame.image.load("assets/options_t.png"), (106, 445))
btn_locate = pygamebutton(pygame.image.load("assets/locate.png"), pygame.image.load("assets/locate_t.png"), (122, 270))

while running:

    screen.blit(background.image, background.pos)
    btn_find.display(screen)
    btn_options.display(screen)

    if stat in [1, 2, 3, 4, 404]:
        showtext(screen, pbtexte, "assets/McRegular.otf", 20, (250, 95), (255, 255, 255), "center")
    if stat in [1, 2, 3, 4]:
        showtext(screen, f"Is it the right run?", "assets/McRegular.otf", 20, (250, 120), (255, 255, 255), "center")
        btn_yes.display(screen)
        btn_no.display(screen)
    if stat == 2 or stat == 4:
        showtext(screen, f"Instance: {locatedrun['inst']}", "assets/McRegular.otf", 20, (250, 225), (255, 255, 255), "center")
        showtext(screen, f"Save name: {locatedrun['savename']}", "assets/McRegular.otf", 20, (250, 250), (255, 255, 255), "center")
        btn_compile.display(screen)
    if stat in [3, 33, 404]:
        showtext(screen, f"As the save couldn't automatically be found,", "assets/McRegular.otf", 20, (250, 225), (255, 255, 255), "center")
        showtext(screen, f"please locate it manually.", "assets/McRegular.otf", 20, (250, 250), (255, 255, 255), "center")
        btn_locate.display(screen)
    if stat == 4:
        showtext(screen, f"Zip file created !", "assets/McRegular.otf", 20, (250, 355), (255, 255, 255), "center")
    if stat == 33:
        showtext(screen, "This world didn't finished the game.", "assets/McRegular.otf", 20, (250, 95), (255, 255, 255), "center")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == pygame.BUTTON_LEFT:
                if collide(btn_find, event.pos):
                    locatedrun = locateSave()
                    if locatedrun["time"] == math.inf:
                        pbtexte = f"Couldn't find any finished run."
                        stat = 404
                    else:
                        seconds = int((locatedrun["time"] / 1000) % 60)
                        minutes = int((locatedrun["time"] / (1000 * 60)) % 60)
                        hours = int((locatedrun["time"] / (1000 * 60 * 60)) % 24)
                        if hours == 0:
                            pbtexte = f"Found a pb with the time of {minutes}:{seconds}"
                            pbtime = f"{minutes}:{seconds}"
                            stat = 1
                        else:
                            pbtexte = f"Found a pb with the time of {hours}:{minutes}:{seconds}"
                            pbtime = f"{hours}:{minutes}:{seconds}"
                            stat = 1
                elif collide(btn_yes, event.pos) and stat in [1, 3]:
                    stat = 2
                elif collide(btn_no, event.pos) and stat in [1, 2]:
                    stat = 3
                elif collide(btn_locate, event.pos) and stat in [3, 33, 404]:
                    selectedpath = askdirectory()
                    if selectedpath == "":
                        stat = 33
                    else:
                        splitedpath = selectedpath.split("/", len(selectedpath))
                        locatedrun = {
                            "time": math.inf,
                            "inst": splitedpath[-4],
                            "savename": splitedpath[-1]
                        }
                        f = open(home_directory + "/.runscompiler/options.json")
                        data = json.load(f)
                        multipath = data["multipath"]
                        f.close()
                        fsigt = open(multipath + "/instances/" + locatedrun["inst"] + "/.minecraft/saves/" + locatedrun["savename"] + "/speedrunigt/record.json")
                        igtdata = json.load(fsigt)
                        if igtdata["is_completed"]:
                            locatedrun["time"] = igtdata["retimed_igt"]
                            seconds = int((locatedrun["time"] / 1000) % 60)
                            minutes = int((locatedrun["time"] / (1000 * 60)) % 60)
                            hours = int((locatedrun["time"] / (1000 * 60 * 60)) % 24)
                            if hours == 0:
                                pbtexte = f"Found a pb with the time of {minutes}:{seconds}"
                                pbtime = f"{minutes}:{seconds}"
                                stat = 1
                            else:
                                pbtexte = f"Found a pb with the time of {hours}:{minutes}:{seconds}"
                                pbtime = f"{hours}:{minutes}:{seconds}"
                                stat = 1
                        else:
                            stat = 33
                elif collide(btn_compile, event.pos) and stat == 2:
                    mooveWorldFiles()
                    mooveLogs()
                    zipit()
                    stat = 4
                elif collide(btn_options, event.pos):
                    os.startfile(home_directory + "/.runscompiler/options.json")
                    optionschecked = True

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
