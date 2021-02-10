"""
Daniel Vogler
gpxProcessingExample
"""

from gpxProcessing import gpxProcessing
from datetime import timedelta, datetime
import pika, sys, os
import json

startTime = datetime.now()

### radius (m) around start/end trackpoints
radius = 7

### dtw threshold
dtwThreshold = 0.7

### gpx sub-track must consist of minimum number of points
minTrkps = 50

### initialize
gp = gpxProcessing()

def process(goldPath, activityPath):
    gold = gp.gpxLoading(goldPath)
    ### interpolate gold data
    goldInterpolated = gp.interpolate(gold)

    ### load activity data to be edited
    trkps = gp.gpxLoading(activityPath)
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

    print(">> Final DTW (y): %2.5f"% (finalDTW) )
    print(">> Final T [s]:  " , (finalT) )
    print(">> Total execution time:", datetime.now() - startTime)

def main():
    amqp_connection = os.environ.get('CLOUDAMQP', 'amqp://laceup:laceup@localhost:5672/%2f/messages')
    connection = pika.BlockingConnection(pika.URLParameters(amqp_connection))
    channel = connection.channel()

    def callback(ch, method, properties, body):
        message = json.loads(body)
        gold = message['gold']
        activity = message['activity']
        print("Processing... %r" % activity)
        process(gold, activity)
        print("Processing done %r" % activity)

    channel.basic_consume(queue='gpx_matching_queue', on_message_callback=callback, auto_ack=True)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
