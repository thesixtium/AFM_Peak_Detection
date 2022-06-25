import numpy
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import pandas as pd
from scipy.fft import fft, ifft
from statistics import geometric_mean


def moving_average(arr, window_size):
    return numpy.convolve(arr, numpy.ones(window_size), 'valid') / window_size


def geometric_moving_average(arr, window_size):
    i = 0
    moving_averages = []
    while i < len(arr) - window_size + 1:
        this_window = arr[i: i + window_size]
        window = []
        for j in this_window:
            window.append(j + 10)
        moving_averages.append(geometric_mean(window) - 10)
        i += 1

    return moving_averages

def exponential_moving_average(arr, com=0.4):
    df = pd.DataFrame(arr).ewm(com=com).mean()
    returnValue = []
    for value in df.to_numpy():
        returnValue.append(value[0])
    return returnValue


def clean(x):
    return [moving_average(x, 40),
            geometric_moving_average(x, 40),
            exponential_moving_average(x),
            fourier_clean(x)]


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

def into_slopes(dictionary):
    valley_array = dictionary["valleys"]
    peak_array = dictionary["peaks"]

    slopes_array = []

    valley_index = 0
    peak_index = 1

    if len(valley_array) < len(peak_array):
        peak_index += 1

    while valley_index != len(valley_array) and peak_index != len(peak_array):
        # peaks_array.append([peak, x[peak]])
        peak_x = peak_array[peak_index][1]
        peak_y = peak_array[peak_index][0]
        valley_x = valley_array[valley_index][1]
        valley_y = valley_array[valley_index][0]
        slopes_array.append((peak_y-valley_y)/(peak_x-valley_x))

        valley_index += 1
        peak_index += 1

    return slopes_array


def histogram(x, plot_name, x_axis_name, y_axis_name, fontsize, low_threshold=0.0, high_threshold=10000.0):
    thresholded_x = []
    for value in x:
        if high_threshold >= value >= low_threshold:
            thresholded_x.append(value)

    floats = [float(i) for i in thresholded_x]
    n, bins, patches = plt.hist(numpy.array(floats), bins='auto')  # arguments are passed to np.histogram

    x_axis = []
    for i in range(0, len(bins) - 1):
        x_axis.append((bins[i] + bins[i + 1]) / 2)

    plt.plot(x_axis, n)
    plt.xlabel(x_axis_name, fontsize=fontsize)
    plt.ylabel(y_axis_name, fontsize=fontsize)

    peak_plot_x = []

    peaks, _ = find_peaks(n, prominence=20)
    for point in n[peaks]:
        for i in range(0, len(n)):
            if point == n[i]:
                peak_plot_x.append(x_axis[i])

    plt.plot(peak_plot_x, n[peaks], "xr")

    plt.title(plot_name + " Histogram with 'auto' bins")
    plt.savefig(plot_name + ".jpg")
    plt.close()

    return [peak_plot_x, n[peaks]]

def fourier_clean(x):

    fourier_data = fft(numpy.array(x))
    fourier_data2 = fourier_data
    fourier_data2[abs(fourier_data2) < 10] = 0

    y = ifft(fourier_data2)

    return y
