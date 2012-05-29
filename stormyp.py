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
    def get(self, playlistID = None):
        c = Connection()
        db = c.musicLibrary 
        collection = db.sideb0ard_playlists
        playlistsz = []
        if playlistID is None:
            key = "playlist:user0:itunes:*"
            for k in collection.find():
                #jk = json_util.default(k)
                jk = json.dumps(k, default=json_util.default)
                playlistsz.append(jk)
            print(playlistsz)
        else:
            pass
            #key = "playlist:user0:itunes:{0}:document".format(playlistID)
            #self.set_header("Content-Type", "application/json") 
            
class TrackHandler(tornado.web.RequestHandler):
    def get(self,tid):
        self.write("TRAXX Bitch {0}\n".format(tid))

application = tornado.web.Application([
    (r"/", MainHandler),
    #(r"/playlist/?", PlaylistHandler),
    #(r"/playlist/?([a-zA-Z0-9]+)?/?", PlaylistHandler),
    (r"/playlist/([0-9]+)?/?", PlaylistHandler),
    #(r"/([a-zA-Z0-9]+)/playlist/?([0-9]+)?/?", PlaylistHandler),
    #(r"/playlist/([0-9]+)", PlaylistHandler),
    #(r"/track/([0-9]+)", TrackHandler),
    #(r"/import/playlist/", ImportPlaylistHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
