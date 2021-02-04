# gpxProcessing

Pre-processing and analysis of gpx tracks (activities) for comparison to an existing gpx track (gold standard, segment). Checked are the joint start and end points with a given tolerance to trim the activity. Both tracks are interpolated to allow for both curves to be compared with dynamic time warping. Dynamic time warping allows to assess whether the activity actually completed the gold standard segment, and what the shortest required time was (in case of multiple repetitions or many points of the activity within the allowed distance of start and end points). 

### Usage 
- GPX tracks are in `./gpx_files/`
- Example usage demonstrated in `./gpxProcessingExample`

### Dependencies
Python libraries:

* gpxpy (`pip install gpxpy`)
* haversine (`pip install haversine`)
* similaritymeasures (`pip install similaritymeasures`)
* datetime
* numpy
* matplotlib

![Example image](/images/example_cropped_track.png "Example of gpx crop")
