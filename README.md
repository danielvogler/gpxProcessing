# gpxProcessing

Pre-processing of gpx tracks for comparison to an existing gpx track. Checked are the joint start and end points with  given tolerance. 

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
