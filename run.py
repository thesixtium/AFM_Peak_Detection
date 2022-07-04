import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import signal_cleanup
import warnings


# open stuff stuff in sm4
# Make sure EVERY graph has correct sized labels
# Make sure EVERY graph has a title
# fit gaussian
# write how many peaks / centers
# combine all graphs

# Penny Next Step:
# Make it so that it prints out batches with file name in front
# Try on other set of Penny data, see what happens
# Print out the average slip width and double slip width
# Data I'm doing right now it 4nm
# Next one is 3nm
# Make how big the width is a input parameter and do stuff with it
# 3rd data set is 30nm

# Document everything

def read_csv_line(file_name):
    """
    Reads CSV file into a 2D array of strings, then converts array of strings into
        an array of floats.

    :param file_name: file name / file path to read, including the file extension
    :return: 2D array of floats
    """

    # Initialize return array
    return_array = []

    # Read each line of csv file into return array
    with open(file_name, "r") as f:
        reader = csv.reader(f, delimiter=",")
        for i, line in enumerate(reader):
            return_array.append(line)

    # Convert each entry in 2D array into a float
    for i in range(0, len(return_array)):
        for j in range(0, len(return_array[0])):
            return_array[i][j] = float(return_array[i][j])

    return return_array


def find_csv_line_peaks(x, chart_type, x_label, y_label, distance, printout=False):
    """
    Find the peaks and valleys in a data set

    :param x: 1D array of the data set
    :param chart_type: What type of data is passed in (only used for output plot if printout is True)
    :param x_label: X-axis label (only used for output plot if printout is True)
    :param y_label: Y-axis label (only used for output plot if printout is True)
    :param distance: The minimum distance between peaks
    :param printout: Whether or not to print out the data in the form of a saved graph
    :return: A dictionary with 'peaks' and 'valleys' containing the peaks and valleys of 'x'
    """

    # Find the peaks based on scipy.signal's find_peaks method
    peaks, _ = find_peaks(x, prominence=0.008, distance=distance)

    # Inverse graph over the x-axis so find_peaks can be applied again
    y = x * (-1)

    # Find the peaks based on scipy.signal's find_peaks method
    valleys, _ = find_peaks(y, prominence=0.008, distance=distance)

    if printout:
        # Print out a chart showing the peaks and valleys overlayed on the data set
        print(peaks)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.plot(peaks, x[peaks], "xr")
        plt.plot(valleys, x[valleys], "ob")
        plt.plot(x)
        plt.legend(['Finished Chart'])
        plt.savefig(chart_type.replace(" ", "_") + "_Output_Plot.jpg")
        plt.close()

    # Initialize empty arrays
    peaks_array = []
    valley_array = []

    # Assemble the peaks array
    for peak in peaks:
        peaks_array.append([peak, x[peak]])

    # Assemble the valley array
    for valley in valleys:
        valley_array.append([valley, x[valley]])

    # Assemble the return dictionary
    points = {
        "peaks": peaks_array,
        "valleys": valley_array
    }

    return points


def start(file_name, width_in_nm, printout_status=False):
    """
    The start of the program, to be called by an outside main function

    :param file_name: the CSV file to use, extension included
    :param width_in_nm: how wide the sample is in nanometers
    :param printout_status: whether or not to give a detailed print out of all steps
    :return: an extensive dictionary of the steps, widths, and slopes for each filter type
    """

    # Ignore warnings because they're annoying (although I should probably take care of them)
    warnings.filterwarnings("ignore")

    # Read the CSV file
    csv_array = read_csv_line(file_name)

    # If printing out, remove the file name to make everything more clear
    if printout_status:
        file_name = ""
    else:
        file_name = file_name[:-4] + " "

    # Initialize all MA arrays
    moving_average_steps_array = []
    moving_average_widths_array = []
    moving_average_slopes_array = []

    # Initialize all GMA arrays
    geometric_moving_average_steps_array = []
    geometric_moving_average_widths_array = []
    geometric_moving_average_slopes_array = []

    # Initialize all EMA arrays
    exponential_moving_average_steps_array = []
    exponential_moving_average_widths_array = []
    exponential_moving_average_slopes_array = []

    # Initialize all Fourier arrays
    fourier_steps_array = []
    fourier_widths_array = []
    fourier_slopes_array = []

    # Initialize pixels to nanometers conversion
    nm_per_pixel = width_in_nm / len(csv_array[0])
    minimum_nm_between_peaks = 25

    # Initialize all graph labels and font sizes
    xlabel = "Distance (" + str(nm_per_pixel) + " nm/pixel)"
    ylabel = "Force (Volts)"
    fontsize = 15

    # Go through every row of the array (ie. go through each row of the CSV file)
    for i in range(0, len(csv_array)):

        # Don't printout anything other than the first row
        if i != 0:
            printout_status = False

        # Make everything a float
        for j in range(0, len(csv_array[i])):
            csv_array[i][j] = float(csv_array[i][j])

        # Process all the data through the different filters
        data = signal_cleanup.clean(csv_array[i])
        moving_average_data = data[0]
        geometric_moving_average_data = data[1]
        exponential_moving_average_data = data[2]
        fourier_data = data[3]

        # Print out unfiltered and filtered data
        if printout_status:
            print("Unfiltered Data: " + str(csv_array[i]))
            plt.plot(csv_array[i])
            plt.legend(['Unfiltered Data'])
            plt.xlabel(xlabel, fontsize=fontsize)
            plt.ylabel(ylabel, fontsize=fontsize)
            plt.savefig("Unfiltered_Plot.jpg")
            plt.close()

            print("MA: " + str(moving_average_data))
            plt.plot(moving_average_data)
            plt.xlabel(xlabel, fontsize=fontsize)
            plt.ylabel(ylabel, fontsize=fontsize)
            plt.legend(['Moving Average Filtered Data'])
            plt.savefig("Moving_Average_Filtered_Plot.jpg")
            plt.close()

            print("GMA: " + str(geometric_moving_average_data))
            plt.plot(geometric_moving_average_data)
            plt.xlabel(xlabel, fontsize=fontsize)
            plt.ylabel(ylabel, fontsize=fontsize)
            plt.legend(['Geometric Moving Average Filtered Data'])
            plt.savefig("Geometric_Moving_Average_Filtered_Plot.jpg")
            plt.close()

            print("EMA: " + str(exponential_moving_average_data))
            plt.plot(exponential_moving_average_data)
            plt.xlabel(xlabel, fontsize=fontsize)
            plt.ylabel(ylabel, fontsize=fontsize)
            plt.legend(['Exponential Moving Average Filtered Data'])
            plt.savefig("Exponential_Moving_Average_Filtered_Plot.jpg")
            plt.close()

            print("fourier: " + str(fourier_data))
            plt.plot(fourier_data)
            plt.xlabel(xlabel, fontsize=fontsize)
            plt.ylabel(ylabel, fontsize=fontsize)
            plt.legend(['Fourier Filtered Data'])
            plt.savefig("Fourier_Filtered_Plot.jpg")
            plt.close()

            print("mix_of_data")
            plt.plot(csv_array[i], label="Unfiltered Data", zorder=0)
            plt.plot(exponential_moving_average_data, label="EMA Data", zorder=10)
            plt.plot(moving_average_data, label="MA Data", zorder=20)
            plt.plot(geometric_moving_average_data, label="GMA Data", zorder=30)
            plt.plot(fourier_data, label="Fourier Data", zorder=40)
            plt.legend()
            plt.xlabel(xlabel, fontsize=fontsize)
            plt.ylabel(ylabel, fontsize=fontsize)
            plt.savefig("Total_Filtered_Plot.jpg")
            plt.close()

        # Find the peaks and valleys of the data passed through a MA filter
        moving_average_points = find_csv_line_peaks(
            np.array(moving_average_data),
            "Moving Average",
            xlabel,
            ylabel,
            ((1 / nm_per_pixel) * minimum_nm_between_peaks * 0.01),
            printout=printout_status)

        # Find the peaks and valleys of the data passed through a GMA filter
        geometric_moving_average_points = find_csv_line_peaks(
            np.array(geometric_moving_average_data),
            "Geometric Moving Average",
            xlabel,
            ylabel,
            ((1 / nm_per_pixel) * minimum_nm_between_peaks * 0.01),
            printout=printout_status)

        # Find the peaks and valleys of the data passed through a EMA filter
        exponential_moving_average_points = find_csv_line_peaks(
            np.array(exponential_moving_average_data),
            "Exponential Moving Average",
            xlabel,
            ylabel,
            ((1 / nm_per_pixel) * minimum_nm_between_peaks * 0.01),
            printout=printout_status)

        # Find the peaks and valleys of the data passed through a Fourier filter
        fourier_points = find_csv_line_peaks(
            np.array(fourier_data),
            "Fourier",
            xlabel,
            ylabel,
            ((1 / nm_per_pixel) * minimum_nm_between_peaks * 0.01),
            printout=printout_status)

        # Process peaks and valleys of the MA filtered data
        moving_average_iter_steps_array = signal_cleanup.into_steps(moving_average_points)
        moving_average_iter_widths_array = signal_cleanup.into_widths(moving_average_points)
        moving_average_iter_slopes_array = signal_cleanup.into_slopes(moving_average_points)

        # Process peaks and valleys of the GMA filtered data
        geometric_moving_average_iter_steps_array = signal_cleanup.into_steps(geometric_moving_average_points)
        geometric_moving_average_iter_widths_array = signal_cleanup.into_widths(geometric_moving_average_points)
        geometric_moving_average_iter_slopes_array = signal_cleanup.into_slopes(geometric_moving_average_points)

        # Process peaks and valleys of the GMA filtered data
        exponential_moving_average_iter_steps_array = signal_cleanup.into_steps(exponential_moving_average_points)
        exponential_moving_average_iter_widths_array = signal_cleanup.into_widths(exponential_moving_average_points)
        exponential_moving_average_iter_slopes_array = signal_cleanup.into_slopes(exponential_moving_average_points)

        # Process peaks and valleys of the Fourier filtered data
        fourier_iter_steps_array = signal_cleanup.into_steps(fourier_points)
        fourier_iter_widths_array = signal_cleanup.into_widths(fourier_points)
        fourier_iter_slopes_array = signal_cleanup.into_slopes(fourier_points)

        # Split the values of the MA filtered data for easier time putting into a dictionary
        for value in moving_average_iter_steps_array:
            moving_average_steps_array.append(value)
        for value in moving_average_iter_widths_array:
            moving_average_widths_array.append(value)
        for value in moving_average_iter_slopes_array:
            moving_average_slopes_array.append(value)

        # Split the values of the GMA filtered data for easier time putting into a dictionary
        for value in geometric_moving_average_iter_steps_array:
            geometric_moving_average_steps_array.append(value)
        for value in geometric_moving_average_iter_widths_array:
            geometric_moving_average_widths_array.append(value)
        for value in geometric_moving_average_iter_slopes_array:
            geometric_moving_average_slopes_array.append(value)

        # Split the values of the EMA filtered data for easier time putting into a dictionary
        for value in exponential_moving_average_iter_steps_array:
            exponential_moving_average_steps_array.append(value)
        for value in exponential_moving_average_iter_widths_array:
            exponential_moving_average_widths_array.append(value)
        for value in exponential_moving_average_iter_slopes_array:
            exponential_moving_average_slopes_array.append(value)

        # Split the values of the Fourier filtered data for easier time putting into a dictionary
        for value in fourier_iter_steps_array:
            fourier_steps_array.append(value)
        for value in fourier_iter_widths_array:
            fourier_widths_array.append(value)
        for value in fourier_iter_slopes_array:
            fourier_slopes_array.append(value)

    # Labels for all the charts
    width_label = "Width (" + str(nm_per_pixel) + " nm/pixel)"
    steps_label = "Step (Volts)"
    slopes_label = "Slope (nN/nm)"

    # Build and return the dictionary that gets returned
    return {
        "Moving Average Widths Peaks": signal_cleanup.histogram(
            moving_average_widths_array,
            file_name + "Moving_Average_Widths",
            width_label,
            "Count of Widths",
            fontsize,
            nm_per_pixel),
        "Moving Average Steps Peaks": signal_cleanup.histogram(
            moving_average_steps_array,
            file_name + "Moving_Average_Steps",
            steps_label,
            "Count of Steps",
            fontsize,
            nm_per_pixel),
        "Moving Average Slopes Peaks": signal_cleanup.histogram(
            moving_average_slopes_array,
            file_name + "Moving_Average_Slopes",
            slopes_label,
            "Count of Slopes",
            fontsize,
            nm_per_pixel),

        "Geometric Moving Average Widths Peaks": signal_cleanup.histogram(
            geometric_moving_average_widths_array,
            file_name + "Geometric_Moving_Average_Widths",
            width_label,
            "Count of Widths",
            fontsize,
            nm_per_pixel),
        "Geometric Moving Average Steps Peaks": signal_cleanup.histogram(
            geometric_moving_average_steps_array,
            file_name + "Geometric_Moving_Average_Steps",
            steps_label,
            "Count of Steps",
            fontsize,
            nm_per_pixel),
        "Geometric Moving Average Slopes Peaks": signal_cleanup.histogram(
            geometric_moving_average_slopes_array,
            file_name + "Geometric_Moving_Average_Slopes",
            slopes_label,
            "Count of Slopes",
            fontsize,
            nm_per_pixel),

        "Exponential Moving Average Widths Peaks": signal_cleanup.histogram(
            exponential_moving_average_widths_array,
            file_name + " Exponential_Moving_Average_Widths",
            width_label,
            "Count of Widths",
            fontsize,
            nm_per_pixel),
        "Exponential Moving Average Steps Peaks": signal_cleanup.histogram(
            exponential_moving_average_steps_array,
            file_name + " Exponential_Moving_Average_Steps",
            steps_label,
            "Count of Steps",
            fontsize,
            nm_per_pixel),
        "Exponential Moving Average Slopes Peaks": signal_cleanup.histogram(
            exponential_moving_average_slopes_array,
            file_name + " Exponential_Moving_Average_Slopes",
            slopes_label,
            "Count of Slopes",
            fontsize,
            nm_per_pixel),

        "Fourier Widths Peaks": signal_cleanup.histogram(
            fourier_widths_array,
            file_name + " Fourier_Widths",
            width_label,
            "Count of Widths",
            fontsize,
            nm_per_pixel),
        "Fourier Steps Peaks": signal_cleanup.histogram(
            fourier_steps_array,
            file_name + " Fourier_Steps",
            steps_label,
            "Count of Steps",
            fontsize,
            nm_per_pixel),
        "Fourier Slopes Peaks": signal_cleanup.histogram(
            fourier_slopes_array,
            file_name + " Fourier_Slopes",
            slopes_label,
            "Count of Slopes",
            fontsize,
            nm_per_pixel)
    }
