"""
Daniel Vogler
gpxProcessingExample
"""

from gpxProcessing import gpxProcessing
from matplotlib import pyplot as plt
from datetime import timedelta, datetime
startTime = datetime.now()

folderPath = "gpx_files/"

### example activity - matching tracks after cropping
# goldName = "tdh1_dv.gpx"
# fileName = "tdh1_mg.gpx"

###
goldName = "tds_sunnestube_segment.gpx"
fileName = "tds_sunnestube_activity_25_25.gpx"          # 0:25:22
# fileName = "tds_sunnestube_activity_25_55.gpx"        # 0:25:55
# fileName = "tds_sunnestube_activity_25_39.gpx"        # 0:25:39

# goldName = "nordicstar_weltcup_segment.gpx"
# fileName = "nordicstar_weltcup_activity_25_52.gpx"    # 0:25:35

# goldName = "nordicstar_dischmatal_segment.gpx"
# fileName = "nordicstar_dischmatal_activity_44_39.gpx" # 0:44:37

### example activity - no matching start/end points found
# goldName = "tdh1_dv.gpx"
# fileName = "tdu2a.gpx"

### example activity - gpx track jump during activity - tdh2
# goldName = "tdh2.gpx"
# fileName = "tdh2_error.gpx"

### example activity - overlapping tracks - tdu3
# goldName = "tdu3_dv.gpx"
# fileName = "tdu3_ls.gpx"

### example activity - match TH
# goldName = "th1_gold.gpx"
# fileName = "th1_ttb.gpx"
# goldName = "th2_gold.gpx"
# goldName = "th3_gold.gpx"


### radius (m) around start/end trackpoints
radius = 7

### dtw threshold
dtwThreshold = 0.7

### gpx sub-track must consist of minimum number of points
minTrkps = 50


### initialize
gp = gpxProcessing()

### load gold standard/baseline segment
gold = gp.gpxLoading(folderPath+goldName)
### interpolate gold data
goldInterpolated = gp.interpolate(gold)

### load activity data to be edited
trkps = gp.gpxLoading(folderPath+fileName)
### crop activity data to segment length
gpxCropped = gp.gpxTrackCrop(gold,trkps,radius)

### find potential start/end trackpoints - just for plotting
nnStart, nnStartIdx = gp.nearestNeighbours(gpxCropped,gold[:4,0],radius)
nnFinish, nnFinishIdx = gp.nearestNeighbours(gpxCropped,gold[:4,-1],radius)

### initial time
finalT = timedelta(seconds=1e6)
### possible start point combinations
for i in nnStartIdx:

    ### possible end point combinations
    for j in nnFinishIdx:

        ### start needs to happen before finish and include minTrkps in between
        if i < j-minTrkps:

            ### compute DTW between gold and activity
            dtw, deltaT = gp.dtwComputation(gpxCropped[:,i:j+1],goldInterpolated)

            ### collect final time and dtw
            if deltaT < finalT and dtw < dtwThreshold:
                finalT = deltaT
                finalDTW = dtw

print("\nFinal DTW (y): %2.5f"% (finalDTW) )
print("Final T [s]:  " , (finalT) )

print("Total execution time:", datetime.now() - startTime)

### plot gpx tracks
fig = plt.figure(num=None, figsize=(200, 150), dpi=80, facecolor='w', edgecolor='k')
gp.gpxPlot(fig,trkps,["Original Activity","+","b"])
gp.gpxPlot(fig,gpxCropped,["Activity Cropped","+","g"])
gp.gpxPlot(fig,nnStart,["NN Start","o","k"])
gp.gpxPlot(fig,nnFinish,["NN Finish","o","k"])
gp.gpxPlot(fig,gold,["Gold","+","r"])

### plot interpolated gpx tracks
fig = plt.figure(num=None, figsize=(200, 150), dpi=80, facecolor='w', edgecolor='k')
gp.gpxPlot(fig,gold,["Gold","o","r"])
gp.gpxPlot(fig,goldInterpolated.T,["Gold Interpolated","+","r"])
gp.gpxPlot(fig,gpxCropped,["Activity Cropped","o","g"])
gpxInterpolated = gp.interpolate(gpxCropped)
gp.gpxPlot(fig,gpxInterpolated.T,["Activity Interpolated","x","g"])

plt.show()
exit()
