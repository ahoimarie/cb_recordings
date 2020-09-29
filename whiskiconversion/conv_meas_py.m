function out = conv_meas_py(filename)
% Convert whisker measurements data to npy
% NPY output array contains three columns: [FID WhiskerLabels Angles]
% where FID corresponds to frame ID, whisker labels the whisker ID (0, 1,
% 2, ...) and the Angles the measured angle of traced whiskers in degrees. 
% Angles are wrapped to 0-360 degrees.
%
% <filename>:   filename without file suffix
% example: filename = '/path/to/file/R_rc'
% 
% M. Tolkiehn 02/2020, University of Bristol.
% -------------------------------------------------------------
disp('Loading whisking data...')
[fid,wid,label,angle, facex, facey,score] = loadconvertMeasurements(filename);
disp('Done.')
disp('Linearly interpolate whisker traces.')

nwhisk = numel(unique(label))-1;

% Dealing with missing frames by interpolating between missing values
labelip = [];
angleip = [];
samip = [];
for j = 1:nwhisk % cycle through labels (whisker IDs from 0 to n)
    pos = angle(label==j-1)' ; % angle during recording
    sam = fid(label==j-1)' ;

    sid = 1:sam(end)+1;
    posi = NaN(size(sid)); %initialise
    posi(sam+1) = pos;
    labeli = (j-1)*ones(size(sid));   
    nanx = isnan(posi);
    t    = 1:numel(posi);
    posi(nanx) = interp1(t(~nanx), posi(~nanx), t(nanx));
    angleip = vertcat(angleip,posi');
    labelip = vertcat(labelip,labeli');
    samip = vertcat(samip,sid');    
end

% Interpolated values
angles = angleip;
fids = samip;
labels = labelip; 

disp('Save measurements to numpy array.');
measurements = [double(fids) labels angles];
writeNPY(measurements, [filename(1:end-3) '_whiskermeasurements.npy'])
out = [];

end