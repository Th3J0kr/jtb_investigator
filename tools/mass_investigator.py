#!/usr/bin/env python3

import os, sys, csv
import investigation

class MassInvestigator:

    def __init__(self, ipL=None, hostL=[], fileName=[]):
        self.fileName = fileName
        self.ipL = ipL
        self.hostL = hostL

    def getHosts(self, fileName=None, ipL=[], hostL=[]):
        if not fileName:
            fileName = self.fileName
        if fileName:
            with open(fileName, 'r') as f:
                if 'hostnames' in fileName:
                    if fileName.endswith('.csv'):
                        print('[*] Reading CSV...')
                        
                    else:
                        print('[*] Reading text file...')
                        hosts = f.readlines()
                        for h in hosts:
                            hostL.append(h.strip("\n"))
                    sys.exit(0)
                    return hostL
                       
                elif 'ips' in fileName:
                    if fileName.endswith('.csv'):
                        print('[*] Reading CSV...')
                    else:
                        print('[*] Reading text file...')
                        hosts = f.readlines()
                        for h in hosts:
                            ipL.append(h)
                    sys.exit(0)
                    return ipL
                else:
                    print('[!] I don\'t understand that file type! Make sure it starts with ips or hostnames!')
            f.close
            print('Investigating hosts...')
            
        else:
            print('No file provided!')
            return

    def checkHosts(self, ipL=None, hostL=None, fFormat=None, nmap=True):
        if ipL:
            print('Got IPs, running investigations.')
            for ip in ipL:
                host = investigation.Host()
                host.ip = ip
                newInvestigation = investigation.Investigate()
                host = newInvestigation.autoSherlock(host, nmap=nmap)
                if fFormat:
                    newInvestigation.exportReport(host, fFormat)
                else:
                    newInvestigation.exportReport(host, 'csv')
        elif hostL:
            print('Got hostsnames, running investigaitons.')
            for inHost in hostL:
                host = investigation.Host()
                host.domainName = inHost
                newInvestigation = investigation.Investigate()
                host = newInvestigation.autoSherlock(host, nmap=nmap)
                if fFormat:
                    newInvestigation.exportReport(host, fFormat)
                else:
                    newInvestigation.exportReport(host, 'csv')
        else:
            print('Couldn\'t get targets to investigate!')

if __name__ == '__main__':
    try:
        prog = self.main()

    except KeyboardInterrupt:
        print('\r[!] Quitting!')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)