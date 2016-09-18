import math
import wave
import struct

class Coacher:
    
    def __init__(self, outpath='.'):
        self.rate = 22050;
        self.inpath = 'data'
        self.outpath = outpath
        self.playlist = []

    def pcm_channels(self, wave_name):
        """Given a file-like object or file path representing a wave file,
        decompose it into its constituent PCM data streams.

        Input: A file like object or file path
        Output: A list of lists of integers representing the PCM coded data stream channels
            and the sample rate of the channels (mixed rate channels not supported)
        """
        stream = wave.open(wave_name,"rb")

        num_channels = stream.getnchannels()
        sample_rate = stream.getframerate()
        sample_width = stream.getsampwidth()
        num_frames = stream.getnframes()

        raw_data = stream.readframes( num_frames ) # Returns byte data
        stream.close()

        total_samples = num_frames * num_channels

        if sample_width == 1: 
            fmt = "%iB" % total_samples # read unsigned chars
        elif sample_width == 2:
            fmt = "%ih" % total_samples # read signed 2 byte shorts
        else:
            raise ValueError("Only supports 8 and 16 bit audio formats.")

        integer_data = struct.unpack(fmt, raw_data)
        del raw_data # Keep memory tidy (who knows how big it might be)

        channels = [ [] for time in range(num_channels) ]
        
        for index, value in enumerate(integer_data):
            bucket = index % num_channels
            channels[bucket].append(value)

        return channels, sample_rate

    def read_wav(self, wave_name):
        """Read a wav file and returns first channel"""
        file_name = self.inpath+'/'+wave_name+'.wav'
        # TODO should resample if necessary
        channels,sample_rate = self.pcm_channels(file_name)
        #print 'Read', wave_name,' at', sample_rate
        return channels[0];

    def save_wav(self, wave_name, channel):
        file_name = self.outpath+'/'+wave_name+'.wav'
        # Open up a wav file
        wav_file=wave.open(file_name,"w")

        # wav params
        nchannels = 1

        sampwidth = 2

        nframes = len(channel)
        comptype = "NONE"
        compname = "not compressed"
        wav_file.setparams((nchannels, sampwidth, self.rate, nframes, comptype, compname))
        
        raw_data = []
        for value in channel:
            packed_value = struct.pack('h', value)
            raw_data.append(packed_value)
        raw_str = ''.join(raw_data)
        wav_file.writeframes(raw_str)

        wav_file.close()
        mp3 = wave_name+'.mp3'
        self.playlist.append(mp3)

    def silence(self, duration_milliseconds=500):
        """
        Adding silence is easy - we add zeros to the end of our array
        """
        num_samples = duration_milliseconds * (self.rate / 1000.0)

        channel = []
        for x in range(int(num_samples)): 
            channel.append(0)

        return channel

    def sinewave(self, freq=440.0, duration=500, volume=32000):
        """
        The sine wave generated here is the standard beep.  If you want something
        more aggresive you could try a square or saw tooth waveform.   Though there
        are some rather complicated issues with making high quality square and
        sawtooth waves... which we won't address here :) 
        """
        num_samples = duration * (self.rate / 1000.0)

        channel = []
        for x in range(int(num_samples)):
            channel.append(int(volume * math.sin(2 * math.pi * freq * ( float(x) / self.rate ))))
            
        return channel

    def duration(self, channel):
        """Returns duration of channel in ms"""
        return len(channel)/(self.rate/1000.0)

    def save_playlist(self, mp3_list = None, m3u_name = 'seance.m3u'):
        FORMAT_DESCRIPTOR = "#EXTM3U"
        RECORD_MARKER = "#EXTINF"

        if mp3_list is None:
            mp3_list = self.playlist
        fp = file(m3u_name, "w")
        fp.write(FORMAT_DESCRIPTOR + "\n")
        for track in mp3_list:
            fp.write(track+'\n')
        fp.close()
