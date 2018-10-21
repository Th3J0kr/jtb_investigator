#!/bin/bash

if [ -f ipasn_db_main.dat ];
then
    echo '[*] Found file, updating'

    echo '[*] Cleaning up old archives'
    for f in $( ls | grep 'bz2'); do
        rm -f $f
    done
    for f in $( ls | grep 'bak'); do
        rm -f $f
    done
    
    echo '[*] Downloading new database'
    pyasn_util_download.py --latest

    echo '[*] Backing up old archive'
    mv ipasn_db_main.dat ipasn_db_main.dat.bak

    if [ -f ipasn_db_main.dat.bak ]; then
        for newF in $( ls | grep 'bz2'); do
            pyasn_util_convert.py --single $newF ipasn_db_main.dat
        done
    else
        echo '[!] Unable to backup database... canceling update.'
    fi
fi