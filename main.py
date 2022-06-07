import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import signal_cleanup
from scipy.stats import norm

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


def read_csv_line():
    return_array = []
    with open("file.csv", "r") as f:
        reader = csv.reader(f, delimiter=",")
        for i, line in enumerate(reader):
            # print('line[{}] = {}'.format(i, line))
            return_array.append(line)
    for i in range(0, len(return_array)):
        for j in range(0, len(return_array[0])):
            return_array[i][j] = float(return_array[i][j])
    return return_array


def find_csv_line_peaks(x, number, printout=False):

    # Try widths again
    # Try combining prominence and widths
    # about 0.3 nm
    # openturns gaussian distribution of stuff

    peaks, _ = find_peaks(x, prominence=0.008, distance=85)
    y = x * (-1)
    valleys, _ = find_peaks(y, prominence=0.008, distance=85)
    if printout:
        print(peaks)
        plt.plot(peaks, x[peaks], "xr")
        plt.plot(valleys, x[valleys], "ob")
        plt.plot(x)
        plt.legend(['Finished Chart'])
        # plt.show()
        plt.savefig(str(number) + "_output_plot.png")

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


if __name__ == '__main__':
    printout_status = False

    csv_array = read_csv_line()
    steps_array = []
    widths_array = []
    for i in range(0, len(csv_array)):
    # for i in range(0, 1):
        print(i)

        for j in range(0, len(csv_array[i])):
            csv_array[i][j] = float(csv_array[i][j])

        if printout_status:
            print(csv_array[i])
            plt.plot(csv_array[i])
            plt.legend(['Unfiltered Data'])
            # plt.show()
            plt.savefig(str(i) + "_unfiltered_plot.png")
            plt.close()

        data = signal_cleanup.clean(csv_array[i])

        if printout_status:
            print(data)
            plt.plot(data)
            plt.legend(['Filtered Data'])
            # plt.show()
            plt.savefig(str(i) + "_filtered_plot.png")
            plt.close()

        points = find_csv_line_peaks(np.array(data), i, printout=printout_status)

        iter_steps_array = signal_cleanup.into_steps(points)
        for value in iter_steps_array:
            steps_array.append(value)

        iter_widths_array = signal_cleanup.into_widths(points)
        for value in iter_widths_array:
            widths_array.append(value)

    signal_cleanup.histogram(widths_array, "Widths")
    signal_cleanup.histogram(steps_array, "Steps")
