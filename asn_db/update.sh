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
        echo '[*] Processing new ASN database...'
        for newF in $( ls | grep 'bz2'); do
            pyasn_util_convert.py --single $newF ipasn_db_main.dat
        done

        if [ -f ipasn_db_main.dat ]; then
            echo '[*] Update successful, removing downloaded .bz2 archive...'
            for f in $( ls | grep 'bz2'); do
                rm -f $f
            done
        fi

    else
        echo '[!] Unable to backup database... canceling update.'
    fi
else
	echo '[!] No Database found!'
    echo '[*] Checking for old downloads...'

    for f in $( ls | grep 'bz2'); do
        echo '[!] Removing old database '
        rm -f $f
    done

	echo '[*] Downloading new database!'
	pyasn_util_download.py --latest

	for newF in $( ls | grep 'bz2'); do
		echo '[*] Processing new database file...'
		pyasn_util_convert.py --single $newF ipasn_db_main.dat
	done

	if [ -f ipasn_db_main.dat ];
	then
		echo '[*] New database ready!'
        echo '[*] Removing downloaded archive...'
        for f in $( ls | grep 'bz2'); do
            rm -f $f
        done
	else
		echo '[!] Something went wrong!'
	fi


fi
