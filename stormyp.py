#!/usr/bin/python
import tornado.ioloop
import tornado.web
import redis
import json
from plistlib import readPlistFromString

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, tigrrr!!\n")

class PlaylistHandler(tornado.web.RequestHandler):
    def get(self, username = None, playlistID = None):
        #self.write("Username: {0} // PlaylistID: {1}".format(username, playlistID))
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        if playlistID is None:
            #self.write("Printing all playlists\n")
            key = "playlist:1:*"
            #print "KEY SI {0}".format(key)
            allplaylistkeys = r.keys(key)
            allplaylists = {}
            for k in allplaylistkeys:
                # NEED PAGINATION
                #allplaylists { k : r.get(key) }
                #self.write("{0}".format(r.get(k)))
                #plist_version = readPlist(r.get(k))
                plist_version = readPlistFromString(r.get(k))
                print "plsit -- {0}".format(plist_version)
                #allplaylists[k] = json.dumps(plist_version)
                allplaylists[k] = r.get(k)
            #json_playlists = json.dumps(allplaylists)
            print "{0}".format(allplaylists)
        else:
            self.write("Playlists Bitch {0}\n".format(playlistID))
            key = "playlist:1:itunes:{0}:contents".format(playlistID)
            self.write("Key -- {0}\n".format(key))
            playlist = r.get(key)
            self.write("Playlist -- {0}\n".format(playlist))
            
class TrackHandler(tornado.web.RequestHandler):
    def get(self,tid):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.write("TRAXX Bitch {0}\n".format(tid))
        key = "track:1:itunes:{0}:contents".format(tid)
        self.write("Key -- {0}\n".format(key))
        track = r.get(key)
        self.write("Trax09r -- {0}\n".format(track))

class ImportPlaylistHandler(tornado.web.RequestHandler):
    def get(self,tid):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.write("TRAXX Bitch {0}\n".format(tid))
        key = "track:1:itunes:{0}:contents".format(tid)
        self.write("Key -- {0}\n".format(key))
        track = r.get(key)
        self.write("Trax09r -- {0}\n".format(track))


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/playlist/([a-zA-Z0-9]+)/?", PlaylistHandler),
    (r"/playlist/([a-zA-Z0-9]+)/([0-9]+)", PlaylistHandler),
    #(r"/playlist/([0-9]+)", PlaylistHandler),
    (r"/track/([0-9]+)", TrackHandler),
    (r"/import/playlist/", ImportPlaylistHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
