import requests

print('Hello World')
print('Getting a HTTP page')

#r = requests.get('https://www.moh.gov.sg/news-highlights/details/1-337-more-cases-discharged-611-new-cases-of-covid-19-infection-confirmed')
r = requests.get('https://www.moh.gov.sg/docs/librariesprovider5/pressroom/press-releases/moh-press-release---annex-b-(29-may-2020).pdf')
print('Status code is ', r.status_code)

# now print the response
content = r.text
#print(content)
#print(len(content))

#print(content.splitlines())

# break it into lines
lineArray = content.splitlines()
print('Number of lines in content is : ', len(lineArray))

# now parse through each line in the text

for lineNum, eachLine in enumerate(lineArray):
    print('Line #', lineNum, 'is ', eachLine)


