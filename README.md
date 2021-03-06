# gpxProcessing

Pre-processing and analysis of gpx tracks (activities) for comparison to an existing gpx track (gold standard, segment). Checked are the joint start and end points with a given tolerance to trim the activity. Both tracks are interpolated to allow for both curves to be compared with dynamic time warping. Dynamic time warping allows to assess whether the activity actually completed the gold standard segment, and what the shortest required time was (in case of multiple repetitions or many points of the activity within the allowed distance of start and end points). 


### Usage 
- GPX tracks are in `./gpx_files/`
- Example usage demonstrated in `./gpx_processing_example`


### Available in PyPI here: 
- [https://github.com/geopard-py/geopard](https://github.com/geopard-py/geopard)
- [https://pypi.org/project/geopard/](https://pypi.org/project/geopard/)


### Dependencies
Python libraries:
* gpxpy (`pip install gpxpy`)
* haversine (`pip install haversine`)
* similaritymeasures (`pip install similaritymeasures`)
* numpy
* matplotlib


![Example image](/images/example_track.png "Example of gpx crop")
Example of gold segment, total activity and activity cropped to gold segment length.


![Example image](/images/example_track_start-finish.png "Example start and end points")
Example of start and end points to crop gpx tracks and obtain pairs for dtw matching.

