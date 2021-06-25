# Cloned Plate Detector
## Introduction:
An application for checking whether a car correctly corresponds to the model data linked to its number plate. This is achieved by predicting the make and model of the car from a video input, requesting the data linked to the number plate from the Driver and Vehicle Standards Agency (DVSA) database and then comparing the two sets of data.
## How it works:
- Using the YOLOv3 object detection algorithm I trained two models, one for detecting number plates and 
one for detecting two different UK car models. 
- I then used the resulting weights to detect plate and model objects from an input video, this provided two 
separate JSON files that contain the bounding box coordinates of detected objects. 
- The plate coordinates are used to make crops of the plates, the crops are then sent to a plate reading API 
which returns strings of the plate registration. 
- The strings are then input into the DVSA database and the resulting make and model data is recorded in 
custom plate objects.
- The coordinates of the plates are then compared with those of the previously detected car models. If a 
plate is within the bounding box of a car, it is predicted to belong to that car. 
- Then the vehicle data gathered from the DVSA database is compared with that of the car model 
prediction. The comparisons are printed in the console, finally the vehicle data and plate crops are 
labelled at the top of the video in each frame. An edited video that contains all of these drawn labels is 
returned as the final output.
