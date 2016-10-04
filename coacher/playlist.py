class Playlist(object):

    def __init__(self, outpath='.'):
        self.playlist = []
        self.duration = 0

    def __iadd__(self, track):
        self.playlist.append(track)
        return self

    def strtime(self, sec):
        s = ''
        sec = int(sec)
        hrs = sec / 3600
        if hrs>0: s += str(hrs)+'h'
        sec -= 3600*hrs
        mins = sec / 60
        if mins>0: s += str(mins)+'mn'
        sec -= 60*mins
        s += str(sec)+'s'
        return s

    def save(self, m3u_name):
        M3U_EXTENDED = "#EXTM3U"
        M3U_INFORMATION = "#EXTINF:"

        print m3u_name,':'
        fp = file(m3u_name, "w")
        fp.write(M3U_EXTENDED + '\n')
        for track in self.playlist:
            if isinstance(track, tuple):
                fp.write(M3U_INFORMATION+str(int(track[1]/1000))+','+track[2]+'\n')
                fp.write(track[0]+'\n')
                self.duration += track[1]
                print '- ', track[0], ':', self.strtime(track[1]/1000)
            else:
                fp.write(track+'\n')
                print '- ', track
        fp.close()
        print 'Total:', self.strtime(self.duration/1000)
