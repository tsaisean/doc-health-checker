import csv


class CsvOutputHandler:
    def __init__(self):
        self.csvfile = open('pages.csv', 'w', newline='')
        self.csv_writer = csv.writer(self.csvfile)

    def __del__(self):
        self.csvfile.close()

    def print(self, row):
        self.csv_writer.writerow(row)