# Welcome to my python project!

I completed this project for my second python class. Its purpose is to take a csv or binary file with some wave signal information and perform a fourier transform to make the signal cleaner. It displays a graph with both the original and clean wave in user-selected colors along with some information about the signal.

# How to run it:
For this project to work, make sure you install the TKinter, MatPlotLib, and Numpy packages for python.
Then, run the fourier_gui.py file. 
Click browse to open a signal file (the data folder inside the python project is opened by default).    
Open one of the noisy_signal files, select the plot colors, select the number of terms, and then plot the data.
You can save the plot you created in the top menu bar.

# Project file structure:
    Data folder: contains signal files to use with this program.
    Figures: Default save location for the plots you create.
    src: contains the main script and supporting methods
        - given: contains supporting methods. Most importantly fft.py which contains the FFT class to actually perform the fourier transform.
        - fourier_gui.py: contains the TKinter loop and the main method.