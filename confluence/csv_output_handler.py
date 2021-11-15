import csv

import util


class CsvOutputHandler:
    def __init__(self):
        self.csvfile = open('pages.csv', 'w', newline='')
        self.csv_writer = csv.writer(self.csvfile)

    def __del__(self):
        self.csvfile.close()

    def add(self, level, title, link, last_updated):
        row = util.generate_cvs_row(level, title, link, last_updated)
        self.csv_writer.writerow(row)
