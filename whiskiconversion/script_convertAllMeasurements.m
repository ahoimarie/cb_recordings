% Load and convert all measurements files in the folder
clear all

filepath = '/Volumes/bunaken/Marie/npx/';
filedirs = dir([filepath, 'MB*']);
% figdir = [filepath 'figs/'];
addpath(genpath('/Volumes/bunaken/Marie/npx_processing'))

for j = 1:length(filedirs)
    
    myKsDir = [filepath filedirs(j).name];
    addpath(myKsDir)
    name = filedirs(j).name;
%     Get mouse name
    mid = [name(1:5), '-',name(10:11)]; % . mouse ID
    filenameM = [myKsDir filesep mid(end-1:end) '_rc'];
    
    if ~exist([filenameM '.measurements'])
        mid = [name(1:5), '-',name(10)]; % . mouse ID
        filenameM = [myKsDir filesep mid(end) '_rc'];
    end
    % Convert measurements to numpy array
    if ~exist([filenameM(1:end-3) '_whiskermeasurements.npy'])
        fprintf('Creating %s. \n', [filenameM(1:end-3) '_whiskermeasurements.npy'])
        conv_meas_py(filenameM)
    else
        fprintf('File %s already exists. \n', [filenameM(1:end-3) '_whiskermeasurements.npy'])
        
    end
    
    
end
