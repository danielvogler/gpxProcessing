"""
Daniel Vogler
gpxProcessingExample
"""

from gpxProcessing import gpxProcessing
from matplotlib import pyplot as plt

folderPath = "gpx_files/"
### gold standard other files are compared with
goldName = "tdh1_dv.gpx"
### example activity - to be cropped
fileName = "tdh1_mg.gpx" 
### example activity - no matching start/end points found
# fileName = "tdu2a.gpx"

### radius around start/end trackpoints
radius = 50


### initialize
gp = gpxProcessing()

### load gold standard/baseline segment
gold = gp.gpxLoading(folderPath+goldName)

### load activity data to be edited
trkps = gp.gpxLoading(folderPath+fileName)

### crop activity data to segment length
gpxCropped = gp.gpxTrackCrop(gold,trkps,radius)

### find potential start/end trackpoints
nnStart = gp.nearestNeighbours(gold,gold[:4,0],radius)
nnFinish = gp.nearestNeighbours(gold,gold[:4,-1],radius)


### plot gpx tracks
fig = plt.figure(num=None, figsize=(20, 15), dpi=80, facecolor='w', edgecolor='k')
gp.gpxPlot(fig,gold,["Gold","+","r"])
gp.gpxPlot(fig,nnStart,["NN Start","x","k"])
gp.gpxPlot(fig,nnFinish,["NN Finish","x","k"])
gp.gpxPlot(fig,trkps,["Original Activity","+","b"])
gp.gpxPlot(fig,gpxCropped,["Cropped","+","g"])
plt.show()
exit()