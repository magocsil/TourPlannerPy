# TourPlannerPy

A **TourPlannerPy** egy Pythonban írt túratervező alkalmazás, amely a Tkinter könyvtár által nyújtott lehetőségekkel él a grafikus felhasználói felület megvalósítása során. Az útvonalakat MySQL szerver segítségével tárolja, így annak működése, párhuzamos futása elengedhetetlen a szoftver működéséhez. A szerver adatai a **databaseAccess.py** fájlban adhatók meg. Alapértelmezettként hostnak *localhost*, felhasználónak *root* és jelszónak is *root* van megadva. A szoftver az útvonalat és/vagy jelölőket térképen jeleníti meg, melyek elkészítéséhez a MapQuest API-t használtam.

## Felhasznált technológia (környezetek, könyvtárak, alkalmazások)
- Python 3.10 (Tkinter, MySQL Connector/Python)
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
- A tárolt túrák száma a főablak bal felső sarkában jelenik meg.

![image](https://github.com/magocsil/TourPlannerPy/assets/40305206/201ffb91-2df7-4b2d-a2de-98a720b27089)
- A túra adatait az útvonalat a főablak bal oldalán lévő listából kiválasztva, majd a *Kiválaszt* gombra kattintva jeleníthetjük meg. Az azonosító, a túra neve, az adatsor típusa, a kiindulópont, a cél, a hossz, az időtartam és legfeljebb kilenc lehelyezett jelölő kerül kiírásra. Természetesen a térkép is láthatóvá válik.

![image](https://github.com/magocsil/TourPlannerPy/assets/40305206/ccc958d0-b1b1-4643-91ba-deefaa0d2e2f)
- Ha a túrának volt kezdő- és végpontja, akkor *Útvonal* típusú, és a hossza kilométerben és az időtartama [óra:perc:másodperc] formátumban a térképre is rá van nyomtatva. Ha nem, akkor *Jelölők* típusa. Ebben az esetekben az említett adatok nincsenek számolva.
- A túra a jobb alsó sarkában lévő *Túra törlése* gombra kattintva törölhető. Ismét előugró ablak figyelmezteti a felhasználót. A módosítás az adatbázisban is megtörténik.

![image](https://github.com/magocsil/TourPlannerPy/assets/40305206/a26b7d8b-0e17-4d88-b227-25625d537a91)
- Az alkalmazásból való kilépéskor a program ismételten rákérdez a felhasználó szándékára. Ez a jelölőnégyzet segítségével kikapcsolható, melynek állapota az adatbázissal szinkronizálva van, így a program mindig a legutóbbi beállítást tárolja. A főablak jobb alsó sarkában a rákérdezés ki- és bekapcsolható.
