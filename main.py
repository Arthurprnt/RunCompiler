import datetime, json, os, pygame, shutil, zipfile, time
import math
from tkinter.filedialog import askdirectory
import tkinter as tk
from tkinter import simpledialog
from btpygame import pygameimage, pygamebutton, collide, showtext

home_directory = os.path.expanduser('~')

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
                    if os.path.isfile(multipath + "/instances/" + inst + "/.minecraft/saves/" + d + "/speedrunigt/record.json"):
                        fsigt = open(multipath + "/instances/" + inst + "/.minecraft/saves/" + d + "/speedrunigt/record.json")
                        igtdata = json.load(fsigt)
                        if igtdata["is_completed"] is True:
                            if igtdata["retimed_igt"] < pb["time"]:
                                pb["time"] = igtdata["retimed_igt"]
                                pb["inst"] = inst
                                pb["savename"] = d
                        fsigt.close()
                        time.sleep(0.001)

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
pygame.display.set_caption('RunsCompiler by DraquoDrass')
pygame.display.set_icon(pygame.image.load('assets/icon.png'))
clock = pygame.time.Clock()
running = True
stat = 0
goodrun = None

background = pygameimage(pygame.image.load("assets/background.png"), (0, 0))
setupbackground = pygameimage(pygame.image.load("assets/setupbackground.png"), (0, 0))
btn_find = pygamebutton(pygame.image.load("assets/find.png"), pygame.image.load("assets/find_t.png"), (122, 10))
btn_yes = pygamebutton(pygame.image.load("assets/yes.png"), pygame.image.load("assets/yes_t.png"), (101, 140))
btn_no = pygamebutton(pygame.image.load("assets/no.png"), pygame.image.load("assets/no_t.png"), (304, 140))
btn_compile = pygamebutton(pygame.image.load("assets/zip.png"), pygame.image.load("assets/zip_t.png"), (62, 270))
btn_options = pygamebutton(pygame.image.load("assets/options.png"), pygame.image.load("assets/options_t.png"), (106, 445))
btn_locate = pygamebutton(pygame.image.load("assets/locate.png"), pygame.image.load("assets/locate_t.png"), (122, 270))
btn_finish = pygamebutton(pygame.image.load("assets/finish.png"), pygame.image.load("assets/finish_t.png"), (139, 760))

btn_click = pygamebutton(pygame.image.load("assets/click.png"), pygame.image.load("assets/click_t.png"), (57, 160))
btn_click2 = pygamebutton(pygame.image.load("assets/click.png"), pygame.image.load("assets/click_t.png"), (57, 310))
btn_click3 = pygamebutton(pygame.image.load("assets/click.png"), pygame.image.load("assets/click_t.png"), (57, 460))
btn_click4 = pygamebutton(pygame.image.load("assets/click.png"), pygame.image.load("assets/click_t.png"), (57, 610))

if not(os.path.exists(home_directory + "/.runscompiler/")):
    os.mkdir(home_directory + "/.runscompiler/")
if os.path.isfile(home_directory + "/.runscompiler/options.json"):

    optionschecked = True
    screen = pygame.display.set_mode((500, 520))

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
                            fsigt = open(
                                multipath + "/instances/" + locatedrun["inst"] + "/.minecraft/saves/" + locatedrun[
                                    "savename"] + "/speedrunigt/record.json")
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
else:

    optionschecked = False
    screen = pygame.display.set_mode((500, 840))

    while running:

        screen.blit(setupbackground.image, setupbackground.pos)
        showtext(screen, "Hello, welcome to run compiler.", "assets/McRegular.otf", 20, (250, 35), (255, 255, 255), "center")
        showtext(screen, "It looks like the app is not setup,", "assets/McRegular.otf", 20, (250, 60), (255, 255, 255), "center")
        showtext(screen, "so let's configure it !", "assets/McRegular.otf", 20, (250, 85), (255, 255, 255), "center")
        showtext(screen, "First, locate your MultiMC folder:", "assets/McRegular.otf", 20, (250, 135), (255, 255, 255), "center")
        btn_click.display(screen)

        if stat > 0:
            showtext(screen, "Nice, now locate the folder", "assets/McRegular.otf", 20, (250, 260), (255, 255, 255), "center")
            showtext(screen, "where you want the zip to go:", "assets/McRegular.otf", 20, (250, 285), (255, 255, 255), "center")
            btn_click2.display(screen)

        if stat > 1:
            showtext(screen, "Almost done, write", "assets/McRegular.otf", 20, (250, 410), (255, 255, 255), "center")
            showtext(screen, "your instance format (ex: RSG_*):", "assets/McRegular.otf", 20, (250, 435), (255, 255, 255), "center")
            btn_click3.display(screen)

        if stat > 2:
            showtext(screen, "To finish, write", "assets/McRegular.otf", 20, (250, 560), (255, 255, 255), "center")
            showtext(screen, "your saves format (ex: Random Speedrun #*)", "assets/McRegular.otf", 20, (250, 585), (255, 255, 255), "center")
            btn_click4.display(screen)

        if stat > 3:
            showtext(screen, 'Once the button "FINISH" clicked', "assets/McRegular.otf", 20, (250, 710), (255, 255, 255), "center")
            showtext(screen, "You'll need to restart the app", "assets/McRegular.otf", 20, (250, 735), (255, 255, 255), "center")
            btn_finish.display(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == pygame.BUTTON_LEFT:
                    if collide(btn_click, event.pos):
                        multimcpath = askdirectory()
                        if multimcpath != "":
                            stat = 1
                    elif collide(btn_click2, event.pos):
                        zipedpath = askdirectory()
                        if zipedpath != "":
                            stat = 2
                    elif collide(btn_click3, event.pos):
                        ROOT = tk.Tk()
                        ROOT.withdraw()
                        instanceformat = simpledialog.askstring(title="RunsCompiler by DraquoDrass", prompt="Instances name format:")
                        if instanceformat is not(None) and instanceformat != "" and "*" in instanceformat:
                            stat = 3
                    elif collide(btn_click4, event.pos):
                        ROOT = tk.Tk()
                        ROOT.withdraw()
                        saveworldformat = simpledialog.askstring(title="RunsCompiler by DraquoDrass", prompt="Saves name format:")
                        if saveworldformat != "" and "*" in saveworldformat:
                            stat = 4
                    elif collide(btn_finish, event.pos):
                        f = open(home_directory + "/.runscompiler/options.json", "w")
                        f.writelines(["{\n",
                                      f'\t"multipath": "' + multimcpath + '",\n',
                                      '\t"zippath": "' + zipedpath + '",\n',
                                      '\t"instformat": "' + instanceformat + '", \n',
                                      '\t"saveformat": "' + saveworldformat + '"\n',
                                      '}'
                                      ])
                        f.close()
                        running = False

        pygame.display.flip()
        clock.tick(60)

pygame.quit()
