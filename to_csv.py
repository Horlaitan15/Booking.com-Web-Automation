import csv

"""
    This file write the csv file.
"""


def write_csv(data, row):
    if row == 1:
        with open("Booking.csv", 'w') as f:
            writer = csv.writer(f)
            writer.writerows(data)
    else:
        with open("Booking.csv", 'a') as f:
            writer = csv.writer(f)
            writer.writerows(data)
