import shutil
import _mysql_connector
import mysql.connector as con
import time
import os

projectAbsolutePath = os.getcwd()
imagesAbsolutePath = projectAbsolutePath + "\\output"


def databaseDrop():
    try:
        with con.connect(host="localhost", user="root", password="root", database="tourplannerpy") as db:
            with db.cursor() as cursor:
                cursor.execute("DROP DATABASE IF EXISTS tourplannerpy")
                global projectAbsolutePath
                global imagesAbsolutePath
                if projectAbsolutePath != imagesAbsolutePath:
                    try:
                        shutil.rmtree(imagesAbsolutePath)
                    except Exception as e:
                        print(
                            "[%s] Hiba (célkönyvtár törlése): %s" % (time.strftime("%H:%M:%S", time.localtime()), e))
    except con.Error as e:
        print("[%s] Hiba (adatbázis törlése): %s" % (time.strftime("%H:%M:%S", time.localtime()), e))
        return -1
    else:
        return 0


def databaseCreate():
    try:
        with con.connect(host="localhost", user="root", password="root") as db:
            with db.cursor() as cursor:
                cursor.execute("""
                    CREATE DATABASE IF NOT EXISTS tourplannerpy;
                    DEFAULT CHARACTER SET utf8;
                    COLLATE utf8_hungarian_ci
                """)
    except con.Error as e:
        print("[%s] Hiba (adatbázis létrehozása): %s" % (time.strftime("%H:%M:%S", time.localtime()), e))
        return -1
    else:
        return 0


def databaseTablesCreate():
    try:
        with con.connect(host="localhost", user="root", password="root", database="tourplannerpy") as db:
            with db.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS config (
                        name VARCHAR(20) UNIQUE PRIMARY KEY,
                        value BOOLEAN DEFAULT TRUE
                    )
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS tours (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(100),
                        type ENUM('Útvonal', 'Jelölők'),
                        departure VARCHAR(100),
                        destination VARCHAR(100),
                        duration VARCHAR(12),
                        distance VARCHAR(12)
                    )
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS waypoints (
                        id INT,
                        location VARCHAR(100),
                        color VARCHAR(7)
                    )
                """)
    except con.Error as e:
        print("[%s] Hiba (adattáblák létrehozása): %s" % (time.strftime("%H:%M:%S", time.localtime()), e))
        return -1
    else:
        return 0


def databaseUpdateRemember():
    try:
        with con.connect(host="localhost", user="root", password="root", database="tourplannerpy") as db:
            with db.cursor() as cursor:
                cursor.execute("""
                    UPDATE tourplannerpy.config
                    SET value = NOT value WHERE name = 'remember'
                """)
                db.commit()
    except con.Error as e:
        print("[%s] Hiba  (emlékező jelölőnégyzet frissítése): %s" % (time.strftime("%H:%M:%S", time.localtime()), e))
        return -1
    else:
        return 0


def databaseInit():
    try:
        with con.connect(host="localhost", user="root", password="root", database="tourplannerpy") as db:
            with db.cursor() as cursor:
                try:
                    cursor.execute("INSERT INTO tourplannerpy.config (name, value) VALUES ('remember', False)")
                    db.commit()
                    global projectAbsolutePath
                    global imagesAbsolutePath
                    try:
                        os.mkdir(imagesAbsolutePath)
                    except:
                        imagesAbsolutePath = projectAbsolutePath
                    return 0
                except con.IntegrityError or _mysql_connector.MySQLInterfaceError:
                    print("[%s] A program korábban létrehozott adatbázist használ." \
                          % time.strftime("%H:%M:%S", time.localtime()))
                    return 1
    except con.Error as e:
        print("[%s] Hiba (kezdeti értékadás): %s" % (time.strftime("%H:%M:%S", time.localtime()), e))
        return -1


def databaseRememberCheck():
    try:
        with con.connect(host="localhost", user="root", password="root", database="tourplannerpy") as db:
            with db.cursor() as cursor:
                cursor.execute("SELECT value FROM tourplannerpy.config WHERE name = 'remember'")
                return cursor.fetchall()[0][0]
    except con.Error as e:
        print("[%s] Hiba (emlékező jelölőnégyzet betöltése): %s" % (time.strftime("%H:%M:%S", time.localtime()), e))


def databaseInsert(tourName, departure, destination, tourInfo, waypoints):
    tourType = "Útvonal"
    if tourInfo[0] == "waypoints":
        tourType = "Jelölők"
        if departure != "":
            waypoints[departure] = "#3B5998"
            departure = ""
        if destination != "":
            waypoints[destination] = "#3B5998"
            destination = ""
        tourInfo[0] = ""

    try:
        with con.connect(host="localhost", user="root", password="root", database="tourplannerpy") as db:
            with db.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO tourplannerpy.tours
                    (name, type, departure, destination, duration, distance) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')
                """ % (tourName, tourType, departure, destination, tourInfo[0], tourInfo[1]))
                db.commit()
                if len(waypoints) > 0:
                    for s in waypoints:
                        cursor.execute("""
                            INSERT INTO tourplannerpy.waypoints (id, location, color)
                            VALUES ((SELECT MAX(tourplannerpy.tours.id) FROM tourplannerpy.tours),
                            '%s', '%s')
                        """ % (s, waypoints[s]))
                        db.commit()
                return 0
    except con.Error as e:
        print("[%s] Hiba (túra hozzáadása): %s" % (time.strftime("%H:%M:%S", time.localtime()), e))
        return -1


def databaseCountOfTours():
    try:
        with con.connect(host="localhost", user="root", password="root", database="tourplannerpy") as db:
            with db.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(tourplannerpy.tours.id)
                    FROM tourplannerpy.tours
                """)
                result = cursor.fetchall()
                if result:
                    return int(result[0][0])
                else:
                    return 0
    except con.Error as e:
        print("[%s] Hiba (túrák számának lekérése): %s" % (time.strftime("%H:%M:%S", time.localtime()), e))
        return -1


def databaseLoad():
    try:
        with con.connect(host="localhost", user="root", password="root", database="tourplannerpy") as db:
            with db.cursor() as cursor:
                cursor.execute("SELECT name FROM tourplannerpy.tours")
                result = cursor.fetchall()
                if result:
                    return result
                else:
                    return []
    except con.Error as e:
        print("[%s] Hiba (túrák nevének lekérése): %s" % (time.strftime("%H:%M:%S", time.localtime()), e))
        return [-1]


def databaseSelect(selectedElement):
    try:
        with con.connect(host="localhost", user="root", password="root", database="tourplannerpy") as db:
            with db.cursor() as cursor:
                cursor.execute("SELECT * FROM tourplannerpy.tours WHERE name = '%s'" % selectedElement)
                result = cursor.fetchall()
                if result:
                    return result[0]
                else:
                    return []
    except con.Error as e:
        print("[%s] Hiba (túrák adatainak lekérése): %s" % (time.strftime("%H:%M:%S", time.localtime()), e))
        return [-1]


def databaseDeleteTour(selectedElement):
    try:
        with con.connect(host="localhost", user="root", password="root", database="tourplannerpy") as db:
            with db.cursor() as cursor:
                cursor.execute("SELECT id FROM tourplannerpy.tours WHERE name = '%s'" % selectedElement)
                id = cursor.fetchall()[0][0]
                os.remove("%s\\%d.png" % (imagesAbsolutePath, id))
                cursor.execute("DELETE FROM tourplannerpy.waypoints WHERE id = %d" % id)
                db.commit()
                cursor.execute("DELETE FROM tourplannerpy.tours WHERE id = %d" % id)
                db.commit()
                return 0
    except con.Error as e:
        print("[%s] Hiba (túra törlése): %s" % (time.strftime("%H:%M:%S", time.localtime()), e))
        return [-1]


def databaseSelectLastId():
    try:
        with con.connect(host="localhost", user="root", password="root", database="tourplannerpy") as db:
            with db.cursor() as cursor:
                cursor.execute("""
                    SELECT MAX(tourplannerpy.tours.id)
                    FROM tourplannerpy.tours
                """)
                result = cursor.fetchall()
                if result[0][0] is not None:
                    return int(result[0][0])
                else:
                    return 0
    except con.Error as e:
        print("[%s] Hiba (legutolsó azonosító lekérése): %s" % (time.strftime("%H:%M:%S", time.localtime()), e))
        return -1


def databaseSelectWaypoints(selectedElement):
    try:
        with con.connect(host="localhost", user="root", password="root", database="tourplannerpy") as db:
            with db.cursor() as cursor:
                cursor.execute("""
                    SELECT location, color FROM tourplannerpy.waypoints WHERE id = %d 
                """ % selectedElement)
                result = cursor.fetchall()
                if len(result) > 0 and result[0] is not None:
                    return result
                else:
                    return []
    except con.Error as e:
        print("[%s] Hiba (túrák számának lekérése): %s" % (time.strftime("%H:%M:%S", time.localtime()), e))
        return -1

