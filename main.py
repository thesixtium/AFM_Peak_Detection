import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


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
    return return_array


def find_csv_line_peaks(x, m=1.0):
    peaks, _ = find_peaks(x, distance=(20 * m))
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
    plt.close()


if __name__ == '__main__':
    run = 1
    csv_array = read_csv_line()
    print(len(csv_array[0]))
    for j in range(0, len(csv_array[0])):
        csv_array[0][j] = float(csv_array[0][j])
    if run == 0:
        for i in range(5, 200):
            find_csv_line_peaks(np.array(csv_array[0]), (i / 100))
    else:
        for i in range(200, 400):
            find_csv_line_peaks(np.array(csv_array[0]), (i / 100))
