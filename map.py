import json
import requests
from databaseAccess import *
import time
import databaseAccess

key = 'ELGlMojjoaQyqNz3wB4aM5aXYNsgr3Jk'


def directions(departure, destination, waypoints, mapType, width, height):
    urlDir = 'https://www.mapquestapi.com/directions/v2/route?key=%s&from=%s&to=%s&routeType=pedestrian' \
            % (key, departure, destination)
    urlDir = urlDir.replace(' ', '+', -1)

    if departure != "" and destination != "":
        rDir = requests.get(urlDir)
        dataDir = json.loads(rDir.text)

        if "formattedTime" not in dataDir["route"]:
            return [""]
        duration = dataDir["route"]["formattedTime"]
        distance = "%.2f km" % (float(dataDir["route"]["distance"]))
        session = dataDir["route"]["sessionId"]
    else:
        markerColor = "-3B5998"
        if departure != "":
            waypoints[departure] = markerColor
        if destination != "":
            waypoints[destination] = markerColor

        duration = "waypoints"
        distance = ""
        session = ""

    isValidMap = staticMap(duration, distance, waypoints, session, mapType, width, height)
    if isValidMap == False:
        duration = ""
    return [duration, distance]


def staticMap(duration, distance, waypoints, session, mapType, width, height):
    urlStat = 'https://www.mapquestapi.com/staticmap/v5/map?&key=%s&scalebar=true&size=%d,%d&type=%s' \
            % (key, width, height, mapType)
    count = len(waypoints)
    if count > 0:
        urlStat += '&locations='
        for s in waypoints:
            urlStat += '%s|marker%s' % (s, waypoints[s])
            count -= 1
            if count > 0:
                urlStat += '||'
    if session != "":
        urlStat += '&session=%s&banner=%s / %s' % (session, distance, duration)
    else:
        ref = ""
        topLeft = [-90, 180]
        bottomRight = [90, -180]
        countOfWaypoints = 0
        isDataAvailable = False
        for s in waypoints:
            if countOfWaypoints == 0:
                ref = s
            urlGC = "https://www.mapquestapi.com/geocoding/v1/address?key=%s&location=%s&ignoreLatLngInput=true" \
                        % (key, s)
            urlGC = urlGC.replace(' ', '+', -1)
            rGC = requests.get(urlGC)
            dataGC = json.loads(rGC.text)
            if dataGC["info"]["statuscode"] == 0:
                isDataAvailable = True
                lat = float(dataGC["results"][0]["locations"][0]["latLng"]["lat"])
                lng = float(dataGC["results"][0]["locations"][0]["latLng"]["lng"])
                if lat > topLeft[0]:
                    topLeft[0] = lat
                if lat < bottomRight[0]:
                    bottomRight[0] = lat
                if lng < topLeft[1]:
                    topLeft[1] = lng
                if lng > bottomRight[1]:
                    bottomRight[1] = lng
                countOfWaypoints += 1
        if not isDataAvailable:
            return isDataAvailable
        elif countOfWaypoints == 1:
            urlStat += '&center=%s' % ref
        else:
            urlStat += '&boundingBox=%f,%f,%f,%f' % (topLeft[0], topLeft[1], bottomRight[0], bottomRight[1])
    urlStat = urlStat.replace(' ', '+', -1)

    rStat = requests.get(urlStat)

    countOfMaps = databaseCountOfTours() + 1
    with open('%s\\%d.png' % (imagesAbsolutePath, countOfMaps), 'wb') as newMap:
        try:
            newMap.write(rStat.content)
        except Exception as e:
            print("[%s] Hiba (térkép nyomtatása): %s" % (time.strftime("%H:%M:%S", time.localtime()), e))
            return False

    return True
