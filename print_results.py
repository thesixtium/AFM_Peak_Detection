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
            for result in results[type + " " + set + " Peaks"]:
                f.write("\t- (" + str(result[0]) + ", " + str(result[1]) + ")")
                f.write("\n")
            f.write("\n")
            f.write("\n")

    f.close()
