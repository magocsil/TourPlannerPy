# TourPlannerPy

A **TourPlannerPy** egy **Python**ban írt túratervező alkalmazás, amely a **Tkinter** könyvtár által nyújtott lehetőségekkel él a grafikus felhasználói felület megvalósítása során. Az útvonalakat **MySQL** szerver segítségével tárolja, így annak működése, párhuzamos futása elengedhetetlen a szoftver működéséhez. A szerver adatai a **databaseAccess.py** fájlban adhatók meg. Alapértelmezettként hostnak *localhost*, felhasználónak *root* és jelszónak is *root* van megadva. A szoftver az útvonalat és/vagy jelölőket térképen jeleníti meg, melyek elkészítéséhez a **MapQuest API**-t használtam.

## Felhasznált technológia (környezetek, könyvtárak, alkalmazások)
- Python 3.10 (Tkinter, MySQL Connector/Python, time, os, json, shutil, request, PIL)
- PyCharm 2023.1.2 (Community Edition)
- MySQL Community Server 8.0
- MySQL Workbench 8.0 CE
- MapQuest API (Directions API, Static Map API)

## Működés
- A program a főablak bal alsó sarkában állapotüzeneteket jelenít meg.

![image](https://github.com/magocsil/TourPlannerPy/assets/40305206/3a5848ed-a0f7-4b93-b1ab-e33a40ffc1ec)
- Az alkalmazás indításkor megkeresi a *tourplannerpy* adatbázist és létrehozza a szükséges *config*, *tours* és *waypoints* táblákat. Ha valamit nem talál, megpróbálja létrehozni. Ha ez nem sikerül, a felhasználónak a konzolon küld hibaüzenetet, és letiltja a további funkciókat. Amikor a felhasználó megoldotta az adatbázisszerverrel kapcsolatos problémákat, az *Adatbázis létrehozása* gombra kattintva ismét megpróbálhatja elindítja a programot.

![image](https://github.com/magocsil/TourPlannerPy/assets/40305206/ff18e237-ec21-4285-b52b-a4dbf6eb5acf)
- Minden, az adatbázissal kapcsolatos hiba megjelenik a konzolon.

![image](https://github.com/magocsil/TourPlannerPy/assets/40305206/53454eb3-bc64-4205-b9e7-90a435414498)
- Ha az adatbázis korábban használt, vagyis nem új, az is megjelenik a konzolon. Ilyenkor az alkalmazás betölti a már meglévő adatokat.

![image](https://github.com/magocsil/TourPlannerPy/assets/40305206/a9f4e60d-8c97-4a0b-bff4-2d1b58523e27)
- A teljes adatbázis törléséhez az *Adatbázis törlése* gombra kell kattintani. Előugró ablak kér megerősítést. Ez törli a képfájlokat is, amelyek a térképeket tartalmazzák!

![image](https://github.com/magocsil/TourPlannerPy/assets/40305206/386d3c4b-a6b5-4750-a40d-d5e960e2cb01)
- Túra létrehozásához az *+ Új túra hozzáadása...* listaelemre kell kattintani a főablak bal oldalán, majd a *Kiválaszt* gombra. Előugró ablakban meg lehet adni a túra elnevezését, kezdő- és végpontját, a létrehozandó térkép típusát és színes jelölőket. Az útvonaltervezés a *Tervezés* gombra kattintva indul el.

![image](https://github.com/magocsil/TourPlannerPy/assets/40305206/dc626443-ac5a-4a52-9e67-ade85b084635)
- A jelölő nevének megadása után színt lehet neki választani a *Szín kiválasztása...* gombra kattintva. Ha ez nem történik meg, akkor alapértelmezett színnel kerül mentésre. A kiválasztott színt alapértelmezettre a színválasztó gomb melletti *-* gomb megnyomásával lehet visszaállítani.

![image](https://github.com/magocsil/TourPlannerPy/assets/40305206/c128a4c7-6059-4626-9633-2d6105241911)
- Jelölőt a helyszín megadására fenntartott mező melletti *+* gombbal lehet létrehozni, és a kicsit lejjebb található listából kiválasztva, majd a lista melletti *-* gombra kattintva lehet törölni. A jelölőket az adatbázis egy erre kijelölt, külön táblájában tároljuk.

![image](https://github.com/magocsil/TourPlannerPy/assets/40305206/bf0432f9-43fd-4429-9597-38130e5be8d3)
- Mivel túrázás közben megesik, hogy egy környéket járunk be konkrét útvonal nélkül, lehetőség van térképet generálni útvonal nélkül is. Ehhez legalább az egyik útvonalmezőt - ilyen a kezdőpont- és a végpontmező - üresen kell hagyni, és vagy jelölőket kell hozzáadni, hozzáadni, vagy a másik mezőt kitölteni.
- A túra és a különböző helyszínek nevei nem lehetnek hosszabbak 100 karakternél.
- A tervezés gombra kattintva a MapQuest megpróbálja megtalálni a keresett gyalogos útvonalat. Ha ez sikerül, akkor elküldi az adatbázisnak az adatokat és bezárja a tervezőablakot. A túra kap egy ID-t, amely a fájlok könyvtárában létrehozott *output* mappában és az adatbázisban egyaránt azonosítja őket. Ha ez nem sikerül, a tervezőablak nem zárul be, és megjelenik rajta egy hibaüzenet.
- Két túrának nem lehet ugyanaz a neve. Ha mégis ilyen eset adódna, az új példány nevét bővíti egy *\** karakterrel.
- A tárolt túrák száma a főablak bal felső sarkában jelenik meg.

![image](https://github.com/magocsil/TourPlannerPy/assets/40305206/201ffb91-2df7-4b2d-a2de-98a720b27089)
- A túra adatait az útvonalat a főablak bal oldalán lévő listából kiválasztva, majd a *Kiválaszt* gombra kattintva jeleníthetjük meg. Az azonosító, a túra neve, az adatsor típusa, a kiindulópont, a cél, a hossz, az időtartam és legfeljebb kilenc lehelyezett jelölő kerül kiírásra. Természetesen a térkép is láthatóvá válik.

![image](https://github.com/magocsil/TourPlannerPy/assets/40305206/ccc958d0-b1b1-4643-91ba-deefaa0d2e2f)
- Ha a túrának volt kezdő- és végpontja, akkor *Útvonal* típusú, és a hossza kilométerben és az időtartama [óra:perc:másodperc] formátumban a térképre is rá van nyomtatva. Ha nem, akkor *Jelölők* típusa. Ebben az esetekben az említett adatok nincsenek számolva.
- A túra a jobb alsó sarkában lévő *Túra törlése* gombra kattintva törölhető. Ismét előugró ablak figyelmezteti a felhasználót. A módosítás az adatbázisban is megtörténik.

![image](https://github.com/magocsil/TourPlannerPy/assets/40305206/a26b7d8b-0e17-4d88-b227-25625d537a91)
- Az alkalmazásból való kilépéskor a program ismételten rákérdez a felhasználó szándékára. Ez a jelölőnégyzet segítségével kikapcsolható, melynek állapota az adatbázissal szinkronizálva van, így a program mindig a legutóbbi beállítást tárolja. A főablak jobb alsó sarkában a rákérdezés ki- és bekapcsolható.

![image](https://github.com/magocsil/TourPlannerPy/assets/40305206/ac2beb22-48d9-4cae-b470-b854983b81b3)

## Fájlok
### main.py
A **main.py** tartalmazza a felhasználói felületet és az ahhoz tartozó logikát. Az adatok validálása is jórészt itt történik. Nem hajt végre módosításokat az adatbázisban, csupán elindítja az ezzel kapcsolatos folyamatokat, és az eredménynek megfelelően módosítja a felhasználói felületet. Függvényei:
- *geometryGenerator(width, height)*: A Tkinter *geometry()* függvényébe írandó sztringet hozza létre az ablak kívánt méretéből. A képernyő felbontását is használja, hogy az ablakot a monitor közepére helyezze.
- *killWindow()*: Az alkalmazás bezárását megelőző figyelmeztető ablakot hozza létre.
- *addWindow()*: A túratervező ablakot valósítja meg.
- *storeTour()*: Megkísérli létrehozni az útvonalat és elmenteni a túrát a megadott paraméterekkel.
- *colorChange()*: A színválasztó ablak és logikája kódban.
- *colorDefault()*: A kiválasztott színt törlő gomb megnyomásakor végrehajtott utasításokat tartalmazza.
- *addWaypoint()*: Jelölő hozzáadásakor fut le. Megpróbálja elmenteni a jelölőt.
- *removeWaypoint()*: Törli a listából kiválasztott jelölőt.
- *selectListItem():* A főablak bal oldali listájából kiválasztott elemnek megfelelő függvény meghívásáért felelős.
- *tryDatabaseCreate()*: Megpróbálja létrehozni az adatbázist.
- *tryDatabaseDropPrompt()*: Az adatbázis törlését megelőző előugró ablakot hívja elő.
- *tryDatabaseDrop()*: Ha az adatbázis-törlési szándékot a felhasználó megerősítette, ez a függvény fut le.
- *tryDatabaseTablesCreate()*: Megpróbálja létrehozni az adatbázis tábláit.
- *tryDatabaseCountOfTours()*: Az adatbázisban található túrák számát kéri le.
- *updateList()*: Új túra létrehozása esetén frissíti a főablak bal oldalának listáját.
- *tryDatabaseInit()*: Megpróbálja betölteni a már eltárolt adatokat.
- *displayRecord()*: Egy túra részleteinek lekérését és az eredmények feldolgozását végzi.
- *clearFields()*: A főablak jobb oldaláról eltünteti a korábban megjelenített túra összes részletét.
- *tryDatabaseDeleteTourPrompt()*: A túra törlése előtti felugró ablakot készíti el.
- *tryDeleteTour()*: Törölteti az adatbázissal a kiválasztott túrát.

### map.py
A **map.py** kéri le az adatokat a MapQuest-től, és szükség szerint formázza őket. A térképet is ez nyomtatja ki *.png* fájlba. *GET* kérelmekkel dolgozik. Függvényei:
- *directions(departure, destination, waypoints)*: *Útvonal* típusú túra esetén az útvonaltervezés a feladata, *Jelölők* típusú rekord esetén pedig a megfelelő módon formázza az adatokat. A **Directions API**-t használja.
- *staticMap(duration, distance, waypoints, session, mapType, width, height)*: A végső térképet készíti el és kiírja azt egy fájlba, amelynek neve a túra azonosítója az adatbázisban.

### databaseAccess.py
A már korábban is említett **databaseAccess.py** az egyetlen fájl, amely ténylegesen az adatbázisnak küld utasításokat. Ha valami félremegy, a konzolra hibaüzenetet nyomtat. A *with* és a *try* felváltott használata miatt a hibaüzenet formátuma nem egységes. Függvényei:
- *databaseDrop()*: Megpróbálja törölni az adatbázist.
- *databaseCreate()*: Megkísérli elkészíteni az adatbázist.
- *databaseTableCreate()*: Megpróbálja elkészíteni az adattáblákat.
- *databaseUpdateRemember()*: Negálja az adatbázisban a kilépési rákérdezésre emlékező jelölőnégyzet aktuális állapotát.
- *databaseInit()*: A *config* táblába beírja az imént említett jelölőnégyzetet.
- *databaseRememberCheck()*: Kiolvassa az adatbázisból a szóban forgó jelölőnégyzet előző állapotát.
- *databaseInsert(tourName, departure, destination, tourInfo, waypoints)*: Beírja az adatbázisba a létrehozott túra részleteit.
- *databaseCountOfTours()*: A tárolt túrák számával tér vissza.
- *databaseLoad()*: A tárolt túrák nevével tér vissza.
- *databaseSelect(selectedElement)*: A keresett túra részleteit kéri le az adatbázisból.
- *datbaseSelectTour(selectedElement)*: A kiválasztott túrát törli.
- *dataSelectLastId()*: A *tours* tábla legutolsó kiadott azonosítójával tér vissza.
- *databaseSelectWaypoints(selectedElement)*: Kiolvassa a keresett túrához tartozó jelölőket.
