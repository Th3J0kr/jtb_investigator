#!/usr/bin/env python3
import os, sys, glob, json, csv, io, argparse, time

class CombineReports:
    def __init__(self, name=None):
        self.name = name
        self.reportDirs = os.listdir('reports/')
        self.mainDir = os.path.dirname(os.path.realpath(sys.argv[0]))

    def main(self, name=None):
        if not name:
            name = self.name
        if self.reportDirs: 
            for d in self.reportDirs:
                direc = 'reports/' + d + '/'
                try:
                    os.chdir(direc)
                    print('Combining: {}'.format(os.getcwd()))

                    combinedFileName = name + '_combined.' + d
                    if not os.path.isfile(combinedFileName):
                        if d == 'csv':
                            print('Initializing csv file...')
                            fh = open(combinedFileName, 'w', newline='\n')
                            csvWriter = csv.writer(fh, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
                            csvWriter.writerow(['ip','domainName','status','ports','whoisInfo','asnNum','asnInfo', 'blackListed'])
                            fh.close()
                    else:
                        print('Archiving old combined report...')
                        newName = combinedFileName + '.old'
                        os.rename(combinedFileName, str(int(time.time())) + '_' + newName)
                        if d == 'csv':
                            print('Initializing CSV file')
                            fh = open(combinedFileName, 'w', newline='\n')
                            csvWriter = csv.writer(fh, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
                            csvWriter.writerow(['ip','domainName','status','ports','whoisInfo','asnNum','asnInfo', 'blackListed'])
                            fh.close()
                    with open(combinedFileName, 'a', newline='\n') as fc:
                        for f in glob.glob("*." + d):
                            if '_combined' not in f:
                                print('Combining report {}...'.format(f))
                                with open(f, 'r') as fo:
                                    if d == 'txt':
                                        headingL = f.split('.')
                                        heading = '.'.join(headingL[:(len(headingL)-2)])
                                        report = fo.read()
                                        fc.write(heading + ':\n')
                                        fc.write(report + '\n')
                                    elif d == 'csv':
                                        csvWriter = csv.writer(fc, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                                        csvReader = csv.reader(fo, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
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
                                print('Removing report {}'.format(f))
                                os.remove(f)
                    fc.close()
                    os.chdir(self.mainDir)
                except:
                    print('Could\'t find directory {}.'.format(direc))
            print('All done!')
        else:
            print('No report directories provided!')
        sys.exit(0)