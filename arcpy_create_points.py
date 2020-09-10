# filename:  arcpy-create-points-insert-cursor.py (Python2)
# purpose: read in a txtfile (csv) via Python I/O
# and use the ArcPy module's Insert Cursor to put the data into a shapefile (.shp)

# imports and set local vars
import arcpy
import sys
import os.path
from arcpy import env
from arcpy import management as DM

scriptdir = os.path.dirname(sys.argv[0])
dataWS = "data"
ptfeatname = "sample_pts_from_csv_3.shp"
dir = scriptdir + "/" + dataWS
ptfeatpath = dir + "/" + ptfeatname

# env settings
env.workspace = dir

# create dir if it doesn't exist
if not arcpy.Exists(dir):
    DM.CreateFolder(scriptdir, dataWS)

# grab spatial reference object from existing data
sr = arcpy.Describe(r"F:\prog\marbles\samples.shp").spatialReference

# Read in some sample pts from a csv
inputFile = r"F:\prog\Marbles\samples.csv"
textin = open(inputFile, "r")

# Create an empty Shapefile featureclass (fc)
ptfeatures = DM.CreateFeatureclass(dir, ptfeatname, "POINT", "", "", "", sr)

# Add "SAMPLES_ID" and "CATOT" Fields to your fc
DM.AddField(ptfeatures, "SAMPLES_ID", "LONG")
DM.AddField(ptfeatures, "CATOT", "DOUBLE")

# Create an Insert Cursor and add point data to your fc
cur = arcpy.InsertCursor(ptfeatures)
firstRow = True
for txtrow in textin:
    if not firstRow:
        ptfeat = cur.newRow()
        values = txtrow.split(",")
        # build geometry from x,y in the csv
        ptobj = arcpy.Point(float(values[2]), float(values[3]))
        ptfeat.shape = ptobj
        # populate the other fields
        ptfeat.SAMPLES_ID = int(float(values[0]))
        ptfeat.CATOT = float(values[1])
        # actually insert the row
        cur.insertRow(ptfeat)
    firstRow = False

# Add X,Y Data to your fc (this must get its data from the Point obj)
DM.AddXY(ptfeatures)

# del objects and close text files for garbage collection
textin.close()
del cur, sr, ptfeat
