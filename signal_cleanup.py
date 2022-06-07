import numpy
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


def moving_average(x, w):
    return numpy.convolve(x, numpy.ones(w), 'valid') / w


def clean(x):
    return moving_average(x, 40)


def into_steps(dictionary):
    valley_array = dictionary["valleys"]
    peak_array = dictionary["peaks"]

    steps_array = []

    valley_index = 0
    peak_index = 0

    if len(valley_array) > len(peak_array):
        valley_index += 1

    while valley_index != len(valley_array) and peak_index != len(peak_array):
        # peaks_array.append([peak, x[peak]])
        peak = peak_array[peak_index][1]
        valley = valley_array[valley_index][1]
        steps_array.append(peak - valley)

        valley_index += 1
        peak_index += 1

    return steps_array


def into_widths(dictionary):
    valley_array = dictionary["valleys"]
    peak_array = dictionary["peaks"]

    width_array = []

    valley_index = 0
    peak_index = 1

    if len(valley_array) < len(peak_array):
        peak_index += 1

    while valley_index != len(valley_array) and peak_index != len(peak_array):
        # peaks_array.append([peak, x[peak]])
        peak = peak_array[peak_index][0]
        valley = valley_array[valley_index][0]
        width_array.append(peak - valley)

        valley_index += 1
        peak_index += 1

    return width_array


def histogram(x, plot_name, low_threshold=0.0, high_threshold=10000.0):
    thresholded_x = []
    for value in x:
        if high_threshold >= value >= low_threshold:
            thresholded_x.append(value)

    n, bins, patches = plt.hist(thresholded_x, bins='auto')  # arguments are passed to np.histogram

    x_axis = []
    for i in range(0, len(bins) - 1):
        x_axis.append((bins[i] + bins[i + 1]) / 2)

    plt.plot(x_axis, n)

    peak_plot_x = []

    peaks, peaks2 = find_peaks(n, prominence=20)
    for point in n[peaks]:
        for i in range(0, len(n)):
            if point == n[i]:
                peak_plot_x.append(x_axis[i])

    plt.plot(peak_plot_x, n[peaks], "xr")

    plt.title(plot_name + " Histogram with 'auto' bins")
    # plt.show()
    plt.savefig(plot_name + ".png")
    plt.close()


def histogram_p(x, plot_name, low_threshold=0.0, high_threshold=10000.0):
    for j in range(1, 2000):
        if j%10 == 0:
            print(j)
            thresholded_x = []
            for value in x:
                if high_threshold >= value >= low_threshold:
                    thresholded_x.append(value)

            n, bins, patches = plt.hist(thresholded_x, bins='auto')  # arguments are passed to np.histogram

            x_axis = []
            for i in range(0, len(bins) - 1):
                x_axis.append((bins[i] + bins[i + 1]) / 2)

            plt.plot(x_axis, n)

            peak_plot_x = []
            peaks, peaks2 = find_peaks(n, prominence=j / 100)
            for point in n[peaks]:
                for i in range(0, len(n)):
                    if point == n[i]:
                        peak_plot_x.append(x_axis[i])

            plt.plot(peak_plot_x, n[peaks], "xr")
            plt.title(plot_name + " Histogram with 'auto' bins, " + str(j))
            plt.savefig(plot_name + "_" + str(j) + ".png")
            plt.close()
