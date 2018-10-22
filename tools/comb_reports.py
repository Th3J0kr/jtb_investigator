#!/usr/bin/env python3
import os, sys, glob, json, csv, io, argparse, time

def parse_args():
    parser = argparse.ArgumentParser(description='Investigate from the command line')
    parser.add_argument('-r', '--remove', action='store_true', help = 'IPs or range to investigate separated by spaces (enclose in quotes)')
    parser.add_argument('-n', '--name', type=str, help='Filename of combined report. (e.g. investigation1) (Will still be in reports/<format>/<filename>.<filetype>)')
    args = parser.parse_args()
    return args

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

print('[Combing Reports]')

args = parse_args()
if args.remove:
    remove = True
for d in reportDirs:
    os.chdir(d)
    print('[*] Entering: {}'.format(os.getcwd()))
    if args.name:
        combinedFileName = args.name + '_combined.' + d
    else:
        combinedFileName = d + '_combined.' + d
    if not os.path.isfile(combinedFileName):
        if d == 'csv':
            print('[*] Initializing csv file...')
            fh = open(combinedFileName, 'w', newline='\n')
            csvWriter = csv.writer(fh, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
            csvWriter.writerow(['ip','domainName','status','ports','whoisInfo','asnNum','asnInfo'])
            fh.close()
    else:
        print('[*] Archiving old combined report...')
        newName = combinedFileName + '.old'
        os.rename(combinedFileName, str(int(time.time())) + '_' + newName)
        if d == 'csv':
            print('[*] Initializing CSV file')
            fh = open(combinedFileName, 'w', newline='\n')
            csvWriter = csv.writer(fh, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
            csvWriter.writerow(['ip','domainName','status','ports','whoisInfo','asnNum','asnInfo'])
            fh.close()
    with open(combinedFileName, 'a', newline='\n') as fc:
        for f in glob.glob("*." + d):
            if '_combined' not in f:
                print('[*] Combining report {}...'.format(f))
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
                print('[*] Saved reports to {}'.format(combinedFileName))
                if remove:
                    print('[!] Removing report {}'.format(f))
                    os.remove(f)
    fc.close()
    os.chdir(reportsPath)
print('[*] All done!')
    
