#!/usr/bin/env python3

import os, sys, argparse

def parse_args():
        parser = argparse.ArgumentParser(description='Investigate from the command line')
        parser.add_argument('-i', '--ip', type=str, help = 'IPs or range to investigate separated by spaces (enclose in quotes)')
        parser.add_argument('-n', '--hostname', type=str, help ='Hostnames to investigate separated by spaces (enclose in quotes)')
        parser.add_argument('-f', '--format', type=str, help='Format to export file to (csv (default), json, txt)')
        args = parser.parse_args()
        return args

def main():
    args = parse_args()
    ipL = []
    hostL = []
    if args.ip:
        ipL = args.ip.split(' ')
    elif args.hostname:
        hostL = args.hostname.split(' ')
    else:
        print('[!] No arguments... Exiting!')
        sys.exit(0)
    myPath = os.path.realpath(__file__).split('/')
    pathLen = len(myPath) - 2
    jtbPath = '/' + '/'.join(myPath[1:pathLen])
    os.chdir(jtbPath)
    sys.path.insert(0, jtbPath)
    import jtb
    import investigation
    host = investigation.Host()

    
    if ipL:
        print('[*] Got IPs, running investigations.')
        for ip in ipL:
            host.ip = ip
            newInvestigation = investigation.Investigate()
            host = newInvestigation.autoSherlock(host)
            if args.format:
                newInvestigation.exportReport(host, args.format)
            else:
                newInvestigation.exportReport(host)
    if hostL:
        print('[*] Got hosts, running investigaitons.')
        for inHost in hostL:
            host.domainName = inHost
            newInvestigation = investigation.Investigate()
            host = newInvestigation.autoSherlock(host)
            if args.format:
                newInvestigation.exportReport(host, args.format)
            else:
                newInvestigation.exportReport(host, 'csv')
    else:
        print('[!] Couldn\'t get targets from cli!')

if __name__ == '__main__':
    try:
        args = parse_args()
        prog = main()

    except KeyboardInterrupt:
        print('\r[!] Quitting!')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)