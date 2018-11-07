#!/usr/bin/env python3

import os, sys, argparse, math, csv, json
from investigation import Investigate, Host
from modules import UtcToLocal
import tools.comb_reports
import tools.mass_investigator
import colorama
from colorama import Fore, Back, Style


class Main:
    
    def __init__(self, host=None, args=None):
       self.host = host
       self.args = args
       colorama.init()
       
    
    def helpMsg(self):
        return """

jtb.py [-h] [-i IP] [-n HOSTNAME] [-r REPORT] [-d] [-f FORMAT] [-p]
              [-t TIME] [-m MASS] [-c COMBINE] [-v]

Investigate from the command line

optional arguments:
  -h, --help            show this help message and exit
  -i IP, --ip IP        IP to investigate
  -n HOSTNAME, --hostname HOSTNAME
                        Hostname to investigate
  -r REPORT, --report REPORT
                        Report to import
  -d, --disable         Disable auto investigate when starting with option
  -f FORMAT, --format FORMAT
                        Format to export to. Avoids prompt for CLI auto
                        investigate.
  -p, --passive         Passive recon only. Doesn't run nmap or any scans that
                        interact with the target itself.
  -t TIME, --time TIME  Convert time from UTC to Local Time and quit. (format:
                        2018-10-16 21:22:23)
  -m MASS, --mass MASS  Filename of hostnames or ips to investigate. Must
                        start with "hostnames_" "ips_", supports txt and csv 
                        import files
  -c COMBINE, --combine COMBINE
                        Name to give file after combine
                        (<filename>_combined.<format>
  -v, --version         Print JTB version currently installed

Examples:

Convert time: './jtb.py -t '2018-10-16 21:22:23''
Start investigation with a hostname: './jtb.py -n scanme.nmap.org -d'
Start investigation with an IP: './jtb.py -i 8.8.8.8 -d'
Get all information you can about hostname: './jtb.py -n scanme.nmap.org'
Get all information you can about hostname using only passive techniques: './jtb.py -n scanme.nmap.org -p'
Get all information you can about hostname and send to csv report (avoids the prompt after the investigation): './jtb.py -n scanme.nmap.org -f csv'
Combine all reports currently in reports (exluding already combined files) into 'new_combined.<format>': './jtb.py -c new'
Run batch investigation of hostnames in hostnames_test.txt in passive mode (without nmap) and export report in json (csv is default): './jtb.py -m hostnames_test.txt -p -f json'
Run batch investigation of hostnames in hostnames_test.txt in passive mode (without nmap) and export report in json (csv is default) then combine files into 'test1_combine.json' (warning also combines other reports): './jtb.py -m hostnames_test.txt -p -f json -c test1'
        """

    def parse_args(self):
        parser = argparse.ArgumentParser(add_help=False, description='Investigate from the command line', usage=self.helpMsg())
        parser.add_argument('-i', '--ip', type=str, help = 'IP to investigate')
        parser.add_argument('-h', '--help', action='store_true', help = 'IP to investigate')
        parser.add_argument('-n', '--hostname', type=str, help ='Hostname to investigate')
        parser.add_argument('-r', '--report', type=str, help='Report to import')
        parser.add_argument('-d', '--disable', action='store_true', help='Disable auto investigate when starting with option')
        parser.add_argument('-f', '--format', type=str, help="Format to export to. Avoids prompt for CLI auto investigate.")
        parser.add_argument('-p', '--passive', action='store_true', help="Passive recon only. Doesn't run nmap or any scans that interact with the target itself.")
        parser.add_argument('-t', '--time', type=str, help="Convert time from UTC to Local Time and quit. (format: 2018-10-16 21:22:23)")
        parser.add_argument('-m', '--mass', type=str, help='Filename of hostnames or ips to investigate, supports csv and txt. Must start with "hostnames_" "ips_"')
        parser.add_argument('-c', '--combine', type=str, help='Name to give file after combine (<filename>_combined.<format>')
        parser.add_argument('-v', '--version', action='store_true', help='Print JTB version currently installed')
        self.args = parser.parse_args()
        if self.args.help:
            print(self.helpMsg())
            sys.exit(0)

    def importInvestigation(self, filepath=None):
        if not filepath:
            print(Fore.MAGENTA + 'Please provide a filepath of the investigation to import:' + Style.RESET_ALL)
            filepath = input('> ')

        fileParts = filepath.split('.')
        fileType = fileParts[-1]
        
        if not os.path.isfile(filepath):
            print('Couldn\'t find the file!')
        else:
            print(Fore.BLUE + 'Importing Investigation {}'.format(filepath) + Style.RESET_ALL)

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
       
            if len(inReport) == 8:
                self.host = Host(ip=inReport[0], domainName=inReport[1], status=inReport[2], ports=inReport[3], 
                                whoisInfo=inReport[4], asnNum=inReport[5], asnInfo=inReport[6], blackListed=inReport[7])
            else:
                print(Fore.Red + 'Wrong number of arguments in saved report' + Style.RESET_ALL)
                print(inReport)

    def printVersion(self):
        print()
        print('=-'*21)
        print('= JTB Investigator Version: 2.1 \t=-')
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
        print(Fore.GREEN + """
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
        Version: 2.1
        https://www.github.com/th3J0kr/jtb_investigator

        """ + Style.RESET_ALL)
        

    def displayMainMenu(self):
        print()
        print('Choose an option: ')
        print('1: Open a new investigation')
        print('2: Import a previous investigation')
        print('3: Mass Investigaton of file (csv or txt) (file must start with "hostnames_" or "ip_"')
        print('4: Combine current reports into 1 file for each format')
        print(Fore.RED + '99: Quit' + Style.RESET_ALL)

    def run(self):
        self.displayIntro()
        if self.args:
            ready = False

            if self.args.version:
                self.printVersion()

            newInvestigation = Investigate()
            self.host = Host()

            if self.args.time:
                timeConv = UtcToLocal()
                try:
                    print('{} in Local time is: {}'.format(self.args.time, timeConv.convertTime(self.args.time)))
                    print()
                except:
                    print(Fore.RED + 'Unable to convert time! Check format matches 2018-10-16 21:22:23' + Stle.RESET_ALL)
                    print()
                sys.exit(0)
            elif self.args.mass:
                fileName = self.args.mass
                try:
                    while not os.path.isfile(fileName):
                        print(Fore.MAGENTA + 'Enter a filename of hostnames or ips (must start with "hostnames_" or "ips_"' + Style.RESET_ALL)
                        fileName = input('> ')
                except KeyboardInterrupt:
                    pass
                massInvestigator = tools.mass_investigator.MassInvestigator()
                hostL = massInvestigator.getHosts(fileName)
                if 'hostnames_' in fileName:
                    if self.args.format:
                        if self.args.passive:
                            massInvestigator.checkHosts(hostL=hostL, fFormat=self.args.format, nmap=False)
                        else:
                            massInvestigator.checkHosts(hostL=hostL, fFormat=self.args.format)
                    else:
                        if self.args.passive:
                            massInvestigator.checkHosts(hostL=hostL, nmap=False)
                        else:
                            massInvestigator.checkHosts(hostL=hostL)
                elif 'ips_' in fileName:
                    if self.args.format:
                        if self.args.passive:
                            massInvestigator.checkHosts(ipL=hostL, fFormat=self.args.format, nmap=False)
                        else:
                            massInvestigator.checkHosts(ipL=hostL, fFormat=self.args.format)
                    else:
                        if self.args.passive:
                            massInvestigator.checkHosts(ipL=hostL, nmap=False)
                        else:
                            massInvestigator.checkHosts(ipL=hostL)
                else:
                    print('File name needs to start with hostnames_ or ips_')
                    sys.exit(0)
                print(Fore.GREEN + 'Done!' + Style.RESET_ALL)
            
            if self.args.combine:
                name = self.args.combine
                while name == "":
                    print(Fore.MAGENTA + 'What do you want the group name for these reports to be? ("<name>_hostnames.<format>"' + Style.RESET_ALL)
                    name = input("> ")
                combReport = tools.comb_reports.CombineReports()
                combReport.main(name=name)
                print(Fore.GREEN + 'Done!' + Style.RESET_ALL)
                print()
                sys.exit(0)
            #print('Here\'s what I got: IP {}; Hostname{}'.format(self.host.ip, self.host.domainName))
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
                #newInvestigation.printReport(self.host)
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

            elif cmd == '3':
                fileName = ""
                try:
                    while not os.path.isfile(fileName):
                        print(Fore.MAGENTA + 'Enter a filename of hostnames or ips (must start with "hostnames_" or "ips_"' + Style.RESET_ALL)
                        fileName = input('> ')
                except KeyboardInterrupt:
                    pass
                massInvestigator = tools.mass_investigator.MassInvestigator()
                hostL = massInvestigator.getHosts(fileName)
                ap = ""
                while ap == "":
                    print(Fore.MAGENTA + 'Do you want to run in (A)ctive or (P)assive mode?' + Style.RESET_ALL)
                    ap = input("> ")
                ap = ap.upper()
                if 'hostnames_' in fileName:
                    if ap == 'A':
                        massInvestigator.checkHosts(hostL=hostL)
                    else:
                        massInvestigator.checkHosts(hostL=hostL, nmap=False)

                elif 'ips_' in fileName:
                    if ap == 'A':
                        massInvestigator.checkHosts(ipL=hostL)
                    else:
                        massInvestigator.checkHosts(ipL=hostL, nmap=False)
                print('Done!')
                sys.exit(0)

            elif cmd == '4':
                name = ""
                while name == "":
                    print(Fore.MAGENTA + 'What do you want the group name for these reports to be? ("<name>_hostnames.<format>"' + Style.RESET_ALL)
                    name = input("> ")
                
                combReport = tools.comb_reports.CombineReports()
                combReport.main(name=name)
                print('Done!')
                print()
                sys.exit(0)
            
            elif cmd == '99':
                print(Fore.RED + '[!] Quitting!' + Style.RESET_ALL)
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
        print(Fore.RED + '\r[!] Quitting!' + Style.RESET_ALL)
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)