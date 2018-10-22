#!/usr/bin/env python3
import os, sys, glob, json, csv, io

myPath = os.path.realpath(__file__).split('/')
pathLen = len(myPath) - 2
jtbPath = '/' + '/'.join(myPath[1:pathLen])
reportsPath = jtbPath + '/reports/'
try:
    os.chdir(reportsPath)
except:
    print('[!] Couldn\'t find reports directory. Did you move it?')
    sys.exit(0)

reportDirs = os.listdir('.')

for d in reportDirs:
    os.chdir(d)
    print('[*] Entering: {}'.format(os.getcwd()))
    combinedFileName = d + '_combined.' + d
    if not os.path.isfile(combinedFileName):
        if d == 'csv':
            fh = open(combinedFileName, 'w', newline='\n')
            csvWriter = csv.writer(fh, delimiter=',', quotechar='\'', quoting=csv.QUOTE_ALL)
            csvWriter.writerow(['ip','domainName','status','ports','whoisInfo','asnNum','asnInfo'])
            fh.close()
    with open(combinedFileName, 'a', newline='\n') as fc:
        for f in glob.glob("*." + d):
            if f != combinedFileName:
                with open(f, 'r') as fo:
                    if d == 'txt':
                        headingL = f.split('.')
                        heading = '.'.join(headingL[:(len(headingL)-2)])
                        report = fo.read()
                        fc.write(heading + ':\n')
                        fc.write(report + '\n')
                    elif d == 'csv':
                        csvWriter = csv.writer(fc, delimiter=',', quotechar='\'', quoting=csv.QUOTE_ALL)
                        csvReader = csv.reader(fo, delimiter=',', quotechar='\'', quoting=csv.QUOTE_ALL)
                        next(csvReader)
                        row = next(csvReader)
                        for i in row:
                            i.strip('\'')
                            try:
                                for n in i:
                                    n.strip('')
                            except:
                                pass
                        csvWriter.writerow(row)
                    elif d == 'json':
                        report = fo.read()
                        fc.write(report + '\n\n')
                fo.close()
    fc.close()
    os.chdir(reportsPath)
    
