#!/usr/bin/env python3

import os, sys, argparse
from investigation import Investigate, Host

class Main:
    
    def __init__(self, host=None, args=None):
       self.host = host
       self.args = args

    def parse_args(self):
        parser = argparse.ArgumentParser(description='Investigate from the command line')
        parser.add_argument('-i', '--ip', type=str, help = 'IP to investigate')
        parser.add_argument('-n', '--hostname', type=str, help ='Hostname to investigate')
        self.args = parser.parse_args()


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
    
    author: @th3J0kr
    version: 0.1
    https://www.github.com/th3J0kr/jtb_investigator                        

        """)

    def displayMainMenu(self):
        print()
        print('Choose an option: ')
        print('1: Open a new investigation')
        print('99: Quit')

    def run(self):
        
        if self.args:
            ready = False
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
            else:
                print('Not useful arguments!')
            print('Here\'s what I got: IP {}; Hostname{}'.format(self.host.ip, self.host.domainName))

            if ready:
                self.host = newInvestigation.autoSherlock(self.host)
                newInvestigation.printReport(self.host)
                newInvestigation.exportReport(self.host)
                sys.exit(0)
            
        while True:
            self.displayIntro()
            self.displayMainMenu()
            
            cmd = input('> ')
            print()

            if cmd == '1':
                newInvestigation = Investigate()
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