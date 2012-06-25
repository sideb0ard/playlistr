#!/usr/bin/python
import tornado.ioloop
import tornado.web
import json
import pymongo
from pymongo import Connection
from bson import json_util

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, tigrrr!!\n")

class PlaylistHandler(tornado.web.RequestHandler):
    def get(self, playlistID = None, skip = None, count = None):
        c = Connection()
        db = c.musicLibrary 
        collection = db.sideb0ard_playlists
        playlistsz = []
        if playlistID is None:
            for k in collection.find().skip(10).limit(20):
                jk = json.dumps(k, default=json_util.default)
                playlistsz.append(jk)
            jplaylists = json.dumps(playlistsz)
            self.set_header("Content-Type", "application/json") 
            self.write(jplaylists)
        else:
            playlist = []
            for p in collection.find({"Playlist ID" : int(playlistID)}).limit(1):
                jp = json.dumps(p, default=json_util.default)
                playlist.append(jp)

            self.set_header("Content-Type", "application/json") 
            self.write(playlist[0])

            
class TrackHandler(tornado.web.RequestHandler):
    def get(self,trackID = None):
        c = Connection()
        db = c.musicLibrary
        collection = db.sideb0ard_tracks
        track = []
        for t in collection.find({"Track ID" : int(trackID)}).limit(1):
            jt = json.dumps(t, default=json_util.default)
            track.append(jt)
        self.set_header("Content-Type", "application/json") 
        self.write(track[0])

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/playlist/?([0-9]+)?/?", PlaylistHandler),
    (r"/track/([0-9]+)/?", TrackHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
