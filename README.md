[![Build Status](https://travis-ci.com/ahoimarie/cb_recordings.svg?token=USnpr24bQjvx6pPPWuJG&branch=master)](https://travis-ci.com/ahoimarie/cb_recordings)
[![codecov](https://codecov.io/gh/ahoimarie/cb_recordings/branch/master/graph/badge.svg)](https://codecov.io/gh/ahoimarie/cb_recordings)

# Electrophysiological recordings with Neuropixels and simultaneous High-Speed video (Dalsa Genie HM)

This repository allows you to load and process both the tracked, 
traced whisker data (assuming whisker videos were processed on [Janelia's whisker tracker](https://wiki.janelia.org/wiki/display/MyersLab/Whisker+Tracking)) 
and [Neuropixels](https://www.neuropixels.org) data that were spike-sorted using [Kilosort2](https://github.com/MouseLand/Kilosort2). 

This repository contains functions to open the spike-sorted [Neuropixels](https://www.neuropixels.org) data as well as processed whisking data in *python*. 

The Neuropixels module `loadKSdir` is based upon the Matlab implementation of it from the lab of Kenneth Harris and Matteo Carandini at UCL, available on the [Cortex Lab Github page](https://github.com/cortex-lab/spikes/). 

The **whisking module** loads the whisking data and extracts the parts of the recording where whisking was detected.
Whisking parameter extraction is translated from and based on the script that accompanies the Primer [Analysis of Neuronal Spike
Trains, Deconstructed", by J. Aljadeff, B.J. Lansdell, A.L. Fairhall and D. Kleinfeld (2016) Neuron,
91](http://dx.doi.org/10.1016/j.neuron.2016.05.039). 


## Assumptions: 
* You have read the relevant information on [Neuropixels](https://www.neuropixels.org), and read through the [Neuropixels github](https://github.com/cortex-lab/neuropixels/wiki). 
* You have read the documentation on [Spike Glx](https://billkarsh.github.io/SpikeGLX/), including any subcategories. They like to update things every now and then, so keep checking.  
* You have read the documentation on [Kilosort2](https://github.com/MouseLand/Kilosort2)
* You have read the documentation on [Phy](https://github.com/cortex-lab/phy)
* You have read the documentation on [whisker tracking](https://wiki.janelia.org/wiki/display/MyersLab/Whisker+Tracking) and [Nathan Clack's github](https://github.com/nclack/whisk) and [ffmpeg](https://ffmpeg.org). 
* The time-consuming manual spike sorting is carried out as discussed e.g. [Phy](https://phy.readthedocs.io/en/latest/) or [at Kilosort2](https://github.com/MouseLand/Kilosort2). 

***
***

# Whisker signal preprocessing (processing high-speed camera data)
In addition to neural data processing, you need to process the high-speed video data. 
1. You copied your data from the acquisition machine to your NAS. 
2. Read everything you need about the [whisker tracker developed by N. Clack at Janelia](https://wiki.janelia.org/wiki/display/MyersLab/Whisker+Tracking+Downloads). You may also install it on your machine. 
3. As instructed on the above mentioned site, make sure [ffmpeg](www.ffmpeg.org) is installed. 
4. You need to *transcode* the files. You may also wish to crop it, which you can also do with `ffmpeg`. 
5. Streampix records the files at an approximate frame rate. The whisker tracker cannot deal with that.  The frame rate doesn't really affect the data, but it does affect the timestamps that are attached to each packet. Use the following to transcode your videos in a lossless way using huffyuv at a frame rate of 299 Hz. (Here, we use 299 as an inspection with `ffprobe -i video.avi` had indicated that the effective frame rate was 299.3 Hz, so we round down). Video input is *video.avi* and video output is *video_rc.avi*, which we create in this step. You may change the name as you wish. In your command line, go to the folder of your video/experiment data and type: 
    ``` bash
    ffmpeg -i testvideo.avi -crf 0 -c:v huffyuv -c:a copy -r 299 testvideo_rc.avi
    ```
***
6. After transcoding, open your new video_rc.avi with the whiski software (drag and drop). Identify the best point for your whisker pad origin (hover with your mouse). Note down the coordinates indicated. Measuring the whisker data assuming  **vertical** alignment of the longitudinal mouse axis, the whisker pad is located at **posX** and **posY**.
7. Next: Whisker tracing. In your terminal, type:
``` bash
    trace testvideo_rc.avi testvideo.whiskers
```
   This traces all lines in the video and takes a LONG time. Sometimes several hours. 
***
7. After tracing finished, we run the measurement function of whiski. In this example, we assume a vertical alignment of the longitudinal mouse axis, hence we use the **y** variable. 
    ```bash
    measure --face posX posY y testvideo.whiskers testvideo.measurements
    ```
***
8. Classification of measurements, where we overwrite the previously obtained measurements. You could also opt to create yet another file if you wish. Here, the whiskers are classified throughout the measurements. Pixel dimensions of the whiskers are found at 0.04 px per 2 mm, and we want to classify `n = 3` whiskers (all others were trimmed). 
    ``` bash
    classify testvideo.measurements testvideo.measurements posX posY y -px2mm 0.04 -n 3
    ```
***
9. Reclassification.
    ``` bash
    reclassify -n 3 testvideo.measurements testvideo.measurements
    ```
10. Optional: convert outputs to human readable formats (from binaries)
    ``` bash
    whisker_convert testvideo.whiskers testvideoH.whiskers whiskbin1
    ```
11. Convert measurement outputs to human readable format:
    ``` bash
    measurements_convert testvideo.measurements testvideoH.measurements v1
    ```
    
# Putting things together
## Processing of whisker measurements files
The measurements files and whisker files created by whiski are huge and impractical to use. Hence, we are going to convert them to contain the useful data. 
* Convert measurements data to .npy using the scripts in `/whiskiconversion`. The scripts depend on the module `npy-matlab`, which we already included in the kilosort2 clustering folder. They also depend on `LoadMeasurements.m` provided by [the Janelia whisker tracker](https://github.com/nclack/whisk/blob/master/matlab/LoadMeasurements.m). 
* The function converts the .measurements files to a python numpy array `npy`. The numpy array contains three columns: `[FID WhiskerLabels Angles]`, where FID corresponds to frame ID, whisker labels the whisker ID (0, 1, 2, ...) and the Angles the measured angle of traced whiskers in degrees. Angles are wrapped to 0-360 degrees. 

The function `conv_meas_py.m` loads the `.measurements` file using `LoadMeasurements.m` within the wrapper function `loadconvertMeasurements.m` (which also wraps the angles to 360 degrees) and unpacks the resulting Matlab struct into `[fid,wid,label,angle, facex, facey,score]`. 

    *    fid           - Video frame where the segment was found
    *    wid           - id for the segment on that frame
    *    label         - identity.  For tracking use -1 for *not a whisker* and 
    *                    0,1,2.. for whiskers.                                  
    *    angle         - mean angle at follicle
    *    face_x        - roughly, center of whisker pad, y coordinate           
    *    face_y        - roughly, center of whisker pad, y coordinate           
    *    score         - median score from tracing                              
Unfortunately, the whisker tracking output is not complete and we have to deal with missing frames. The script `conv_meas_py.m` deals with missing frames by linearly interpolating between missing values. **This is a very unsophisticated method and could and should be improved upon.**
Finally, `conv_meas_py.m` takes `fid, labels, angles` and saves it to a numpy array with the ending `_whiskermeasurements.npy`. 


