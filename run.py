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
# Basically, print out the stats in a file in a readable fashion
# Slips would be 0.25nm - 0.35nm
# Change peak detection width to be 0.25nm minimum
# Report per dataset
# Data I'm doing right now it 4nm
# Next one is 3nm
# Make how big the width is a input parameter and do stuff with it
# 3rd data set is 30nm

def read_csv_line(file_name):
    return_array = []
    with open(file_name, "r") as f:
        reader = csv.reader(f, delimiter=",")
        for i, line in enumerate(reader):
            # print('line[{}] = {}'.format(i, line))
            return_array.append(line)
    for i in range(0, len(return_array)):
        for j in range(0, len(return_array[0])):
            return_array[i][j] = float(return_array[i][j])
    return return_array


def find_csv_line_peaks(x, type, xlabel, ylabel, printout=False):

    peaks, _ = find_peaks(x, prominence=0.008, distance=85)
    y = x * (-1)
    valleys, _ = find_peaks(y, prominence=0.008, distance=85)
    if printout:
        print(peaks)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.plot(peaks, x[peaks], "xr")
        plt.plot(valleys, x[valleys], "ob")
        plt.plot(x)
        plt.legend(['Finished Chart'])
        plt.savefig(type + " Output Plot.jpg")

    peaks_array = []
    valley_array = []

    for peak in peaks:
        peaks_array.append([peak, x[peak]])

    for valley in valleys:
        valley_array.append([valley, x[valley]])

    points = {
        "peaks": peaks_array,
        "valleys": valley_array
    }

    plt.close()

    return points


def start(file_name, width_in_nm, printout_status=False):

    warnings.filterwarnings("ignore")

    csv_array = read_csv_line(file_name)

    if printout_status:
        file_name = ""
    else:
        file_name = file_name[:-4] + " "

    moving_average_steps_array = []
    moving_average_widths_array = []
    moving_average_slopes_array = []

    geometric_moving_average_steps_array = []
    geometric_moving_average_widths_array = []
    geometric_moving_average_slopes_array = []

    exponential_moving_average_steps_array = []
    exponential_moving_average_widths_array = []
    exponential_moving_average_slopes_array = []

    fourier_steps_array = []
    fourier_widths_array = []
    fourier_slopes_array = []

    nm_per_pixel = width_in_nm / len(csv_array[0])

    xlabel = "Distance (" + str(nm_per_pixel) + " nm/pixel)"
    ylabel = "Force (Volts)"
    fontsize = 15

    for i in range(0, len(csv_array)):

        if i != 0:
            printout_status = False

        if printout_status:
            print(i)

        for j in range(0, len(csv_array[i])):
            csv_array[i][j] = float(csv_array[i][j])

        if printout_status:
            print(csv_array[i])
            plt.plot(csv_array[i])
            plt.legend(['Unfiltered Data'])
            plt.xlabel(xlabel, fontsize=fontsize)
            plt.ylabel(ylabel, fontsize=fontsize)
            plt.savefig("Unfiltered Plot.jpg")
            plt.close()

        data = signal_cleanup.clean(csv_array[i])
        moving_average_data = data[0]
        geometric_moving_average_data = data[1]
        exponential_moving_average_data = data[2]
        fourier_data = data[3]

        if printout_status:
            print(moving_average_data)
            plt.plot(moving_average_data)
            plt.xlabel(xlabel, fontsize=fontsize)
            plt.ylabel(ylabel, fontsize=fontsize)
            plt.legend(['Moving Average Filtered Data'])
            plt.savefig("Moving Average Filtered Plot.jpg")
            plt.close()

            print(geometric_moving_average_data)
            plt.plot(geometric_moving_average_data)
            plt.xlabel(xlabel, fontsize=fontsize)
            plt.ylabel(ylabel, fontsize=fontsize)
            plt.legend(['Geometric Moving Average Filtered Data'])
            plt.savefig("Geometric Moving Average Filtered Plot.jpg")
            plt.close()

            print(exponential_moving_average_data)
            plt.plot(exponential_moving_average_data)
            plt.xlabel(xlabel, fontsize=fontsize)
            plt.ylabel(ylabel, fontsize=fontsize)
            plt.legend(['Exponential Moving Average Filtered Data'])
            plt.savefig("Exponential Moving Average Filtered Plot.jpg")
            plt.close()

            print(fourier_data)
            plt.plot(fourier_data)
            plt.xlabel(xlabel, fontsize=fontsize)
            plt.ylabel(ylabel, fontsize=fontsize)
            plt.legend(['Fourier Filtered Data'])
            plt.savefig("Fourier Filtered Plot.jpg")
            plt.close()

            plt.plot(csv_array[i], label="Unfiltered Data", zorder=0)
            plt.plot(exponential_moving_average_data, label="EMA Data", zorder=10)
            plt.plot(moving_average_data, label="MA Data", zorder=20)
            plt.plot(geometric_moving_average_data, label="GMA Data", zorder=30)
            plt.plot(fourier_data, label="Fourier Data", zorder=40)
            plt.legend()
            plt.xlabel(xlabel, fontsize=fontsize)
            plt.ylabel(ylabel, fontsize=fontsize)
            plt.savefig("Total Filtered Plot.jpg")
            plt.close()

        moving_average_points = find_csv_line_peaks(
            np.array(moving_average_data),
            "Moving Average",
            xlabel,
            ylabel,
            printout=printout_status)
        geometric_moving_average_points = find_csv_line_peaks(
            np.array(geometric_moving_average_data),
            "Geometric Moving Average",
            xlabel,
            ylabel,
            printout=printout_status)
        exponential_moving_average_points = find_csv_line_peaks(
            np.array(exponential_moving_average_data),
            "Exponential Moving Average",
            xlabel,
            ylabel,
            printout=printout_status)
        fourier_points = find_csv_line_peaks(
            np.array(fourier_data),
            "Fourier",
            xlabel,
            ylabel,
            printout=printout_status)

        moving_average_iter_steps_array = signal_cleanup.into_steps(moving_average_points)
        moving_average_iter_widths_array = signal_cleanup.into_widths(moving_average_points)
        moving_average_iter_slopes_array = signal_cleanup.into_slopes(moving_average_points)

        geometric_moving_average_iter_steps_array = signal_cleanup.into_steps(geometric_moving_average_points)
        geometric_moving_average_iter_widths_array = signal_cleanup.into_widths(geometric_moving_average_points)
        geometric_moving_average_iter_slopes_array = signal_cleanup.into_slopes(geometric_moving_average_points)

        exponential_moving_average_iter_steps_array = signal_cleanup.into_steps(exponential_moving_average_points)
        exponential_moving_average_iter_widths_array = signal_cleanup.into_widths(exponential_moving_average_points)
        exponential_moving_average_iter_slopes_array = signal_cleanup.into_slopes(exponential_moving_average_points)

        fourier_iter_steps_array = signal_cleanup.into_steps(fourier_points)
        fourier_iter_widths_array = signal_cleanup.into_widths(fourier_points)
        fourier_iter_slopes_array = signal_cleanup.into_slopes(fourier_points)

        for value in moving_average_iter_steps_array:
            moving_average_steps_array.append(value)
        for value in moving_average_iter_widths_array:
            moving_average_widths_array.append(value)
        for value in moving_average_iter_slopes_array:
            moving_average_slopes_array.append(value)

        for value in geometric_moving_average_iter_steps_array:
            geometric_moving_average_steps_array.append(value)
        for value in geometric_moving_average_iter_widths_array:
            geometric_moving_average_widths_array.append(value)
        for value in geometric_moving_average_iter_slopes_array:
            geometric_moving_average_slopes_array.append(value)

        for value in exponential_moving_average_iter_steps_array:
            exponential_moving_average_steps_array.append(value)
        for value in exponential_moving_average_iter_widths_array:
            exponential_moving_average_widths_array.append(value)
        for value in exponential_moving_average_iter_slopes_array:
            exponential_moving_average_slopes_array.append(value)

        for value in fourier_iter_steps_array:
            fourier_steps_array.append(value)
        for value in fourier_iter_widths_array:
            fourier_widths_array.append(value)
        for value in fourier_iter_slopes_array:
            fourier_slopes_array.append(value)

    width_label = "Width (" + str(nm_per_pixel) + " nm/pixel)"
    steps_label = "Step (Volts)"
    slopes_label = "Slope (nN/nm)"

    return {
        "Moving Average Widths Peaks": signal_cleanup.histogram(
            moving_average_widths_array,
            file_name + "Moving Average Widths",
            width_label,
            "Count of Widths",
            fontsize,
            nm_per_pixel),
        "Moving Average Steps Peaks": signal_cleanup.histogram(
            moving_average_steps_array,
            file_name + "Moving Average Steps",
            steps_label,
            "Count of Steps",
            fontsize,
            nm_per_pixel),
        "Moving Average Slopes Peaks": signal_cleanup.histogram(
            moving_average_slopes_array,
            file_name + "Moving Average Slopes",
            slopes_label,
            "Count of Slopes",
            fontsize,
            nm_per_pixel),

        "Geometric Moving Average Widths Peaks": signal_cleanup.histogram(
            geometric_moving_average_widths_array,
            file_name + "Geometric Moving Average Widths",
            width_label,
            "Count of Widths",
            fontsize,
            nm_per_pixel),
        "Geometric Moving Average Steps Peaks": signal_cleanup.histogram(
            geometric_moving_average_steps_array,
            file_name + " Geometric Moving Average Steps",
            steps_label,
            "Count of Steps",
            fontsize,
            nm_per_pixel),
        "Geometric Moving Average Slopes Peaks": signal_cleanup.histogram(
            geometric_moving_average_slopes_array,
            file_name + " Geometric Moving Average Slopes",
            slopes_label,
            "Count of Slopes",
            fontsize,
            nm_per_pixel),

        "Exponential Moving Average Widths Peaks": signal_cleanup.histogram(
            exponential_moving_average_widths_array,
            file_name + " Exponential Moving Average Widths",
            width_label,
            "Count of Widths",
            fontsize,
            nm_per_pixel),
        "Exponential Moving Average Steps Peaks": signal_cleanup.histogram(
            exponential_moving_average_steps_array,
            file_name + " Exponential Moving Average Steps",
            steps_label,
            "Count of Steps",
            fontsize,
            nm_per_pixel),
        "Exponential Moving Average Slopes Peaks": signal_cleanup.histogram(
            exponential_moving_average_slopes_array,
            file_name + " Exponential Moving Average Slopes",
            slopes_label,
            "Count of Slopes",
            fontsize,
            nm_per_pixel),

        "Fourier Widths Peaks": signal_cleanup.histogram(
            fourier_widths_array,
            file_name + " Fourier Widths",
            width_label,
            "Count of Widths",
            fontsize,
            nm_per_pixel),
        "Fourier Steps Peaks": signal_cleanup.histogram(
            fourier_steps_array,
            file_name + " Fourier Steps",
            steps_label,
            "Count of Steps",
            fontsize,
            nm_per_pixel),
        "Fourier Slopes Peaks": signal_cleanup.histogram(
            fourier_slopes_array,
            file_name + " Fourier Slopes",
            slopes_label,
            "Count of Slopes",
            fontsize,
            nm_per_pixel)
            }
