import pickle
import os
import os.path as pth
import csv


def read_crawler_file(my_path):
    """
        Read data from csv file into dictionary.
    """
    if not pth.exists(my_path):
        my_file = open(my_path, "w+")
        my_file.close()
    my_result = {}
    if os.stat(my_path).st_size > 0:
        with open(my_path, mode="r") as inp:
            reader = csv.reader(inp)
            l = 0;
            for rows in reader:
                l=l+1
                if len(rows) == 2:
                    my_result[rows[0]] = rows[1]
            print("reading", l)
    return my_result


def write_crawler_file(my_path, my_data):
    if not pth.exists(my_path):
        my_file = open(my_path, "w+")
        my_file.close()
    print("writing", len(my_data))
    with open(my_path, "w") as csv_file:
        writer = csv.writer(csv_file)
        for key, value in my_data.items():
            writer.writerow([key, value])


def append_crawler_file(my_path, my_data):
    if not pth.exists(my_path):
        my_file = open(my_path, "w+")
        my_file.close()
    with open(my_path, "a") as csv_file:
        writer = csv.writer(csv_file)
        for key, value in my_data.items():
            writer.writerow([key, value])


def write_pickle_file(path, data):
    pickle.dump(data, open(path, "wb"))
