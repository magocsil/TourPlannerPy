import tkinter as tk
from tkinter import *
from tkinter import colorchooser
from map import *
from PIL import ImageTk, Image
import os

selectedColor = "#3B5998"


def geometryGenerator(width, height):
    return '%dx%d+%d+%d' % (width, height, screenWidth / 2 - width / 2, screenHeight / 2 - height / 2)


def killWindow():
    if not remember.get():
        killer = Toplevel()
        killer.title("Kilépés")
        iconWarning = PhotoImage(file='warning.png')
        killer.iconphoto(False, iconWarning)
        killer.focus_force()
        killer.grab_set()

        killer.geometry(geometryGenerator(220, 80))
        killer.resizable(False, False)

        labelQuestion = Label(killer, text="Biztos ki akarsz lépni?")
        labelQuestion.place(x=0, y=0, width=220, height=25)
        buttonYes = Button(killer, text="Igen", command=mainWindow.destroy)
        buttonYes.place(x=25, y=25, width=70, height=25)
        buttonNo = Button(killer, text="Nem", command=killer.destroy)
        buttonNo.place(x=120, y=25, width=70, height=25)
        checkboxPrompt = Checkbutton(killer, text="Ne bosszants legközelebb!", variable=remember,
                                     command=databaseUpdateRemember)
        checkboxPrompt.place(x=0, y=50, width=220, height=30)
    else:
        mainWindow.destroy()


def addWindow():
    newTour = Toplevel()
    newTour.title("Új túra hozzáadása")
    iconNew = PhotoImage(file="new.png")
    newTour.iconphoto(False, iconNew)

    newTour.geometry(geometryGenerator(300, 280))
    newTour.resizable(False, False)
    newTour.focus_force()
    newTour.grab_set()

    newTourDeparture = StringVar()
    newTourDestination = StringVar()
    newTourName = StringVar()

    labelName = Label(newTour, text="Túra neve:")
    entryName = Entry(newTour, textvariable=newTourName)
    labelName.place(x=10, y=10)
    entryName.place(x=120, y=10, width=140)
    labelDep = Label(newTour, text="Kiindulás helye:")
    labelDest = Label(newTour, text="Úticél:")
    entryDep = Entry(newTour, textvariable=newTourDeparture)
    labelDep.place(x=10, y=35)
    entryDep.place(x=120, y=35, width=140)
    entryDest = Entry(newTour, textvariable=newTourDestination)
    labelDest.place(x=10, y=60)
    entryDest.place(x=120, y=60, width=140)

    waypoints = {}

    def storeTour():
        departure = entryDep.get()
        destination = entryDest.get()
        name = entryName.get()
        if ((departure != "" and len(departure) <= 50) or (destination != "" and len(destination) <= 50) \
                or len(waypoints) > 0) and len(name) <= 50 and name != "" and departure != destination:
            p = []
            for s in waypoints:
                if s == departure:
                    p.append(s)
                if s == destination:
                    p.append(s)
            for s in p:
                waypoints.pop(s)
            tourInfo = directions(departure, destination, waypoints, mapTypes[optionMapType.get()], detailsPaneWidth,
                                  mapPaneHeight)
            if tourInfo[0] == "":
                labelMessageNew.config(text="Az útvonalat nem sikerült megtervezni!", fg="red")
            elif tourInfo[0] == "waypoints":
                newTour.destroy()
                labelMessageMain.config(text="Helyszínek jelölve!", fg="green")
                if databaseInsert(name, departure, destination, tourInfo, waypoints) == 0:
                    updateList(name)
                tryDatabaseCountOfTours()
            else:
                newTour.destroy()
                labelMessageMain.config(text="Útvonal megtervezve!", fg="green")
                if databaseInsert(name, departure, destination, tourInfo, waypoints) == 0:
                    updateList(name)
                tryDatabaseCountOfTours()
        elif len(departure) > 50 or len(destination) > 50 or len(name) > 50:
            labelMessageNew.config(text="A helyszínek és a túra neve sem\nlehetnek hosszabbak 50 karakternél!",
                                   fg="red")
        else:
            labelMessageNew.config(text="A startot és/vagy a célt meg kell adni,\nvagy legalább egy jelölőt lerakni!",
                                   fg="red")

    buttonOk = Button(newTour, text="Tervezés", command=storeTour)
    buttonOk.place(x=110, y=245, width=80, height=25)

    labelWaypoints = Label(newTour, text="Jelölők")
    labelWaypoints.place(x=0, y=110, width=300, height=25)
    labelWaypointPlace = Label(newTour, text="Hely hozzáadása:")
    labelWaypointPlace.place(x=10, y=135)
    newTourWaypointPlace = StringVar()
    entryWaypointPlace = Entry(newTour, textvariable=newTourWaypointPlace)
    entryWaypointPlace.place(x=120, y=135, width=140)
    labelWaypointColor = Label(newTour, text="Jelölő színe:")
    labelWaypointColor.place(x=10, y=160)
    bWPCCC = "Szín kiválasztása..."

    def colorChange():
        global selectedColor
        selectedColor = str(colorchooser.askcolor(title="Szín kiválasztása")[1])
        if selectedColor != "None":
            buttonWaypointColorChange.config(text="", bg=selectedColor)

    def colorDefault():
        global selectedColor
        selectedColor = "#3B5998"
        buttonWaypointColorChange.config(text=bWPCCC, bg="#3B5998")

    buttonWaypointColorChange = Button(newTour, text=bWPCCC, command=colorChange, fg="white", bg="#3B5998")
    buttonWaypointColorChange.place(x=120, y=160, width=140)
    buttonWaypointColorDefault = Button(newTour, text="-", command=colorDefault)
    buttonWaypointColorDefault.place(x=270, y=160, height=25, width=25)

    labelMessageNew = Label(newTour, text="", justify="left")
    labelMessageNew.place(x=10, y=210, width=280)

    optionWaypoints = StringVar()

    def addWaypoint():
        nWP = newTourWaypointPlace.get()
        for t in waypoints:
            if t == nWP:
                labelMessageNew.config(text="Itt már van jelölő!", fg="red")
                return
        if nWP != "" and len(nWP) <= 50:
            global selectedColor
            waypoints[nWP] = selectedColor.replace("#", "-")
            colorDefault()
            optionMenuWaypoints["menu"].add_command(label=nWP, command=tk._setit(optionWaypoints, nWP))
            newTourWaypointPlace.set("")
            labelMessageNew.config(text="Jelölő hozzáadva!", fg="green")
        elif len(nWP) >= 50:
            labelMessageNew.config(text="A helyszínek nem lehetnek hosszabbak 50 karakternél!")
        else:
            labelMessageNew.config(text="Előbb meg kell adni egy helyszínt!", fg="red")

    buttonAddWaypoint = Button(newTour, text="+", command=addWaypoint)
    buttonAddWaypoint.place(x=270, y=135, width=25, height=25)
    labelDelete = Label(newTour, text="Jelölő törlése:")
    labelDelete.place(x=10, y=185)
    optionMenuWaypoints = OptionMenu(newTour, optionWaypoints, "--")
    optionMenuWaypoints.place(x=120, y=185, height=25, width=140)
    optionWaypoints.set("--")

    def removeWaypoint():
        if optionWaypoints.get() != "--":
            del waypoints[optionWaypoints.get()]
            optionMenuWaypoints['menu'].delete(optionMenuWaypoints['menu'].index(optionWaypoints.get()))
            optionWaypoints.set("--")
            labelMessageNew.config(text="Jelölő törölve!", fg="green")
        else:
            labelMessageNew.config(text="Előbb ki kell választani egy jelölőt!", fg="red")

    buttonRemoveWaypoint = Button(newTour, text="-", command=removeWaypoint)
    buttonRemoveWaypoint.place(x=270, y=185, width=25, height=25)

    labelMapType = Label(newTour, text="Térkép típusa:")
    labelMapType.place(x=10, y=85)
    mapTypes = {"Földtani": "map", "Hibrid": "hyb", "Műhold": "sat", "Utak (világos)": "light", "Utak (sötét)": "dark"}
    optionMapType = StringVar()
    optionMapType.set("Földtani")
    optionMenuMapType = OptionMenu(newTour, optionMapType,
                                   "Földtani", "Hibrid", "Műhold", "Utak (világos)", "Utak (sötét)")
    optionMenuMapType.place(x=120, y=85, height=25, width=140)


def selectListItem():
    if len(listOfTours.curselection()) > 0:
        if listOfTours.curselection()[0] == 0:
            addWindow()
        else:
            displayRecord(listOfToursVar[listOfTours.curselection()[0]])


def tryDatabaseCreate():
    if databaseCreate() == 0:
        labelMessageMain.config(text="Az adatbázis-kapcsolat létrejött!", fg="green")
        tryDatabaseTablesCreate()
    else:
        labelMessageMain.config(text="Az adatbázis-kapcsolatot nem sikerült létrehozni!", fg="red")


def tryDatabaseDropPrompt():
    dropper = Toplevel()
    dropper.title("Adatbázis törlése")
    iconWarning = PhotoImage(file='warning.png')
    dropper.iconphoto(False, iconWarning)
    dropper.focus_force()
    dropper.grab_set()

    dropper.geometry(geometryGenerator(280, 80))
    dropper.resizable(False, False)

    def tryDatabaseDrop():
        dropper.destroy()
        if databaseDrop() == 0:
            labelMessageMain.config(text="Az adatbázis törölve!", fg="green")
            buttonDatabaseDrop.config(state="disabled")
            buttonDatabaseCreate.config(state="normal")
            buttonSelect.config(state="disabled")
            labelRegistered.config(text="Elmentett túrák száma: 0", fg="black")
            remember.set(False)
            lOT_Length = len(listOfToursVar)
            for r in range(lOT_Length):
                if lOT_Length > 1 and r != 1:
                    listOfToursVar.pop(1)
            lOT = Variable(value=listOfToursVar)
            listOfTours.config(listvariable=lOT)

        else:
            labelMessageMain.config(text="Az adatbázist nem sikerült törölni!", fg="red")

    labelQuestion = Label(dropper, text="Biztosan törölni akarod az adatbázist?")
    labelQuestion.place(x=0, y=0, width=280, height=25)
    labelWarning = Label(dropper, text="Ez a művelet nem vonható vissza!", fg="red")
    labelWarning.place(x=0, y=25, width=280, height=25)
    buttonYes = Button(dropper, text="Igen", command=tryDatabaseDrop)
    buttonYes.place(x=55, y=50, width=70, height=25)
    buttonNo = Button(dropper, text="Nem", command=dropper.destroy)
    buttonNo.place(x=150, y=50, width=70, height=25)


def tryDatabaseTablesCreate():
    if databaseTablesCreate() != 0:
        labelMessageMain.config(text="Az adatbázis tábláit nem sikerült létrehozni!", fg="red")
        buttonDatabaseDrop.config(state="normal")
        buttonDatabaseCreate.config(state="normal")
        buttonSelect.config(state="disabled")
    else:
        buttonDatabaseDrop.config(state="normal")
        buttonDatabaseCreate.config(state="disabled")
        buttonSelect.config(state="normal")
        tryDatabaseCountOfTours()
        tryDatabaseInit()


def tryDatabaseCountOfTours():
    countOfTours = databaseCountOfTours()
    if countOfTours != -1:
        labelRegistered.config(text=("Elmentett túrák száma: %d" % countOfTours), fg="black")
    else:
        labelRegistered.config(text="Elmentett túrák száma: hiba!", fg="red")


def updateList(tourName):
    listOfToursVar.append(tourName)
    lOT = Variable(value=listOfToursVar)
    listOfTours.config(listvariable=lOT)


def tryDatabaseInit():
    if databaseInit() != -1:
        records = databaseLoad()
        for s in records:
            if s == -1:
                break
            updateList(s[0])


def displayRecord(selectedElement):
    option = databaseSelect(selectedElement)
    labelValueId.config(text=str(option[0]))
    labelValueName.config(text=option[1])
    labelValueType.config(text=option[2])
    labelValueDeparture.config(text=option[3])
    labelValueDestination.config(text=option[4])
    labelValueDuration.config(text=option[5])
    labelValueDistance.config(text=option[6])

    image = Image.open(("%d.png") % option[0])
    img = ImageTk.PhotoImage(image)
    labelMapImage = Label(mapPane, image=img)
    labelMapImage.image = img
    labelMapImage.place(x=0, y=0)



mainWindow = Tk()

remember = IntVar()

screenWidth = mainWindow.winfo_screenwidth()
screenHeight = mainWindow.winfo_screenheight()

mainWindow.title("Túratervező")
iconMain = PhotoImage(file='icon.png')
mainWindow.iconphoto(False, iconMain)

mainWindowWidth = 700
mainWindowHeight = mainWindowWidth / 4 * 3
mainWindow.geometry(geometryGenerator(mainWindowWidth, mainWindowHeight))
mainWindow.resizable(False, False)

headerHeight = 30
header = Frame(mainWindow, bg="light grey", width=mainWindowWidth, height=headerHeight)
header.place(x=0, y=0)
labelRegistered = Label(header, text="Elmentett túrák száma: 0", bg="light grey")
labelRegistered.place(x=20, y=(headerHeight - 20) / 2)
keywords = StringVar()
searchBar = Entry(header, textvariable=keywords, width=70)
searchBar.place(x=200, y=(headerHeight - 20) / 2)
buttonSearch = Button(header, text="Keresés")
buttonSearch.place(x=mainWindowWidth - 70, y=(headerHeight - 20) / 3)


footerHeight = 50
footer = Frame(mainWindow, bg="light grey", width=mainWindowWidth, height=footerHeight)
footer.place(x=0, y=mainWindowHeight - footerHeight)
rCB_str = "Ne kérdezzen rá kilépéskor"
rememberCheckBox = Checkbutton(footer, text=rCB_str, variable=remember, bg="light grey",
                               activebackground="light grey", command=databaseUpdateRemember)
rememberCheckBox.place(x=mainWindowWidth - 167, y=0, height=footerHeight)


labelMessageMain = Label(footer, text="", bg="light grey")
labelMessageMain.place(x=10, y=0, height=footerHeight)

listWidth = 175
detailsPaneWidth = mainWindowWidth - listWidth
detailsPaneHeight = mainWindowHeight - headerHeight - footerHeight
detailsPane = Frame(mainWindow, width=detailsPaneWidth, height=detailsPaneHeight)
detailsPane.place(x=listWidth, y=headerHeight)

mapPaneHeight = int(detailsPaneHeight / 2)
mapPane = Frame(detailsPane, width=detailsPaneWidth, height=mapPaneHeight)
mapPane.place(x=0, y=0)
labelMapPanePlaceholder = Label(mapPane, text="nincs beolvasott túra")
labelMapPanePlaceholder.place(x=0, y=0, width=detailsPaneWidth, height=mapPaneHeight)

fieldWidth1 = int(detailsPaneWidth / 3)
fieldWidth2 = int(detailsPaneWidth / 4)
labelFieldId = Label(detailsPane, text="Azonosító")
labelFieldId.place(x=0, y=mapPaneHeight + 50, height=25, width=fieldWidth2)
labelFieldName = Label(detailsPane, text="Név")
labelFieldName.place(x=0, y=mapPaneHeight, height=25, width=fieldWidth1)
labelFieldType = Label(detailsPane, text="Típus")
labelFieldType.place(x=fieldWidth2, y=mapPaneHeight + 50, height=25, width=fieldWidth2)
labelFieldDeparture = Label(detailsPane, text="Start")
labelFieldDeparture.place(x=fieldWidth1, y=mapPaneHeight, height=25, width=fieldWidth1)
labelFieldDestination = Label(detailsPane, text="Úticél")
labelFieldDestination.place(x=2 * fieldWidth1, y=mapPaneHeight, height=25, width=detailsPaneWidth - 2 * fieldWidth1)
labelFieldDuration = Label(detailsPane, text="Időtartam")
labelFieldDuration.place(x=2 * fieldWidth2, y=mapPaneHeight + 50, height=25, width=fieldWidth2)
labelFieldDistance = Label(detailsPane, text="Távolság")
labelFieldDistance.place(x=3 * fieldWidth2, y=mapPaneHeight + 50, height=25, width=detailsPaneWidth - 3 * fieldWidth2)
labelValueId = Label(detailsPane, text="", bg="white")
labelValueId.place(x=0, y=mapPaneHeight + 75, height=25, width=fieldWidth2)
labelValueName = Label(detailsPane, text="", bg="white")
labelValueName.place(x=0, y=mapPaneHeight + 25, height=25, width=fieldWidth1)
labelValueType = Label(detailsPane, text="", bg="white")
labelValueType.place(x=fieldWidth2, y=mapPaneHeight + 75, height=25, width=fieldWidth2)
labelValueDeparture = Label(detailsPane, text="", bg="white")
labelValueDeparture.place(x=fieldWidth1, y=mapPaneHeight + 25, height=25, width=fieldWidth1)
labelValueDestination = Label(detailsPane, text="", bg="white")
labelValueDestination.place(x=2 * fieldWidth1, y=mapPaneHeight + 25,
                            height=25, width=detailsPaneWidth - 2 * fieldWidth1)
labelValueDuration = Label(detailsPane, text="", bg="white")
labelValueDuration.place(x=2 * fieldWidth2, y=mapPaneHeight + 75, height=25, width=fieldWidth2)
labelValueDistance = Label(detailsPane, text="", bg="white")
labelValueDistance.place(x=3 * fieldWidth2, y=mapPaneHeight + 75, height=25, width=detailsPaneWidth - 3 * fieldWidth2)

listOfToursVar = ['+ Új túra hozzáadása...']
lOT = Variable(value=listOfToursVar)
listHeight = int((mainWindowHeight - headerHeight - footerHeight) / 17)
listOfTours = Listbox(mainWindow, listvariable=lOT, selectmode="single", height=listHeight)
listOfTours.place(x=0, y=headerHeight, width=listWidth)
buttonSelect = Button(mainWindow, text="Kiválaszt", command=selectListItem)
buttonSelect.place(x=0, y=mainWindowHeight - footerHeight - 25, width=listWidth)

buttonDatabaseCreate = Button(footer, text="Adatbázis\nlétrehozása", command=tryDatabaseCreate)
buttonDatabaseDrop = Button(footer, text="Adatbázis\ntörlése", fg="red", command=tryDatabaseDropPrompt, state="disabled")
buttonDatabaseDrop.place(x=mainWindowWidth - 167 - 60, y=0, height=footerHeight, width=60)
buttonDatabaseCreate.place(x=mainWindowWidth - 167 - 60 - 80, y=0, height=footerHeight, width=80)

tryDatabaseCreate()
if databaseRememberCheck() == 1:
    rememberCheckBox.select()

mainWindow.protocol("WM_DELETE_WINDOW", killWindow)
mainWindow.mainloop()
