# AFM Peak Detection

## General Description
This code is meant to automate the process of finding peaks and valleys in AFM data and do all the needed math, turning hours or days of work into under a minute of computing. This work was done under the guidance of [Dr. Philip Egberts](https://schulich.ucalgary.ca/contacts/philip-egberts).

### What It Does
This code does automatic peak detection and processing for data out of an [Atomic Force Microscopy](https://en.wikipedia.org/wiki/Atomic_force_microscopy) machine. The steps are as follows:
* Recieve the data in a CSV file, with each row being a pass on the sample
* The data is quite noisy when receive, therefore it is cleaned with a moving average filter
* Use [SciPy to find all the peaks and valleys](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html) of each row of the CSV file
* Plot all steps (distance from peak to valley) and widths (distance from peak to peak) in histograms
* Use [SciPy to find the peaks](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.find_peaks.html) on the histogram data

### Technologies Used
Python 3.8 is used with the following packages (all installed via ```pip install```):
* csv
* find_peaks from scipy.signal
* numpy
* matplotlib.pyplot

## Terminology Explanation
This is what one row of the raw CSV data looks like when plotted:
![unfiltered_plot](readme_imgs/unfiltered_plot.jpg)

This is what the above row of raw CSV data looks like when filtered by the moving filter mentioned in [What It Does](###-What-It-Does):
![filtered_plot](readme_imgs/filtered_plot.jpg)

This is a visual diagram of what steps and widths, mentioned in [What It Does](###-What-It-Does), are defined as throughout the project: 
![filtered_plot_explination](readme_imgs/filtered_plot_explination.jpg)

This is what the peaks and valleys of the row of filtered CSV from above will look like:
![output_plot](readme_imgs/output_plot.jpg)

These are the histograms of the Steps and Widths of all 1024 lines of data in the CSV data with a peak detection algorithm:

![Steps Histogram](readme_imgs/Steps.jpg?raw)
![Widths Histogram](readme_imgs/Widths.jpg?raw)


## Usage
Use this code however you want (except for distributing closed source versions)! Please note there are a few __magic numbers__ throughout the program that are calibration values. These numbers are calibrated specifically for the data I received, and may not work on your data.

## Contact
[My Website](https://thesixtium.github.io/)

[Dr. Philip Egberts](https://schulich.ucalgary.ca/contacts/philip-egberts)

## License
[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/): The GNU GPLv3 license is selected so you can do almost anything you want with this project, except distributing closed source versions.
