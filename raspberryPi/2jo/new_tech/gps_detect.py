#!/usr/bin/python
# GoogleMapDownloader.py
# Created by Hayden Eskriett [http://eskriett.com]
#
# A script which when given a lnggitude, latitude and zoom level downloads a
# high resolution google map
# Find the associated blog post at: http://blog.eskriett.com/2013/07/19/downloading-google-maps/

'''
 sudo systemctl stop serial-getty@ttyAMA0.service
 sudo systemctl disable serial-getty@ttyAMA0.service
 sudo systemctl stop gpsd.socket
 sudo systemctl disable gpsd.socket
 sudo systemctl enable gpsd.socket
 sudo systemctl start gpsd.socket
 sudo gpsd /dev/ttyS0 -F /var/run/gpsd.sock
'''
import serial
import urllib.request
from PIL import Image
import os
import math
from decimal import *

class GoogleMapDownloader:
    """
        A class which generates high resolution google maps images given
        a lnggitude, latitude and zoom level
    """

    def __init__(self, lat, lng, zoom=12):
        """
            GoogleMapDownloader Constructor
            Args:
                lat:    The latitude of the location required
                lng:    The lnggitude of the location required
                zoom:   The zoom level of the location required, ranges from 0 - 23
                        defaults to 12
        """
        self._lat = lat
        self._lng = lng
        self._zoom = zoom

    def getXY(self):
        """
            Generates an X,Y tile coordinate based on the latitude, lnggitude
            and zoom level
            Returns:    An X,Y tile coordinate
        """

        tile_size = 256

        # Use a left shift to get the power of 2
        # i.e. a zoom level of 2 will have 2^2 = 4 tiles
        numTiles = 1 << self._zoom

        # Find the x_point given the lnggitude
        point_x = (tile_size / 2 + self._lng * tile_size / 360.0) * numTiles // tile_size

        # Convert the latitude to radians and take the sine
        sin_y = math.sin(self._lat * (math.pi / 180.0))

        # Calulate the y coorindate
        point_y = ((tile_size / 2) + 0.5 * math.log((1 + sin_y) / (1 - sin_y)) * -(
        tile_size / (2 * math.pi))) * numTiles // tile_size

        return int(point_x), int(point_y)

    def generateImage(self, **kwargs):
        """
            Generates an image by stitching a number of google map tiles together.
            Args:
                start_x:        The top-left x-tile coordinate
                start_y:        The top-left y-tile coordinate
                tile_width:     The number of tiles wide the image should be -
                                defaults to 5
                tile_height:    The number of tiles high the image should be -
                                defaults to 5
            Returns:
                A high-resolution Goole Map image.
        """

        start_x = kwargs.get('start_x', None)
        start_y = kwargs.get('start_y', None)
        tile_width = kwargs.get('tile_width', 5)
        tile_height = kwargs.get('tile_height', 5)

        # Check that we have x and y tile coordinates
        if start_x == None or start_y == None:
            start_x, start_y = self.getXY()

        # Determine the size of the image
        width, height = 256 * tile_width, 256 * tile_height

        # Create a new image of the size require
        map_img = Image.new('RGB', (width, height))
        count_x = -1
        for x in range(-(tile_width)//2, (tile_width//2) +1):
            count_x+=1
            count_y = -1
            for y in range(-(tile_height)//2, (tile_height//2) +1):
                count_y+=1
                url = 'https://mt0.google.com/vt?x=' + str(start_x + x) + '&y=' + str(start_y + y) + '&z=' + str(self._zoom)
                print(url)
                current_tile = str(x) + '-' + str(y)
                #print(current_tile)
                urllib.request.urlretrieve(url, current_tile)
                im = Image.open(current_tile)
                #print(count_x)
                #print(count_y)
                map_img.paste(im, (count_x * 256, count_y * 256))

                if(x == 0 and y == 0):
                    drawing_point_x = count_x
                    drawing_point_y = count_y

                os.remove(current_tile)

        return map_img, drawing_point_x, drawing_point_y
        
def main():
    #Receive GPS Data from Adafruit BreakOut Sensor
    getcontext().prec = 8
    fix = 0
    gps_con = 0
    lat = 0
    lng = 0

    while  True:
            # check for gps connected on USB0 or USB1
        if gps_con == 0 and os.path.exists('/dev/ttyAMA0') == True:
          ser = serial.Serial('/dev/ttyAMA0',9600,timeout = 10)
          gps_con = 1
          print ("connected on AMA0")

        if gps_con == 1:
          gps = ser.readline()

          gps = gps.decode()
          gpsList = []
          gpsList = gps.split(',')

          print("TEST:", gps[1:6])
          
        if gps[1 : 6] == "GPGGA":
          gps1 = gps.split(',',14)
        if gps[1 : 6] == "GPGSA":
          fix = int(gps[9:10])
        if gps[1 : 6] == "GPGGA" and len(gps) > 68 and (gps1[3] == "N" or gps1[3] == "S")and fix > 1:
          lat = int(gps[18:20]) + (Decimal(int(gps[20:22]))/(Decimal(60))) + (Decimal(int(gps[23:27]))/(Decimal(360000)))
          if gps[28:29] == "S":
            lat = 0 - lat
          lng = int(gps[30:33]) + (Decimal(int(gps[33:35]))/(Decimal(60))) + (Decimal(int(gps[36:40]))/(Decimal(360000)))
          if gps[41:42] == "W":
            lng = 0 - lng
        print(type(lat))
        print(type(lng))
        lat = float(lat)
        lng = float(lng)
        print ("LAT:" ,lat)
        print ("lng:",lng)
        if gps[1 : 6] == "GPRMC" and fix > 1:
          gps2 = gps.split(',',14)
          print ("SPEED:",gps2[7])
          print ("ANGLE:",gps2[8])
          #print ("")
        if lat > 30 and lng > 120 :
          print("Get the right lan and lon")
          break
        else :
          lat = 37.5083094
          lng = 127.0673151
          break

     # Create a new instance of GoogleMap Downloader
    gmd = GoogleMapDownloader(lat-0.0038, lng-0.0108, 18)

    print("The tile coorindates are {}".format(gmd.getXY()))

    try:
        # Get the high resolution image
        img, gplot_x, gplot_y = gmd.generateImage()
        img = img.convert("RGBA")
        ellipse_box = [gplot_x*256-175, gplot_y*256-175, gplot_x*256+175, gplot_y*256+175]

        tmp = Image.new('RGBA', img.size, (0,0,0,0))
        draw=ImageDraw.Draw(tmp)
        draw.ellipse(ellipse_box,fill=(255,0,0,127))
        img = Image.alpha_composite(img, tmp)
        img = img.convert("RGB")     
    except IOError:
        print("Could not generate the image - try adjusting the zoom level and checking your coordinates")
    else:
        # Save the image to disk
        img.save("high_resolution_image.png")
        print("The map has successfully been created")
#"revised"

if __name__ == '__main__':
    main()
