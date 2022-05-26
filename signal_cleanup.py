# import matplotlib.pyplot as plt
import numpy

'''def moving_average_filter(x):
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
    return'''


def moving_average(x, w):
    return numpy.convolve(x, numpy.ones(w), 'valid') / w


'''def averaging_filter(x):
    y = []
    for index in range(0, len(x) // 2):
        y[index] = 0

    for index in range(0, len(x)):
        y[index // 2] = x[index]

    for index in range(0, len(y)):
        y[index] *= 0.5

    return y'''

'''def length_array(x):
    length = []
    for i in range(0, len(x)):
        length.append(i)
    return length'''


def clean(x):
    """fig = plt.figure(figsize=plt.figaspect(1.0))

    ax1 = fig.add_subplot(2, 2, 1)
    ax1.title.set_text('')

    ax2 = fig.add_subplot(2, 2, 2)
    ax2.title.set_text('')

    ax3 = fig.add_subplot(2, 2, 3)
    ax3.title.set_text('')

    ax4 = fig.add_subplot(2, 2, 4)
    ax4.title.set_text('')

    y1 = x
    y2 = moving_average(x, 10)
    y3 = moving_average(x, 20)
    y4 = moving_average(x, 40)

    length1 = length_array(y1)
    length2 = length_array(y2)
    length3 = length_array(y3)
    length4 = length_array(y4)

    ax1.plot(numpy.array(length1), numpy.array(y1))
    ax2.plot(numpy.array(length2), numpy.array(y2))
    ax3.plot(numpy.array(length3), numpy.array(y3))
    ax4.plot(numpy.array(length4), numpy.array(y4))
    fig.canvas.flush_events()
    plt.draw()

    plt.show()"""

    return moving_average(x, 40)
