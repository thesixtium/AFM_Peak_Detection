import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import signal_cleanup
import warnings

'''
Horizontal distance between valleys / peaks -> Recursivley in each line
Slopes between points -> Recursivley in each line
What is the center / width of histogram -> End of program run
 - Slopes
 - Height differences
Fit to big scary math equations -> End of program run

Get drop from top to bottom of right side
Slopes of the left sides
Histrogram count of step heights

fit giant equations to the histograms 

'''


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


def find_csv_line_peaks(x, type, printout=False):

    peaks, _ = find_peaks(x, prominence=0.008, distance=85)
    y = x * (-1)
    valleys, _ = find_peaks(y, prominence=0.008, distance=85)
    if printout:
        print(peaks)
        plt.xlabel("lateral force (nN)")
        plt.ylabel("tip base position (nm)")
        plt.plot(peaks, x[peaks], "xr")
        plt.plot(valleys, x[valleys], "ob")
        plt.plot(x)
        plt.legend(['Finished Chart'])
        plt.savefig(type + "_output_plot.png")

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


def start(file_name, printout_status=False):
    warnings.filterwarnings("ignore")

    csv_array = read_csv_line(file_name)

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
            plt.xlabel("Distance (nm)")
            plt.ylabel("Force (nN)")
            plt.savefig("unfiltered_plot.png")
            plt.close()

        data = signal_cleanup.clean(csv_array[i])
        moving_average_data = data[0]
        geometric_moving_average_data = data[1]
        exponential_moving_average_data = data[2]
        fourier_data = data[3]

        if printout_status:
            print(moving_average_data)
            plt.plot(moving_average_data)
            plt.xlabel("Distance (nm)")
            plt.ylabel("Force (nN)")
            plt.legend(['Moving Average Filtered Data'])
            plt.savefig("moving_average_filtered_plot.png")
            plt.close()

            print(geometric_moving_average_data)
            plt.plot(geometric_moving_average_data)
            plt.xlabel("Distance (nm)")
            plt.ylabel("Force (nN)")
            plt.legend(['Geometric Moving Average Filtered Data'])
            plt.savefig("geometric_moving_average_filtered_plot.png")
            plt.close()

            print(exponential_moving_average_data)
            plt.plot(exponential_moving_average_data)
            plt.xlabel("Distance (nm)")
            plt.ylabel("Force (nN)")
            plt.legend(['Exponential Moving Average Filtered Data'])
            plt.savefig("exponential_moving_average_filtered_plot.png")
            plt.close()

            print(fourier_data)
            plt.plot(fourier_data)
            plt.xlabel("Distance (nm)")
            plt.ylabel("Force (nN)")
            plt.legend(['Fourier Filtered Data'])
            plt.savefig("fourier_filtered_plot.png")
            plt.close()

            plt.plot(csv_array[i], label="Unfiltered Data", zorder=0)
            plt.plot(exponential_moving_average_data, label="EMA Data", zorder=10)
            plt.plot(moving_average_data, label="MA Data", zorder=20)
            plt.plot(geometric_moving_average_data, label="GMA Data", zorder=30)
            plt.plot(fourier_data, label="Fourier Data", zorder=40)
            plt.legend()
            plt.xlabel("Distance (nm)")
            plt.ylabel("Force (nN)")
            plt.savefig("total_filtered_plot.png")
            plt.close()

        moving_average_points = find_csv_line_peaks(np.array(moving_average_data), "moving_average", printout=printout_status)
        geometric_moving_average_points = find_csv_line_peaks(np.array(geometric_moving_average_data), "geometric_moving_average", printout=printout_status)
        exponential_moving_average_points = find_csv_line_peaks(np.array(exponential_moving_average_data), "exponential_moving_average", printout=printout_status)
        fourier_points = find_csv_line_peaks(np.array(fourier_data), "fourier", printout=printout_status)

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

    return {
        "Moving Average Widths Peaks": signal_cleanup.histogram(
            moving_average_widths_array,
            file_name + " Moving Average Widths",
            "Width (nm)",
            "Count of Widths"),
        "Moving Average Steps Peaks": signal_cleanup.histogram(
            moving_average_steps_array,
            file_name + " Moving Average Steps",
            "Step (nN)",
            "Count of Steps"),
        "Moving Average Slopes Peaks": signal_cleanup.histogram(
            moving_average_slopes_array,
            file_name + " Moving Average Slopes",
            "Slope (nN/nm)",
            "Count of Slopes"),

        "Geometric Moving Average Widths Peaks": signal_cleanup.histogram(
            geometric_moving_average_widths_array,
            file_name + " Geometric Moving Average Widths",
            "Width (nm)",
            "Count of Widths"),
        "Geometric Moving Average Steps Peaks": signal_cleanup.histogram(
            geometric_moving_average_steps_array,
            file_name + " Geometric Moving Average Steps",
            "Step (nN)",
            "Count of Steps"),
        "Geometric Moving Average Slopes Peaks": signal_cleanup.histogram(
            geometric_moving_average_slopes_array,
            file_name + " Geometric Moving Average Slopes",
            "Slope (nN/nm)",
            "Count of Slopes"),

        "Exponential Moving Average Widths Peaks": signal_cleanup.histogram(
            exponential_moving_average_widths_array,
            file_name + " Exponential Moving Average Widths",
            "Width (nm)",
            "Count of Widths"),
        "Exponential Moving Average Steps Peaks": signal_cleanup.histogram(
            exponential_moving_average_steps_array,
            file_name + " Exponential Moving Average Steps",
            "Step (nN)",
            "Count of Steps"),
        "Exponential Moving Average Slopes Peaks": signal_cleanup.histogram(
            exponential_moving_average_slopes_array,
            file_name + " Exponential Moving Average Slopes",
            "Slope (nN/nm)",
            "Count of Slopes"),

        "Fourier Widths Peaks": signal_cleanup.histogram(
            fourier_widths_array,
            file_name + " Fourier Widths",
            "Width (nm)",
            "Count of Widths"),
        "Fourier Steps Peaks": signal_cleanup.histogram(
            fourier_steps_array,
            file_name + " Fourier Steps",
            "Step (nN)",
            "Count of Steps"),
        "Fourier Slopes Peaks": signal_cleanup.histogram(
            fourier_slopes_array,
            file_name + " Fourier Slopes",
            "Slope (nN/nm)",
            "Count of Slopes")
            }
