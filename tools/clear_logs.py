#!/usr/bin/env python3

import os, sys
from subprocess import call

class ClearLogs:
        def main(self):
                scriptPath = os.path.dirname(os.path.realpath(__file__))
                pathP = scriptPath.split('/')
                rootPath = '/'.join(pathP[0:len(pathP)-1])
                reportPath = os.path.join(rootPath, 'reports')

                reportDirs = os.listdir(reportPath)

                for rDir in reportDirs:
                        reports = os.listdir(os.path.join(reportPath, rDir))
                for report in reports:
                        print("[*] Removing {} from {}".format(report, rDir))
                        os.remove(os.path.join(reportPath, rDir, report))

                print('[*] All done!')
                call(['tree', reportPath])
