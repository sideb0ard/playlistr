#!/usr/bin/python
import os.path
import sys
import traceback
import plistlib
import json
import re
import pymongo
from pymongo import Connection

class Playlist(object):

    def __init__(self, filename=None):
        self.plistr= None
        if filename:
            self.plistr = plistlib.readPlist(filename)


    def importPlaylists(self,pcollection):
        for playlist in self.plistr["Playlists"]:
            try:
                playlistID = playlist['Playlist ID']
                print "inserting playlist {0}\n".format(playlistID)
                pcollection.insert(playlist)
            except:
                print "Oh ya, something burny\n\n"
                traceback.print_exc(file=sys.stdout)

    def importTracks(self,tcollection):
        for track in self.plistr["Tracks"]:
            try:
                contents = self.plistr['Tracks'][track]
                print "Inserting {0}...\n".format(contents)
                #cleancontents = {}
                #for item in contents:
                #    if not re.search('Date', item):
                #        cleancontents[item] = contents[item]
                tcollection.insert(contents)
            except:
                print "Ouch, trackData munged\n\n"
                traceback.print_exc(file=sys.stdout)

def playListr(filename):
    myLib = Playlist(filename)
    c = Connection()
    db = c.musicLibrary
    #pcollection = db.sideb0ard_playlists
    #myLib.importPlaylists(pcollection)
    tcollection = db.sideb0ard_tracks
    myLib.importTracks(tcollection)

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
