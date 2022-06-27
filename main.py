from run import start
from print_results import print_results

if __name__ == '__main__':
    filename = "file.csv"
    print_results(start(filename, 3, printout_status=True), filename)
