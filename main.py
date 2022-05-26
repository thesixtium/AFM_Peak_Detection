import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import signal_cleanup


def moving_average_filter(x):
    y = []
    a = 1 / 2
    b = 1 / 3
    for index in range(0, len(x)):
        if index == 0:
            y.append((x[index] + x[index + 1]) * a)
        if index == len(x)-1:
            y.append((x[index - 1] + x[index]) * a)
        else:
            y.append((x[index - 1] + x[index] + x[index + 1]) * b)
    return y

def averaging_filter(x):
    y = []
    for index in range(0, len(x) // 2):
        y[index] = 0

    for index in range(0, len(x)):
        y[index // 2] = x[index]

    for index in range(0, len(y)):
        y[index] *= 0.5

    return y

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


def find_csv_line_peaks(x, m=1.0):
    # best is 0.008
    """peaks, _ = find_peaks(x, distance=(20 * m))
    peaks2, _ = find_peaks(x, prominence=(1 * m))  # BEST!
    peaks3, _ = find_peaks(x, width=(20 * m))
    peaks4, _ = find_peaks(x, threshold=(
                0.4 * m))  # Required vertical distance to its direct neighbouring samples, pretty useless
    plt.subplot(2, 2, 1)
    plt.plot(peaks, x[peaks], "xr")
    plt.plot(x)
    plt.legend(['distance'])
    plt.subplot(2, 2, 2)
    plt.plot(peaks2, x[peaks2], "ob")
    plt.plot(x)
    plt.legend(['prominence'])
    plt.subplot(2, 2, 3)
    plt.plot(peaks3, x[peaks3], "vg")
    plt.plot(x)
    plt.legend(['width'])
    plt.subplot(2, 2, 4)
    plt.plot(peaks4, x[peaks4], "xk")
    plt.plot(x)
    plt.legend(['threshold'])
    plt.savefig(str(m) + "_output_plot.png")
    # plt.show()
    plt.close()"""

    peaks, _ = find_peaks(x, prominence=0.008)
    y = x*(-1)
    valleys, _ = find_peaks(y, prominence=0.008)
    plt.plot(peaks, x[peaks], "xr")
    plt.plot(valleys, x[valleys], "ob")
    plt.plot(x)
    plt.legend(['Finished Chart'])
    plt.show()

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

    return points


if __name__ == '__main__':
    run = 1
    csv_array = read_csv_line()
    print(len(csv_array[0]))

    for j in range(0, len(csv_array[1])):
        csv_array[0][j] = float(csv_array[1][j])
    data = signal_cleanup.clean(csv_array[1])

    points = find_csv_line_peaks(np.array(data))

    '''if run == 0:
        for i in range(5, 200):
            find_csv_line_peaks(np.array(data), (i / 100))
            print(i)
    else:
        for i in range(200, 400):
            find_csv_line_peaks(np.array(data), (i / 100))
            print(i)'''