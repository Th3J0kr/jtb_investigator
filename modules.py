import socket
from datetime import datetime, timezone
import nmap
import whois

class Lookup:
    def __init__(self, host):
        self.host = host

    def doLookup(self, host):
        if not self.host.ip:
            print('Looking up ip from domain {}'.format(self.host.domainName))
            try:
                ip = socket.gethostbyname(self.host.domainName)
                if ip:
                    self.host.ip = ip
                    return self.host
                else:
                    print('Couldn\'t get IP')
            except socket.gaierror:
                print('Couldn\'t look up that host')

        elif not self.host.domainName:
            print('Looking up domain name from ip {}'.format(self.host.ip))
            domainName = socket.gethostbyaddr(self.host.ip)
            if domainName:
                self.host.domainName = domainName[0]
                return self.host
            else:
                print('Couldn\'t get hostname')
        
        else:
            print('You already have the domain and IP!')
    
class PortScan:
    def __init__(self, ip, sType):
        self.ip = ip
        self.sType = sType
        self.ports = []

    def runScan(self, ip, sType):
        print('Running {} scan on {}...'. format(sType, ip))

        scanTypes = ['F', 'sS', 'sV', 'A']
        
        if not sType:
            sType = 'F'
        
        if sType in scanTypes:
            sType = '-' + sType
            self.nm = nmap.PortScanner()
            self.nm.scan(hosts=ip, arguments=sType)
            print('Done! Here\'s what I got:')
            self.parseResults()
            return self.ports
            
        else:
            print('I don\'t run that kind of scan')

    def parseResults(self):
        for host in self.nm.all_hosts():
            print('----------------------------------------------------')
            print('Host : %s (%s)' % (host, self.nm[host].hostname()))
            print('State : %s' % self.nm[host].state())
            print('----------------------------------------------------')

            for proto in self.nm[host].all_protocols():
                lport = self.nm[host][proto].keys()
                for port in lport:
                    self.ports.append(port)

class Whois:
    def __init__(self, hostName="", ip=""):
        self.hostName = hostName
        self.ip = ip
        self.results = ""

    def getInfo(self, hostName="", ip=""):
        self.results = whois.whois(hostName)
        self.whoisReturn = self.parseResults()
        return self.whoisReturn
    
    def parseResults(self):
        whoisResults = {}

        whoisResults['domain_name'] = self.results['domain_name']
        whoisResults['name'] = self.results['name']
        whoisResults['organization'] = self.results['org']
        whoisResults['address'] = self.results['address']
        whoisResults['state'] = self.results['state']
        whoisResults['city'] = self.results['city']
        return whoisResults
