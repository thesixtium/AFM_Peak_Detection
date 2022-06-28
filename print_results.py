def print_results(results, filename):
    f = open(filename[:-4] + "_results.txt", "w")
    f.write(filename + " Results")
    f.write("\n")
    f.write("\n")

    types = ["Moving Average", "Geometric Moving Average", "Exponential Moving Average", "Fourier"]
    data = ["Widths", "Steps", "Slopes"]

    for type in types:
        f.write(type)
        f.write("\n")
        for set in data:
            f.write(set + ": ")
            f.write("\n")
            f.write("\tValues")
            f.write("\n")
            result_set = results[type + " " + set + " Peaks"]
            for result in result_set:
                f.write("\t- (" + str(result[0]) + ", " + str(result[1]) + ")")
                f.write("\n")
            if len(result_set) > 1:
                f.write("\tValue Math")
                f.write("\n")
                for i in range(1, len(result_set)):
                    f.write("\t- Result " +
                            str(i) +
                            "'s x-value is " +
                            str(round(result_set[i][0] / result_set[i-1][0], 2)) +
                            "x result " + str(i-1) +
                            "'s x-value")
                    f.write("\n")
                    f.write("\t- Result " +
                            str(i) +
                            "'s y-value is " +
                            str(round(result_set[i][1] / result_set[i - 1][1], 2)) +
                            "x result " + str(i - 1) +
                            "'s y-value")
                    f.write("\n")
            f.write("\n")
            f.write("\n")

    f.close()
