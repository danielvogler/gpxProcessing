"""
Daniel Vogler
gpxProcessingExample
"""

from gpxProcessing import gpxProcessing
from matplotlib import pyplot as plt

folder_path = "gpx_files/"

### example activity - matching tracks after cropping
gold_name = "tdh1_dv.gpx"
activity_name = "tdh1_mg.gpx"

###
# gold_name = "tds_sunnestube_segment.gpx"
# activity_name = "tds_sunnestube_activity_25_25.gpx"          # 0:25:22
# activity_name = "tds_sunnestube_activity_25_55.gpx"        # 0:25:55
# activity_name = "tds_sunnestube_activity_25_39.gpx"        # 0:25:39

# gold_name = "nordicstar_weltcup_segment.gpx"
# activity_name = "nordicstar_weltcup_activity_25_52.gpx"    # 0:25:35

# gold_name = "nordicstar_dischmatal_segment.gpx"
# activity_name = "nordicstar_dischmatal_activity_44_39.gpx" # 0:44:37

# gold_name = "green_marathon_segment.gpx"
# activity_name = "green_marathon_activity_4_15_17.gpx"        # 4:15:03, 0:20:43 processing time, 0.13 Final DTW, 20m radius

### example activity - no matching start/end points found
# gold_name = "tdh1_dv.gpx"
# activity_name = "tdu2a.gpx"

### example activity - gpx track jump during activity - tdh2
# gold_name = "tdh2.gpx"
# activity_name = "tdh2_error.gpx"

### example activity - overlapping tracks - tdu3
# gold_name = "tdu3_dv.gpx"
# activity_name = "tdu3_ls.gpx"

### example activity - match TH
# gold_name = "th1_gold.gpx"
# activity_name = "th1_ttb.gpx"
# gold_name = "th2_gold.gpx"
# gold_name = "th3_gold.gpx"

### radius (m) around start/end trackpoints
radius = 40#7

"""
Track matching
"""

### initialize
gp = gpxProcessing()

### dtw matching for example segments/activities
final_time, final_dtw = gp.dtw_match(folder_path+gold_name, folder_path+activity_name,radius=radius)

"""
Track plotting
"""

### load gold standard/baseline segment
gold = gp.gpx_loading(folder_path + gold_name)
### interpolate gold data
gold_interpolated = gp.interpolate(gold)

### load activity data to be edited
trkps = gp.gpx_loading(folder_path + activity_name)
### crop activity data to segment length
gpx_cropped = gp.gpx_track_crop(gold, trkps, radius)

### find potential start/end trackpoints - just for plotting
nn_start, nn_start_idx = gp.nearest_neighbours(gpx_cropped,gold[:4,0],radius)
nn_finish, nn_finish_idx = gp.nearest_neighbours(gpx_cropped,gold[:4,-1],radius)

### plot gpx tracks
fig = plt.figure(num=None, figsize=(200, 150), dpi=80, facecolor='w', edgecolor='k')
gp.gpx_plot(fig,nn_start,["NN Start Cropped","X","b"],1200)
gp.gpx_plot(fig,nn_finish,["NN Finish Cropped","P","b"],1200)
gp.gpx_plot(fig,trkps,["Activity",".","k"])
gp.gpx_plot(fig,gpx_cropped,["Activity Cropped","o","k"])
gp.gpx_plot(fig,gold,["Gold","o","r"])

### plot interpolated gpx tracks
fig = plt.figure(num=None, figsize=(200, 150), dpi=80, facecolor='w', edgecolor='k')
gp.gpx_plot(fig,gpx_cropped,["Activity Cropped","o","k"])
gpx_interpolated = gp.interpolate(gpx_cropped)
gp.gpx_plot(fig,gpx_interpolated.T,["Activity Interpolated",".","k"])
gp.gpx_plot(fig,gold,["Gold","o","r"])
gp.gpx_plot(fig,gold_interpolated.T,["Gold Interpolated",".","r"])

plt.show()
exit()
