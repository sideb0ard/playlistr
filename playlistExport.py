#!/usr/bin/python

import re
import os.path
import sys
import plistlib
import simplejson as json

m3uList = "#EXTM3U\n%s\n"
m3uEntry = "#EXTINF:%(length)s,"
m3uEntry += "%(artist)s - %(album)s - %(song)s\n%(filename)s\n"

class Playlists(object):

    def __init__(self, filename=None, destDir=None):
        self.plistr= None
        if filename:
            self.plistr = plistlib.readPlist(filename)
        if not destDir:
            destDir = './'
        self.destDir = destDir

#	def processTrack(self, trackData):
#	    length = trackData.get('Total Time') or 300000
#	    song = trackData.get('Name') or 'Unknown'
#	    artist = trackData.get('Artist') or 'Unknown'
#	    album = trackData.get('Album') or 'Unknown'
#	    data = {
#	        'filename' : trackData['Location'],
#	        'length' : int(length) / 1000 + 1,
#	        'song' : song,
#	        'artist' : artist,
#	        'album' : album,
#	    }
#	    return data
#	    

    def processTrack(self, trackData):
        #print "\n\tPROC:: {0}".format(trackData)
        length = trackData.get('Total Time') or 300000
        #print "\nLENG = {0}".format(length)
#        data = {
#            'length' : int(length) / 1000 + 1.
#        }
#        return m3uEntry % data

    def processTrackIDz(self,idz):
        output =''
        for id in idz:
            try:
                trackData = self.plistr['Tracks'][str(id)]
                #print "\nblah - {0}".format(trackData)
                self.processTrack(trackData)
                #output += self.processTrack(trackData)
            except KeyError:
                print "Barfed on {0}, skipping .. \n".format(id)
        #print json.dumps(output)
        return output


    def export(self):
        #print "YAR!\n"
        for playlist in self.plistr['Playlists']:
            playlistName = playlist['Name']
            print "PLAYLIST:{0}".format(playlistName)
            if re.match('Library',playlistName):
                print "SKIPPING LIBRARY...\n\n"
                continue
            #print "FULLPLAYLIST\n>>>>>>{0}\n\n".format(playlist)
            #try:
            if 'Distinguished Kind' in playlist:
                print "SKIPPING DISTINGUISHED...\n\n"
                continue
            try:
                print json.dumps(playlist)
            except:
                print "\n\nouch\n\n"
            print "\n"
            #print "Playlist Name: {0}\n".format(playlistName)
            try:
                items = playlist['Playlist Items']
            except:
                #print "No playlist items - skipping..\n"
                continue
            #print "\n{0} - with {1}\n".format(playlistName,items)
            trackIDz = [x['Track ID'] for x in items]
            #print "\nTRAK IDZ - {0}".format(trackIDz)
            data = self.processTrackIDz(trackIDz)
#	        data = m3uList % processTrackIDz(trackIDz)
#	        #print "\nDATA:: {0}\n".format(data) 

#    def echo(self,text):
#        #print "\nYAR! {0}\n".format(text)

def playListr(filename, dest=None):
    pls = Playlists(filename,dest)
    pls.export()
#    pls.echo("BLAH")


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
