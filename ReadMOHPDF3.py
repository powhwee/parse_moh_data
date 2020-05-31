import requests
import os
import subprocess
import re
import glob
from datetime import datetime

# define the folder to scan
#folder_to_scan = '/tmp/*.pdf'
folder_to_scan = '/home/phtan/mohpr/*.pdf'

# Function Definitions
def is_empty(string):
    ll = len(string.strip())
    return (ll == 0)


def download_file(url, fileName):
    with open(fileName, "wb") as file:
        response = requests.get(url)
        file.write(response.content)
        print('File ', fileName, ' downloaded with status code ', response.status_code)


def convert_pdf_to_text(from_file_name, to_file_name):
    args = ["/usr/bin/pdftotext",
            '-enc',
            'UTF-8',
            from_file_name,
            to_file_name]
    res = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output = res.stdout.decode('utf-8')
    print(output)


# Parse PDF and convert to a Text File


def parse_pdf_and_append_to_txt_file(pdf_file_name, target_csv_file, date_str):
    # convert pdf to text first
    mm = re.match(r'(.*).pdf', pdf_file_name)
    to_txt_file_name = mm.group(1) + ".txt"
    print('DEBUG >> ' + to_txt_file_name)

    convert_pdf_to_text(pdf_file_name, to_txt_file_name)

    count = 1
    prev_non_contiguous_empty_line = 0
    cumulative_str = ''
    fd = open(to_txt_file_name)
    out_csv_file = target_csv_file
    for x in fd:

        if is_empty((x)):
            if prev_non_contiguous_empty_line >= 2:
                print('Concatenated String ', cumulative_str)
                m = re.match(r".*at (.*),.*total of ([0-9,]+)", cumulative_str)
                if (m != None):
                    nn = m.group(2)
                    nn = nn.replace(',', '')  # remove away '000s separator in numbers eg 2,353 to become 2353
                    print('Matched dorm, #cases : ', date_str + ', ' + m.group(1).upper().strip() + ',', nn)
                    out_csv_file.write(date_str + ', ' + m.group(1).upper() + ', ' + nn + '\n')
                cumulative_str = ''
                prev_non_contiguous_empty_line = 0
            else:  # discard
                cumulative_str = ''
        else:  # not empty, then concatenate
            cumulative_str = cumulative_str + ' ' + x
            cumulative_str = cumulative_str.replace('\n', '').replace('\r', '')
            prev_non_contiguous_empty_line = prev_non_contiguous_empty_line + 1


# Get list of files in a directory
def file_browser():
    return [f for f in glob.glob(folder_to_scan)]


# Extract the date from the filename
def extract_date_from_filename(ff):
    mm = re.match(r'.*/(2020.*).pdf', ff)
    return mm.group(1)


# ----------------------  MAIN PROGRAM STARTS ---------
#
#

print('START OF MAIN PROGRAM')

list_of_files = file_browser()
print(list_of_files)

target_csv_file = open('/tmp/dorm_cases_time_series.csv', 'w')

for ff in list_of_files:
    ddstr = extract_date_from_filename(ff)
    dd = datetime.strptime(ddstr, '%Y-%m-%d')
    parse_pdf_and_append_to_txt_file(ff, target_csv_file, ddstr)

target_csv_file.close()
