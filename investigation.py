from modules import Lookup, PortScan, Whois
import os, io

curDir = os.getcwd()

class Investigate:
    
    def __init__(self):
        self.host = Host()

    def hostInfo(self):
        print('----------------------------------------------------')

        print()
        print('Current host info: ')
        print('IP: {}'.format(self.host.ip))
        print('Domain Name: {}'.format(self.host.domainName))
        print()
        print('----------------------------------------------------')

    def printReport(self):
        print()
        print('----------------------------------------------------')
        for prop, val in vars(self.host).items():
            print('{} : {}'.format(prop, val))
        print('----------------------------------------------------')

    def exportReport(self):
        print('Exporting report...')

        reportDir = curDir + '/reports'
        if not os.path.isdir(reportDir):
              os.mkdir(reportDir)

        if not self.host.domainName:
            reportPath = reportDir + '/' + self.host.ip + '_report.txt'
        else:
            reportPath = reportDir + '/' + self.host.domainName + '_report.txt'

        with open(reportPath, 'w') as f:
            for prop, val in vars(self.host).items():
                f.write('{} : {}\n'.format(prop, val))
        print('Report Exported to {}!'.format(reportPath))

    def openInvestigation(self):
        valid = False
        print('Opening investigation')

        while not valid:
            print()
            print('What do you know about the host?')
            print('1: IP address')
            print('2: Domain Name')
            
            cmd = input('> ')

            if cmd == '1':
                self.host.changeIP()
                if self.host.ip:
                    valid = True
            elif cmd == '2':
                self.host.changeDomain()
                if self.host.domainName:
                    valid = True

            else:
                print('Choose a valid option!')
                print()
           

    def displayInvestMenu(self):
        print()
        print('Choose an option: ')
        print('0: Display help')
        print('1: Print working host info')
        print('2: Print Investigation report')
        print('3: Lookup missing info')
        print('4: Nmap it')
        print('5: Get whois info')
        print('6: Auto Investigate')
        print('96: Export Investigation')
        print('97: Change IP')
        print('98: Change Domain Name')
        print('99: Back to main menu (destroys current investigation)')

    def showHelp(self):
        print("""
------
JTB (Just the basics) Investigator is a simple framework to ease the monotonous looks up many of us do every day. When you get an alert and need to track down an IP or Domain Name or just in general investigation, we often do the same basic look ups (NSLookup, Nmap, whois, etc.) over and over. Trying to manage the different terminals and out puts became annoying and cumbersome to me so I wanted to make it easier.

Author: [@Th3J0kr](https://twitter.com/Th3J0kr)
Version: 0.1
------
##Usage##

`0`: Display help information (not added yet)
`1`: Print info about the host (IP and Domain)
`2`: Print all the information gathered so far.
`3`: Get either the IP or the Domain Name depending which you have already provided
`4`: Get open ports on target host (Only scans 22-443 right now)
`5`: Do a whois lookup and store import information to investigation report
`6`: Let the Investigator collect as much information for you as possible (Runs all modules against what it has)
`96`: Save the investigation to a file in `./reports/<hostname or ip>_report.txt`
`97`: Change IP of target
`98`: Change Domain Name of target
`99`: Go back to main menu. Destroys current investigation
        """)

    def autoSherlock(self):
        print()
        print('Let me see what I can get for you...')
        print()

        lookup = Lookup()
        if not self.host.domainName:
            self.host = lookup.doLookup(self.host)
        elif not self.host.ip:
            self.host = lookup.doLookup(self.host)

        if not self.host.ports:
            sType = 'F'
            scan = PortScan(self.host.ip, sType)
            self.host.ports = scan.runScan(self.host.ip, sType)

        if not self.host.whoisInfo:
                if not self.host.domainName:
                    self.whoisLookup = Whois(ip=self.host.ip)
                else:
                    self.whoisLookup = Whois(hostName=self.host.domainName)
                self.host.whoisInfo = self.whoisLookup.getInfo()

        
    
    def investigation(self):
        
        self.openInvestigation()

        while True:
            self.displayInvestMenu()

            cmd = input('> ')
            if cmd == '0':
                print('Add help')

            elif cmd == '1':
               self.hostInfo()

            elif cmd == '2':
                self.printReport()

            elif cmd == '3':
                lookup = Lookup()
                self.host = lookup.doLookup(self.host)
                if self.host.ip and self.host.domainName:
                    self.hostInfo()

            elif cmd == '4':
                print('What type of scan do you want to do? (e.g. F (default), sS, sV, A)')
                sType = input('> ')
                scan = PortScan(self.host.ip, sType)
                self.host.ports = scan.runScan(self.host.ip, sType)

            elif cmd == '5':
                if not self.host.domainName:
                    self.whoisLookup = Whois(ip=self.host.ip)
                else:
                    self.whoisLookup = Whois(hostName=self.host.domainName)
                self.host.whoisInfo = self.whoisLookup.getInfo()

            elif cmd == '6':
                if not self.host.ip and not self.host.domainName:
                    print('I don\'t have enough info for that yet!')
                else:
                    self.autoSherlock()

            elif cmd == '96':
                self.exportReport()

            elif cmd == '97':
                self.host.changeIP()

            elif cmd == '98':
                self.host.changeDomain()

            elif cmd == '99':
                print('[!] Quitting!')
                break

            else:
                print('Please enter a valid option!')
            
    

class Host:
    def __init__(self, ip="", domainName=""):
        self.ip = ip
        self.domainName = domainName
        self.ports = []
        self.whoisInfo = {}

    def changeIP(self):
        
        while not self.ip:
            print('Please enter IP address of host: ')
            ip = input('(e.g. 10.80.1.1) > ')
            self.ip = ip
        print('Assigned host ip of {}'.format(self.ip))

    def changeDomain(self):
        while not self.domainName:
            print('Please enter Domain Name of host: ')
            domainName = input('(e.g. google.com) > ')    
            self.domainName = domainName
        print('Assigned host domain name of {}'.format(self.domainName))
