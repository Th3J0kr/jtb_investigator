#!/usr/bin/env python3

import os, sys
from investigation import Investigate, Host

class Main:
    
    def __init__(self):
       pass

    
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
    try:
        new.run()
    except KeyboardInterrupt:
        print('\r[!] Quitting!')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)