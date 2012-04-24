#!/usr/bin/python
import re
import os.path
import sys

m3uList = "#EXTM3U\n%s\n"
m3uEntry = "#EXTINF:%(length)s,"
m3uEntry += "%(artist)s - %(album)s - %(song)s\n%(filename)s\n"

def phraseUnicode2ASCII(message):
    """
    Works around the built-in function str(message) which aborts when non-ASCII
    unicode characters are given to it.

    Modified from http://mail.python.org/pipermail/python-list/2002-June/150077.html
    """
    try:
        newMsg = message.encode('ascii')
    except (UnicodeDecodeError, UnicodeEncodeError):
       chars=[]
       for uc in message:
          try:
             char = uc.encode('ascii')
             chars.append(char)
          except (UnicodeDecodeError, UnicodeEncodeError):
             pass
       newMsg = ''.join(chars)
    return newMsg.strip()

class Playlists(object):

    def __init__(self, filename=None, destDir=None):
        self.lib = None
        if filename:
            self.lib = load(filename)
        if not destDir:
            destDir = './'
        self.destDir = destDir

    def processTrack(self, trackData):
        length = trackData.get('Total Time') or 300000
        song = trackData.get('Name') or 'Unknown'
        artist = trackData.get('Artist') or 'Unknown'
        album = trackData.get('Album') or 'Unknown'
        data = {
            'filename': trackData['Location'],
            'length': int(length)  / 1000 + 1,
            'song': phraseUnicode2ASCII(song),
            'artist': phraseUnicode2ASCII(artist),
            'album': phraseUnicode2ASCII(album),
        }
        return m3uEntry % data

    def processTrackIDs(self, ids):
        output = ''
        for id in ids:
            try:
                trackData = self.lib['Tracks'][str(id)]
                output += self.processTrack(trackData)
            except KeyError:
                print "Could not find track %i; skipping ..." % id
        return output

    def cleanName(self, unclean):
        clean = re.sub('[^\w]', '_', unclean)
        clean = re.sub('_{1,}', '_', clean)
        return clean

    def exportPlaylists(self):
        for playlist in self.lib['Playlists']:
            playlistName = self.cleanName(playlist['Name'])
            try:
                items = playlist['Playlist Items']
            except KeyError:
                print "Playlist seems to be empty; skipping ..."
                continue
            trackIDs = [x['Track ID'] for x in items]
            data = m3uList % self.processTrackIDs(trackIDs)
            fh = open("%s/%s.m3u" % (self.destDir, playlistName), 'w+')
            fh.write(data)
            fh.close()

def exportPlaylists(filename, dest=None):
    pls = Playlists(filename, dest)
    pls.exportPlaylists()

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
    

    print 'Library File is {0} and Output Dir is {1}\n'.format(sys.argv[1],sys.argv[2])
    # exportPlaylists(libraryFile, dest)
