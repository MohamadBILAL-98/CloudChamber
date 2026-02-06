# CloudChamber
Python code to take images of a cloud chamber and to analyse them: optical correction matrix, optical correction and fiducial volume, generation of the background image, raw clustering, merging of fragmented clusters. removing correlated cluster, final results. There are two applications : thoron lifetime and Radon in air measurement.   

## Configuration data
The code cloudChamberCommonCode.py defined all data that configures a given data taking period and analysis

## Image Data Taking
In src/acq/ directory the python3 script webcam_dacq.py to take a series of images of the webcam (to be used at the end of the day with FULL HD WEBCAM using a linux computer). See specifications of the webcam FULL HD in the doc directory.

## Optical Aberration correction and Image Fiducial Area
In src/acq/ directory the python3 script chessBoard_CameraCalibrationProcess.py performs the optical aberration correction (using the chess board image in data/ImageDamier_FullResolution/ ) and selects the fiducial area of the image in which the radioactive tracks wil be reconstructed ans analyzed.

## Filtering of corrected images
In src/rec/ directory the python3 script
filteringProcess.py  performs :
- the calculation of the background of the images is calculated for a time period of timePeriod images. In the calculation, to avoid correlations, considered image a distance by timeStep images and the pixel are kept if the light different is less and seuilDiff. The background image are named bck_*
- the background contribution is substract form each corrected image and are named diff_*
- The image is then binarized 0 or 255, depending on a seuil value seuil. The binarized images are named bina_*
- The binarized image is filtered. Very small cluster, less than 5x5 are removed, setting pixel values to zero. After filtering the image a named filt_*
- At the end of the filtering, the average occupancy over a certains interval of images (integrationTime expressed as a number of Image). Only images every deltaTimeStep in unit of images are considered to avoid correlations. The error of the averaged pixel occupancy is measured from the statistical fluctuation in the considered interval of averaging. These results is presented as a plot and the data occupancy point can be fitted to a constant or exponential plus constant function. 
- this script can be executed with a filtering option set to zero, on order to performed only the occupancy and fitting process. 
