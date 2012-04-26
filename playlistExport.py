#!/usr/bin/python

import re
import os.path
import sys
import plistlib

def playListr(filename, dest):
    plistr = plistlib.readPlist(filename)
    for playlist in plistr['Playlists']:
        print playlist['Name']


if __name__ == "__main__":
    
    if len(sys.argv) != 3: 
        print '\nUsage: ./playlistExport.py <ITUNES-LIBRARY-XML-FILE> <M3U-OUTPUTDIR>\n'
        sys.exit(1) 

    if os.path.isfile(sys.argv[1]):
        try:
            doc = open(sys.argv[1]).read().replace('\n', '')
        except IOError as e:
            print "\nOh dear, problems opening {0} - {1}\n".format(sys.argv[1],e)
            sys.exit(1)
    else:
            print "\nYow, looks like file {0} doesn't exist.\n".format(sys.argv[1])
            sys.exit(1)

    if not os.path.isdir(sys.argv[2]):
            print 'Oowie - directory {0} doesn\'t exist.\n'.format(sys.argv[2])
            sys.exit(1)

    libraryFile = sys.argv[1]
    dest = sys.argv[1]
    

    print '\nLibrary File is {0} and Output Dir is {1}\n'.format(sys.argv[1],sys.argv[2])
    playListr(libraryFile, dest)
