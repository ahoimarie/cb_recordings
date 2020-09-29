function [fid,wid,label,angle, facex, facey,score] = loadconvertMeasurements(filenameM)
%This function loads the whisking data measurements file and converts its
%contents (struct) into individual variables (more RAM efficient).
% It takes as input the file path to the .measurements file.
% 
% 
%   <filenameM>     is the path to a .measurements file.
%   <measurements> is a struct array with the following fields:
%
%    fid           - Video frame where the segment was found
%    wid           - id for the segment on that frame
%    label         - identity.  For tracking use -1 for `not a whisker` and 
%                    0,1,2.. for whiskers.                                  
%    face_x        - roughly, center of whisker pad, y coordinate           
%    face_y        - roughly, center of whisker pad, y coordinate           
%    length        - path length in pixels                                  
%    score         - median score from tracing                              
%    angle         - mean angle at follicle
%    curvature     - mean curvature (1/mm)
%    follicle_x    - follicle position: x (px)
%    follicle_y    - follicle position: y (px)
%    tip_x         - tip position: x (px)
%    tip_y         - tip position: y (px)
% 
% Created by Marie Tolkiehn (2020, University of Bristol)
% -------------------------------------------------------------

measurements = LoadMeasurements([filenameM '.measurements']);

fid = vertcat(measurements.fid);
wid = vertcat(measurements.wid);
label = vertcat(measurements.label);
angle = wrapTo360(vertcat(measurements.angle));
facex = vertcat(measurements.face_x);
facey = vertcat(measurements.face_y);
score = vertcat(measurements.score);


% Whisking time stamps
%         id                                                                              
%         time                                                                            
%         x                                                                               
%         y                                                                               
%         thick                                                                           
%         scores 


end

