"""
Daniel Vogler
gpxProcessing
"""

import gpxpy # pip3 install gpxpy
import geo.sphere as sphere # pip3 install geo-py
import numpy as np
from datetime import datetime
from matplotlib import pyplot as plt
from scipy.interpolate import splprep, splev
import similaritymeasures

class gpxProcessing:

    ### Load gpx file and extract information
    def gpxLoading(self,fileName):

        ### load file
        gpxDataOpen = open(fileName)
        gpxData = gpxpy.parse(gpxDataOpen)

        ### initialize lat/lon
        trkpLat = []
        trkpLon = []
        trkpEle = []
        trkpT = []

        ### load relevant gpx data
        for track in gpxData.tracks: 
            for segment in track.segments: 
                for i in range(0,len(segment.points)-1):
                    trkpPoint = segment.points[i]
                    trkpLat.append(trkpPoint.latitude)
                    trkpLon.append(trkpPoint.longitude)
                    trkpEle.append(trkpPoint.elevation)
                    trkpT.append(trkpPoint.time)

        trkps = np.asarray([trkpLat, trkpLon, trkpEle, trkpT])

        return trkps


    ### filter gpx data occurring between two points
    def gpxTrackCrop(self,gold,gpxData,radius):

        ### find possible start/end trackpoints
        nnStart = self.nearestNeighbours(gpxData,gold[:4,0],radius)
        nnFinish = self.nearestNeighbours(gpxData,gold[:4,-1],radius)

        ### determine time range for gpx track
        nnStartEarliest = min(nnStart[3])
        nnFinishLatest = max(nnFinish[3])

        ### delete trackpoints outside relevant time range
        indices = [i for i in range(len(gpxData[3])) if nnStartEarliest <= gpxData[3,i] <= nnFinishLatest]
        crLat   = [gpxData[0,i] for i in indices]
        crLon   = [gpxData[1,i] for i in indices]
        crEle   = [gpxData[2,i] for i in indices]
        crT     = [gpxData[3,i] for i in indices]
        gpxCropped = np.asarray([crLat, crLon, crEle, crT])

        return gpxCropped


    ### find nearest neighbouring points of input point
    def nearestNeighbours(self,gpxData,centroid,radius):

        ### distance of all points to centroid
        distance = [sphere._haversine_distance(i, centroid[:2]) for i in gpxData[:4,:][:2].T ]

        ### points within radius distance of centroid
        indices = [int(i) for i, x in enumerate(distance) if x < radius]

        ### check if nearby points were found
        if not indices:
            print("No trackpoints found near centroid\n")
            return -1

        ### lat, lon, ele, time, distance of all nearest neighbours
        lat   = [gpxData[0,i] for i in indices]
        lon   = [gpxData[1,i] for i in indices]
        ele   = [gpxData[2,i] for i in indices]
        T     = [gpxData[3,i] for i in indices]
        dis   = [distance[i] for i in indices]
        nn = np.asarray([lat, lon, ele, T, dis])

        return nn


    def dtwProcessing(self,gpxData,gold):

        ### interpolate activity
        gpxDataInterpolated = self.interpolate(gpxData)

        dtw, d = similaritymeasures.dtw(gpxDataInterpolated, gold)

        print("\nDynamic Time Warping (y) (DTW): ")
        print(dtw)

        return dtw


    def interpolate(self,gpxData):

        interpolationPoints = 1000
        
        ### add random noise to avoid duplicates
        data = np.array([(x+np.random.uniform(low=-1e-7, high=1e-7),y+np.random.uniform(low=-1e-7, high=1e-7)) for x,y in zip(gpxData[0][:], gpxData[1][:])])

        ### function that interpolates original data
        tck, u = splprep(data.T, u=None, s=0.0, t=10, per=1)

        ### 
        u_new = np.linspace(u.min(), u.max(), interpolationPoints)

        ### fit interpolation function to equi-distant data
        lat, lon = splev(u_new, tck, der=0)

        ### only return necessary gpx data
        points = np.zeros((interpolationPoints,2))
        points[:, 0] = lat
        points[:, 1] = lon

        return points


    ### plot gpx track
    def gpxPlot(self,fig,gpxData,plotInfo):

        fontSize = 30
        markerSize = 500
        plt.rcParams.update({'font.size': fontSize})
        plt.scatter(gpxData[1,:],gpxData[0,:],s=markerSize,marker=plotInfo[1],c=plotInfo[2],label=plotInfo[0])
        plt.legend(loc='upper left')
        plt.xlabel("Longitude")
        plt.ylabel("Latitude")

        return(fig)