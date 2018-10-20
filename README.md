# JTB Investigator

### A tool born out of laziness
------

###### This tool was born out of the unhappy marriage of terrible telemetry and tooling built into BitSight and my general laziness when it comes to doing a lot of look ups on Domain Names and IP addresses.

------

JTB (Just the basics) Investigator is a simple framework to ease the monotonous looks up many of us do every day. When you get an alert and need to track down an IP or Domain Name or just in general investigation, we often do the same basic look ups (NSLookup, Nmap, whois, etc.) over and over. Trying to manage the different terminals and out puts became annoying and cumbersome to me so I wanted to make it easier.

Author: [@Th3J0kr](https://twitter.com/Th3J0kr)

Version: 0.1

------

## Installation

The setup is very simple:

##### Ensure you have nmap, whois, and python 3 installed on the system
###### *Only tested on linux systems with python 3.7 at the moment*

### Install python requirements with pip
`pip3 install -r requirements.txt` or `pip3 install python-nmap python-whois`

### Clone the repo
`git clone https://github.com/Th3J0kr/jtb_investigator.git`

And you're good to go!

## Usage

Using is very simple, that's the whole point. Not just to help us that do this manually everyday but also to make it easier for newbs to do these looks more quickly!

### Menu Driven

Just `cd` into the `jtb_investigator` directory and run `jtb.py` with `./jtb.py` or `python3 jtb.py`

Once running just follow the prompts!

### Command line usage

Using the command line makes the lookups even faster. After I added this feature I realized there isn't much point of the menu driven part but ASCII art is fun so...

Anyway it's easy to automate it all with: `./jtb.py -i <ip to investigate>` or `python3 jtb.py -n <hostname to investigate>`

This will spit the report into the `reports/` directory in `<hostname or ip>_report.txt`.

## General Guidance

### Starting an investigation

After the super sweet ASCII art, you will be prompted to either start an investigation (1) or quit (99). This menu will be have more options in the future such as import an investigation but it's just simple right now.

Hit 1 and you will be asked for an IP or Domain Name. You will not be able to proceed until you provide one or the other to prevent issues down the line.

### Investigating

Once you have started your investigation of an IP or Domain Name you will be presented with a menu of options:

```
Choose an option:
0: Display help
1: Print working host info
2: Print Investigation report
3: Lookup missing info
4: Nmap it
5: Get whois info
6: Auto Investigate
96: Export Investigation
97: Change IP
98: Change Domain Name
99: Back to main menu (destroys current investigation)
>
```

### Menu Options

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

## To Do:

This framework is still in the very early stages of development. There will likely be lots of bugs and errors so don't hesitate to contribute or open an issue on github.

It is written to be easily extended. All the options are classes in the `modules.py` file. To add a new module just add an option to the menu and write a new class in `modules.py`. Pull requests to extend features are welcome

### General improvements

1. Add import investigation
2. ~~Add help in menu~~
3. Stability improvements

### Feature additions

1. Add multi-host capability
2. Add more investigation modules
3. Add different export formats
4. Clean up auto-investigate
5. ~~Add command line options to expedite startup~~











