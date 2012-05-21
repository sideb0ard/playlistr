#!/usr/bin/python
import tornado.ioloop
import tornado.web
import redis

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, playrrr!!\n")

class PlaylistHandler(tornado.web.RequestHandler):
    def get(self, pid = None):
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        if pid is None:
            self.write("Printing all playlists\n")
            key = "playlist:1:*"
            #print "KEY SI {0}".format(key)
            allplaylistkeys = r.keys(key)
            allplaylists = {}
            for k in allplaylistkeys:
                # NEED PAGINATION
                #allplaylists { k : r.get(key) }
                #self.write("{0}".format(r.get(k)))
                allplaylists[k] = r.get(k)
            self.write("Playlistz --\n{0}\n".format(allplaylists))
        else:
            self.write("Playlists Bitch {0}\n".format(pid))
            key = "playlist:1:itunes:{0}:contents".format(pid)
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

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/playlist/", PlaylistHandler),
    (r"/playlist/([0-9]+)", PlaylistHandler),
    (r"/track/([0-9]+)", TrackHandler),
])

if __name__ == "__main__":
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
