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

    peaks, _ = find_peaks(x, prominence=0.008)
    y = x * (-1)
    valleys, _ = find_peaks(y, prominence=0.008)
    if printout:
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


def histogram(x, low_threshold=0.0, high_threshold=100.0):
    thresholded_x = []
    for value in x:
        if high_threshold >= value >= low_threshold:
            thresholded_x.append(value)

    data = np.array(thresholded_x)

    mu, std = norm.fit(data)

    # best fit of data
    _ = plt.hist(thresholded_x, bins='auto')  # arguments are passed to np.histogram

    xmin, xmax = plt.xlim()
    y = np.linspace(xmin, xmax, 100)
    p = norm.pdf(y, mu, std)
    p2 = []

    for point in p:  # Why do we need this????
        p2.append(point * 100)

    plt.plot(y, p2)

    plt.title("Histogram with 'auto' bins")
    plt.show()


if __name__ == '__main__':
    run = 1
    csv_array = read_csv_line()
    steps_array = []
    widths_array = []
    for i in range(0, len(csv_array)):
        print(i)

        for j in range(0, len(csv_array[i])):
            csv_array[i][j] = float(csv_array[i][j])
        data = signal_cleanup.clean(csv_array[i])

        points = find_csv_line_peaks(np.array(data), i)

        iter_steps_array = signal_cleanup.into_steps(points)
        for value in iter_steps_array:
            steps_array.append(value)

        iter_widths_array = signal_cleanup.into_widths(points)
        for value in iter_widths_array:
            widths_array.append(value)

    signal_cleanup.histogram(widths_array, "Widths")
    signal_cleanup.histogram(steps_array, "Steps")
