#!/usr/bin/env python3

import os, sys, argparse, math, csv, json
from investigation import Investigate, Host
from modules import UtcToLocal

class Main:
    
    def __init__(self, host=None, args=None):
       self.host = host
       self.args = args

    def parse_args(self):
        parser = argparse.ArgumentParser(description='Investigate from the command line')
        parser.add_argument('-i', '--ip', type=str, help = 'IP to investigate')
        parser.add_argument('-n', '--hostname', type=str, help ='Hostname to investigate')
        parser.add_argument('-r', '--report', type=str, help='Report to import')
        parser.add_argument('-d', '--disable', action='store_true', help='Disable auto investigate when starting with option')
        parser.add_argument('-f', '--format', type=str, help="Format to export to. Avoids prompt for CLI auto investigate.")
        parser.add_argument('-p', '--passive', action='store_true', help="Passive recon only. Doesn't run nmap or any scans that interact with the target itself.")
        parser.add_argument('-t', '--time', type=str, help="Convert time from UTC to Local Time and quit. (format: 2018-10-16 21:22:23)")
        parser.add_argument('-v', '--version', action='store_true', help='Print JTB version currently installed')
        self.args = parser.parse_args()

    def importInvestigation(self, filepath=None):
        if not filepath:
            print('Please provide a filepath of the investigation to import:')
            filepath = input('> ')

        fileParts = filepath.split('.')
        fileType = fileParts[-1]
        
        if not os.path.isfile(filepath):
            print('Couldn\'t find the file!')
        else:
            print('Importing Investigation {}'.format(filepath))

            inReport = []

            if fileType == 'txt':
                with open(filepath, 'r') as f:
                    report = f.readlines()
                    for line in report:
                        bits = line.split(' : ')
                        try:
                            if bits[1]:
                                inReport.append(bits[1])
                        except:
                            pass
            elif fileType == 'csv':
                with open(filepath, 'r') as f:
                    readCSV = csv.reader(f, delimiter=',', quotechar='\'', quoting=csv.QUOTE_ALL)
                    i = 0
                    for row in readCSV:
                        if i >= 1:
                            inReport = row
                        i = i + 1
            elif fileType == 'json':
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    for host in data:
                        for prop in data[host].items():
                            inReport.append(prop[1])
            f.close
       
            if len(inReport) == 7:
                self.host = Host(ip=inReport[0], domainName=inReport[1], status=inReport[2], ports=inReport[3], 
                                whoisInfo=inReport[4], asnNum=inReport[5], asnInfo=inReport[6])
            else:
                print('Wrong number of arguments in saved report')
                print(inReport)

    def printVersion(self):
        print()
        print('=-'*21)
        print('= JTB Investigator Version: 1.0 \t=-')
        print('=-'*21)
        print('= Author: Th3J0kr \t\t\t=-')
        print('=-'*29)
        print('= https://www.github.com/th3J0kr/jtb_investigator \t=-')
        print('=-'*29)
        pVersion = sys.version
        pVersion = pVersion.split(' ')
        print('= Python version {} \t\t\t=-'.format(pVersion[0]))
        pathLen = math.ceil(len(os.path.realpath(__file__)) - 10)
        print('=-'*pathLen)
        print('= Script Location: {} \t=-'.format(os.path.realpath(__file__)))
        print('=-'*pathLen)
        print()
        sys.exit(0)

    def displayIntro(self):
        print('\033c')
        print("""
        Welcome to the JTB Investigator. To centralize those look ups you have to do 100x a day.

_______________________________________________________________________________________________
        __ ______   ____         __                                                            
        /    /      /   )        /                               ,                             
-------/----/------/__ /--------/-----__---------__---__--_/_--------__----__--_/_----__---)__-
      /    /      /    )       /    /   ) | /  /___) (_ ` /    /   /   ) /   ) /    /   ) /   )
_(___/____/______/____/_______/_ __/___/__|/__(___ _(__)_(_ __/___(___/_(___(_(_ __(___/_/_____
                                                                     /                         
                                                                  (_/  
              _
             | |
             | |===( )   //////
             |_|   |||  | o o|
                    ||| ( c  )                  ____
                     ||| \= /                  ||   \_
                      ||||||                   ||     |
                      ||||||                ...||__/|-"
                      ||||||             __|________|__
                        |||             |______________|
                        |||             || ||      || ||
                        |||             || ||      || ||
------------------------|||-------------||-||------||-||-------
                        |__>            || ||      || ||
        
        Author: Th3J0kr
        Version: 1.0
        https://www.github.com/th3J0kr/jtb_investigator

        """)
        

    def displayMainMenu(self):
        print()
        print('Choose an option: ')
        print('1: Open a new investigation')
        print('2: Import a previous investigation')
        print('99: Quit')

    def run(self):
        
        if self.args:
            ready = False

            if self.args.version:
                self.printVersion()

            newInvestigation = Investigate()
            self.host = Host()

            if self.args.ip and self.args.hostname:
                self.host.ip = self.args.ip
                self.host.domainName = self.args.hostname
                ready = True
            elif self.args.ip:
                self.host.ip = self.args.ip
                ready = True
            elif self.args.hostname:
                self.host.domainName = self.args.hostname
                ready = True
            elif self.args.report:
                self.importInvestigation(self.args.report)
                newInvestigation.printReport(self.host)
                newInvestigation = Investigate(self.host)
                newInvestigation.investigation()
            elif self.args.time:
                timeConv = UtcToLocal()
                try:
                    print('{} in Local time is: {}'.format(self.args.time, timeConv.convertTime(self.args.time)))
                    print()
                except:
                    print('Unable to convert time! Check format matches 2018-10-16 21:22:23')
                    print()
                sys.exit(0)
            else:
                print('Not useful arguments!')
            #print('Here\'s what I got: IP {}; Hostname{}'.format(self.host.ip, self.host.domainName))
            if self.args.disable:
                ready = False
                newInvestigation = Investigate(self.host)
                newInvestigation.printReport(self.host)
                newInvestigation.investigation()
            if ready:
                if self.args.passive:
                    self.host = newInvestigation.autoSherlock(self.host, False)
                else:
                    self.host = newInvestigation.autoSherlock(self.host)
                newInvestigation.printReport(self.host)
                if self.args.format:
                    newInvestigation.exportReport(self.host, self.args.format)
                else:
                    newInvestigation.exportReport(self.host)
                sys.exit(0)
            
        while True:
            self.displayIntro()
            self.displayMainMenu()
            
            cmd = input('> ')
            print()

            if cmd == '1':
                newInvestigation = Investigate()
                newInvestigation.openInvestigation()
                newInvestigation.investigation()
   
            elif cmd == '2':
                try:
                    self.importInvestigation()
                    newInvestigation.printReport(self.host)
                    newInvestigation = Investigate(self.host)
                    newInvestigation.investigation()
                except KeyboardInterrupt:
                    newInvestigation = Investigate()
                    newInvestigation.openInvestigation()
                    newInvestigation.investigation()
            
            elif cmd == '99':
                print('[!] Quitting!')
                try:
                    sys.exit(0)
                except SystemExit:
                    os._exit(0)
            else:
                print('Please choose a valid option')
                



if __name__ == '__main__':
    new = Main()
    new.parse_args()
    try:
        new.run()
    except KeyboardInterrupt:
        print('\r[!] Quitting!')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)