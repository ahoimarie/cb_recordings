# Processing of whisker measurements files
The measurements files and whisker files created by whiski are huge and impractical to use. 
Hence, we are going to convert them to contain the useful data. 

* Convert measurements data to .npy using the scripts in `/whiskiconversion`. The scripts depend on the module [npy-matlab](https://github.com/kwikteam/npy-matlab), which we already included in the kilosort2 clustering folder. They also depend on `LoadMeasurements.m` provided by [the Janelia whisker tracker](https://github.com/nclack/whisk/blob/master/matlab/LoadMeasurements.m). 
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



To compile the mexfiles, go to the whiskrootfolder (cd whiskrootfolder)
`mex -output `
mex -output share/whisk/matlab/LoadWhiskers share/whisk/matlab/src/whisker_io.mex.c -lwhisk -L'/Users/nb18422/Downloads/whisk-1.1.0d-Darwin/lib/whisk' -I'/Users/nb18422/Downloads/whisk-1.1.0d-Darwin/include'

mex -DLOAD_MEASUREMENTS -output share/whisk/matlab/LoadMeasurements share/whisk/matlab/src/measurements_io.mex.c -lwhisk -L./lib -I./include

mex -DLOAD_MEASUREMENTS -output LoadMeasurements src/measurements_io.mex.c -lwhisk -L./lib -I./include
