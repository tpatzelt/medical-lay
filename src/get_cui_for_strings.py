# This script returns UMLS CUIs based on an input file of strings, where each line in txt file is a separate string.
# If no results are found for a specific string, this will be noted in output and output file.
# Each set of results for a string is separated in the output file with '***'.

import argparse

import requests

parser = argparse.ArgumentParser(description='process user given parameters')
parser.add_argument('-k', '--apikey', required=False, dest='apikey',
                    help='enter api key from your UTS Profile',
                    default="43f9234c-4977-45f6-a440-2dda1b43d919")
parser.add_argument('-v', '--version', required=False, dest='version', default='current',
                    help='enter version example-2015AA')
parser.add_argument('-o', '--outputfile', required=True, dest='outputfile',
                    help='enter a name for your output file')
parser.add_argument('-s', '--sabs', required=False, dest='sabs',
                    help='enter a comma-separated list of vocabularies without spaces, like MSH,SNOMEDCT_US,RXNORM')
parser.add_argument('-t', '--ttys', required=False, dest='ttys',
                    help='enter a comma-separated list of term types, like PT,SY,IN')
parser.add_argument('-i', '--inputfile', required=True, dest='inputfile',
                    help='enter a name for your input file')

args = parser.parse_args()
apikey = args.apikey
version = args.version
outputfile = args.outputfile
inputfile = args.inputfile
sabs = args.sabs
ttys = args.ttys

base_uri = 'https://uts-ws.nlm.nih.gov'
string_list = []

with open(inputfile, encoding='utf-8') as f:
    for line in f:
        if line.isspace() is False:
            strings = line.strip()
            string_list.append(strings)
        else:
            continue

print(string_list)

with open(outputfile, 'w', encoding='utf-8') as o:
    for string in string_list:
        page = 0

        o.write('SEARCH STRING: ' + string + '\n' + '\n')

        while True:
            page += 1
            path = '/search/' + version
            query = {'string': string, 'apiKey': apikey, 'rootSource': sabs, 'termType': ttys,
                     'pageNumber': page}
            output = requests.get(base_uri + path, params=query)
            output.encoding = 'utf-8'
            # print(output.url)

            outputJson = output.json()
            results = (([outputJson['result']])[0])['results']

            if len(results) == 0:
                if page == 1:
                    print('No results found for ' + string + '\n')
                    o.write('No results found.' + '\n' + '\n')
                    break
                else:
                    break

            for item in results:
                o.write(
                    'UI: ' + item['ui'] + '\n' + 'Name: ' + item['name'] + '\n' + 'URI: ' + item[
                        'uri'] + '\n' + 'Source Vocabulary: ' + item['rootSource'] + '\n' + '\n')

        o.write('***' + '\n' + '\n')
