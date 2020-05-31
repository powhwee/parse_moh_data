import requests
import os
import subprocess
import re

# Filename definitions
fromFileName = '/tmp/moh.pdf'
toFileName = '/tmp/moh.txt'

# Function Definitions
def is_empty(string):
    ll = len(string.strip())
    return (ll == 0)

def downloadFile(url, fileName):
    with open(fileName, "wb") as file:
        response = requests.get(url)
        file.write(response.content)
        print('File ', fileName, ' downloaded with status code ', response.status_code)

def convertPDFtoText(fromFileName, toFileName):
  SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
  args = ["/usr/bin/pdftotext",
          '-enc',
          'UTF-8',
          fromFileName,
          toFileName]
  res = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
  output = res.stdout.decode('utf-8')
  print(output)


# Step 1
print('Step 1 - Getting MOH PDF file')
downloadFile('https://www.moh.gov.sg/docs/librariesprovider5/pressroom/press-releases/moh-press-release---annex-b-(29-may-2020).pdf', '/tmp/moh.pdf')

# Step 2

print('Convert PDF file to text file')
convertPDFtoText("/tmp/moh.pdf", "/tmp/moh.txt")

# Step 3
print('String separate lines together')
fd = open(toFileName)
count = 1
prevNonContinguousEmptyLine = 0
cummulativeStr = ''

outFile = open("/tmp/dorm_cases_time_series.txt", "w")

for x in fd:
    ## yy = x.strip()
    ## zz = '**' + yy + '**'
    ## print(len(yy), zz)
    if is_empty((x)):
        if prevNonContinguousEmptyLine >= 2:
            print ('Concatenated String ', cummulativeStr)
            outFile.write(cummulativeStr + '\n')
            cummulativeStr = ''
            prevNonContinguousEmptyLine = 0
        else: # discard
            cummulativeStr = ''
    else:  # not empty, then concatenate
        cummulativeStr = cummulativeStr + ' ' + x
        cummulativeStr = cummulativeStr.replace('\n', '').replace('\r', '')
        prevNonContinguousEmptyLine = prevNonContinguousEmptyLine + 1


outFile.close()