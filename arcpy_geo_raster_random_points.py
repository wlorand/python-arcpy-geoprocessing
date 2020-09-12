# filename: arcpy_geo_raster_random_points.py (Python2)
# purpose: Create 100 random points within the extent of an elevation raster
#          and then write out a text file of point coordinates (x,y)

# Imports
import arcpy
import sys
import os.path
import random
from arcpy import env

# Set file and workspace settings
scriptdir = os.path.dirname(sys.argv[0])
datadir = scriptdir + "\ExamData\HMB"
env.workspace = datadir
# print "workspace: " + env.workspace

# Get the extent values from the elev raster
descRas = arcpy.Describe("elev")
ext = descRas.extent
# TODO: convert this code to python 3 -- the print vs print() is a dead giveaway
print "\nXMin: " + str(ext.XMin) + "\nXMax: " + str(ext.XMax) + "\nYMin: " + str(ext.YMin) + "\nYMax: " + str(ext.YMax)

# Get a random x-value within the extent
# print type(ext.XMin) # <type 'float'>
xRange = ext.XMax - ext.XMin
# print xRange, type(xRange)
# oneRandX = xRange * random.random() + ext.XMin
# print oneRandX

# Get a random y-value within the extent
# print type(ext.YMin) # <type 'float'>
yRange = ext.YMax - ext.YMin
# print yRange, type(yRange)
# oneRandY = yRange * random.random() + ext.YMin
# print oneRandY

# Create some empty lists for X and Y and populate them with 100 random values in the extent of the raster
randXList = []
randYList = []
for i in range(0, 100):
    randXValue = xRange * random.random() + ext.XMin
    randXList.append(int(randXValue))
    randYValue = yRange * random.random() + ext.YMin
    randYList.append(int(randYValue))
print randXList
print randYList

# open a text file to write out the random X, Y as point coordinates (space-delimited)
# (opening with a write handle "w" should create the file if it doesn't exist)
# todo: enhance by deleting the file if it already exists (not coded here)
pointfilepath = datadir + "\\randpts.txt"
out_randpts = open(pointfilepath, "w") // TODO: use context manager for Pythonic File I/O
out_randpts.write("X Y \n")  # header line
for i in range(len(randXList)):
    out_randpts.write(str(randXList[i]) + " " + str(randYList[i]) + "\n")
out_randpts.close()
