#!/usr/bin/python
import os.path
import sys
import plistlib
import pymongo
from pymongo import Connection

class Playlist(object):

    def __init__(self, filename=None):
        self.plistr= None
        if filename:
            self.plistr = plistlib.readPlist(filename)

    def importPlaylists(self):
        for playlist in self.plistr["Playlists"]:
            print "PLAYLIST:::{0}".format(playlist)

    def importTracks(self):
        trackKeys = self.plistr["Tracks"]
        for key in trackKeys:
            trackData = self.plistr['Tracks'][str(key)]
            print "TRACKDATA:::{0}".format(trackData)

def playListr(filename):
    myLib = Playlist(filename)
    myLib.importPlaylists() 
    myLib.importTracks() 

if __name__ == "__main__":
    
    if len(sys.argv) != 2: 
        print '\nUsage: ./playlistExport.py <ITUNES-LIBRARY-XML-FILE>\n'
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

    libraryFile = sys.argv[1]
    
    print '\nLibrary File is {0}\n'.format(sys.argv[1])
    playListr(libraryFile)
