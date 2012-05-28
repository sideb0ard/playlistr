#!/usr/bin/python
import tornado.ioloop
import tornado.web
import redis
import json

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, tigrrr!!\n")

class PlaylistHandler(tornado.web.RequestHandler):
    def get(self, userName = None, playlistID = None):
        #self.write("Username: {0} // PlaylistID: {1}\n".format(userName, playlistID))
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        if playlistID is None and userName is None:
            self.write("Wow, something fuccccked up!\n")
        elif playlistID is None:
            #self.write("No Playlists - checking for all user playlists\n")
            key = "playlist:user0:itunes:*"
            #print "KEY SI {0}".format(key)
            alluserplaylistkeys = r.keys(key)
            alluserplaylists = {}
            for k in alluserplaylistkeys:
                alluserplaylists[k] = r.get(k)
            self.set_header("Content-Type", "application/json") 
            #self.write("{0}".format(alluserplaylists))
            self.write(alluserplaylists)
        else:
            #self.write("Username - {0} and playlist ID {1} \n".format(userName,playlistID))
            #self.write("Playlists Bitch {0}\n".format(playlistID))
            key = "playlist:user0:itunes:{0}:document".format(playlistID)
            #self.write("Key -- {0}\n".format(key))
            playlist = r.get(key)
            self.set_header("Content-Type", "application/json") 
            #self.write("Playlist -- {0}\n".format(playlist))
            self.write(playlist)
            
        #        # NEED PAGINATION
                #allplaylists { k : r.get(key) }
                #self.write("{0}".format(r.get(k)))
                #allplaylists[k] = json.dumps(plist_version)
            #json_playlists = json.dumps(allplaylists)
        #else:
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
    #(r"/playlist/?", PlaylistHandler),
    #(r"/playlist/?([a-zA-Z0-9]+)?/?", PlaylistHandler),
    #(r"/playlist/([a-zA-Z0-9]+)/?([0-9]+)?/?", PlaylistHandler),
    (r"/([a-zA-Z0-9]+)/playlist/?([0-9]+)?/?", PlaylistHandler),
    #(r"/playlist/([0-9]+)", PlaylistHandler),
    #(r"/track/([0-9]+)", TrackHandler),
    #(r"/import/playlist/", ImportPlaylistHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
