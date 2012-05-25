#!/usr/bin/python
import os.path
import sys
import traceback
import plistlib
import json
import redis
import re

class Playlist(object):

    def __init__(self, filename=None):
        self.plistr= None
        if filename:
            self.plistr = plistlib.readPlist(filename)


    def importPlaylists(self,r):
        for playlist in self.plistr["Playlists"]:
            try:
                playlistID = playlist['Playlist ID']
                key = "playlist:user0:itunes:{0}:document".format(playlistID)
                #print playlist, "\n\n"
                #print key, "\n\n"
                #contents = self.plistr['Playlists'][playlist]
                #print contents, "\n\n"
                #cleancontents = {}
                #for item in contents:
                #    if not re.search('Date', item):
                #        cleancontents[item] = contents[item]
                document = json.dumps(playlist)
                print "key == {0} // data == {1}\n\n".format(key,document)
                r.set(key,document)
            except:
                print "Oh ya, something burny\n\n"
                traceback.print_exc(file=sys.stdout)

    def importTracks(self,r):
        for track in self.plistr["Tracks"]:
            try:
                key = "track:user0:itunes:{0}:document".format(track)
                contents = self.plistr['Tracks'][track]
                cleancontents = {}
                for item in contents:
                    if not re.search('Date', item):
                        cleancontents[item] = contents[item]
                document = json.dumps(cleancontents)
                print "key == {0} // data == {1}\n\n".format(key,document)
                r.set(key,document)
            except:
                print "Ouch, trackData munged\n\n"
                traceback.print_exc(file=sys.stdout)

def playListr(filename):
    myLib = Playlist(filename)
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    myLib.importPlaylists(r) 
    myLib.importTracks(r) 

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
