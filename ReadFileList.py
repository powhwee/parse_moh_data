import os
import glob
import re
from datetime import datetime

# Get list of files in a directory
def file_browser():
    return [f for f in glob.glob("/home/phtan/mohpr/*.pdf")]


# Extract the date from the filename
def extract_date_from_filename(ff):
    mm = re.match(r'.*/(2020.*).pdf', ff)
    return mm.group(1)


# main program
list_of_files = file_browser()
print(list_of_files)

for ff in list_of_files:
    ddstr = extract_date_from_filename(ff)
    dd = datetime.strptime(ddstr, '%Y-%m-%d')
    print(ff, dd)


