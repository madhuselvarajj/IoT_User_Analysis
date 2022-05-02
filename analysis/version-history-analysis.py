import os, csv
import xml.etree.ElementTree as ET
from lxml import etree
from bs4 import BeautifulSoup
from guesslang import Guess

guess = Guess()
linesOverFive = 0
codeCount = 0
versions = 0
keywords = ["<arduino>","<arduino-c++>", "<arduino-due>", "<arduino-esp8266>", "<arduino-every>", "<arduino-ide>", "<arduino-mkr1000>", "<arduino-ultra-sonic>", "<arduino-uno>" , "<arduino-uno-wifi>", "<arduino-yun>", "<platformio>",
            "<iot>", "<audiotoolbox>", "<audiotrack>", "<aws-iot>", "<aws-iot-analytics>", "<azure-iot-central>", "<azure-iot-edge>", "<azure-iot-hub>", "<azure-iot-hub-device-management>", "<azure-iot-sdk>", "<azure iot-suite>", "<bosch-iot-suite>", "<eclipse-iot>", "<google-cloud-iot>", "<hypriot>", "<iot-context-mapping>", "<iot-devkit>", "<iot-driver-behavior>", "<iot-for-automotive>", "<iot-workbench>", "<iotivity>", "<microsoft iot-central>", "<nb-iot>", "<rhiot>", "<riot>", "<riot-games-api>", "<riot.js>", "<riotjs>", "<watson-iot>", "<windows-10-iot-core>", "<windows-10-iot-enterprise>", "<windows-iot-core-10>", "<windowsiot>", "<wso2iot>", "<xamarin.iot>",
            "<adafruit>", "<android-things>", "<attiny>", "<avrdude>", "<esp32>", "<esp8266>", "<firmata>", "<gpio>", "<hm-10>", "<home-automation>", "<intel-galileo>", "<johnny-five>", "<lora>", "<motordriver>", "<mpu6050>", "<nodemc>", "<omxplayer>", "<raspberry-pi>", "<raspberry-pi-zero>", "<raspberry-pi2>", "<raspberry-pi3>", "<raspberry-pi4>", "<raspbian>", "<serial-communication>", "<servo>", "<sim900>", "<teensy>", "<wiringpi>", "<xbee>"]

IoTParent_IDs = []
IoTParent_Tags = {}
storedIds=[]
versions = 0

def getStoredPostIds():
    global storedIds
    if len(storedIds)== 0:
        filename = ""# insert file path to Post_Information.csv
        with open(filename, mode='r') as f:
            post_info = csv.DictReader(f)
            for row in post_info:
                storedIds.append(row['PostId'])


def fast_iter(context, func, *args, **kwargs):
    """
    http://lxml.de/parsing.html#modifying-the-tree
    Based on Liza Daly's fast_iter
    http://www.ibm.com/developerworks/xml/library/x-hiperfparse/
    See also http://effbot.org/zone/element-iterparse.htm
    """
    for event, elem in context:
        r = func(elem, *args, **kwargs)
        # It's safe to call clear() here because no descendants will be
        # accessed
        elem.clear()
        # Also eliminate now-empty references from the root node to elem
        for ancestor in elem.xpath('ancestor-or-self::*'):
            while ancestor.getprevious() is not None:
                del ancestor.getparent()[0]
        if r == -1:
          break
    del context

def storeVersionHistory(elem):
    global storedIds
    global versions
    lastId = 234714047
    if int(elem.get("Id"))<lastId:
        print("Not yet", elem.get("Id"))
        return 1
    filename = ""#insert file path to Version_Information
    with open(filename, mode='a') as output:
        print("Version ID and PostID:", elem.get("Id"), elem.get("PostId"))
        writer = csv.writer(output)
        if elem.get("PostId") in storedIds and (elem.get("PostHistoryTypeId")=="2" or elem.get("PostHistoryTypeId") == "5"):
            print("stored")
            writer.writerow([elem.get("Id"), elem.get("PostId"), elem.get("PostHistoryTypeId"), elem.get("UserId"), elem.get("UserDisplayName"),elem.get("CreationDate"),elem.get("Text")])
            versions = versions + 1


def main():
    global codeCount
    global linesOverFive
    global versions

    # post version history
    context = etree.iterparse("PostHistory.xml", tag='row')
    getStoredPostIds()
    print(len(storedIds))
    fast_iter(context,storeVersionHistory)
    print("number of code versions:     ", versions)



if __name__ == "__main__":
    main()
