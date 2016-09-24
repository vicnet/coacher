

# les lignes droites de 80m sont calculees a 30s en gros.
# TODO prevoir un mecanisme pour parametrer la vitesse
# et calculer le temps en fonction de la distance

sec = 1000 # 1000 ms
min = 60*sec # 60s

coacher = Coacher()

def beeps():
    beep1 = coacher.read_wav('beep-07.wav')
    beep2 = coacher.sinewave(freq=1000)
    beeps = beep1+coacher.silence(1000-coacher.duration(beep1))
    return beeps*3+beep2*3

def silence(t):
    return coacher.silence(t)

# 1 seconde de silence ou separateur intermots
s1 = silence(1*sec)

def echauffement():
    footing = coacher.read_wav('footing25mn.wav')
    reste15 = coacher.read_wav('reste15mn.wav')
    reste5  = coacher.read_wav('reste5mn.wav')
    channel =\
        footing\
        + silence(10*min)\
        + reste15\
        + silence(10*min)\
        + reste5\
        + silence(5*min)
    coacher.save_wav('echauffement.wav',channel)

def lignes_droites():
    def ligne(ligne_wav, recup_wav='recup.wav'):
        # load files
        cligne = coacher.read_wav(ligne_wav)
        if recup_wav:
            recup = coacher.read_wav(recup_wav)
        cbeeps = beeps()
        tbeeps = coacher.duration(cbeeps)
        # generate prog
        channel =\
              cligne + silence(1*sec) + cbeeps\
            + silence(30*sec-tbeeps) + cbeeps
        if recup:
            channel += recup + silence(20*sec)
        return channel
    lignes = coacher.read_wav('5lignes.wav')
    channel = \
          lignes + silence(1*sec)\
        + ligne('1re-ligne.wav')\
        + ligne('2e-ligne.wav')\
        + ligne('3e-ligne.wav')\
        + ligne('4e-ligne.wav')\
        + ligne('der-ligne.wav')
    coacher.save_wav('lignes.wav',channel)
    
def series():
    plat = coacher.read_wav('plat2mn.wav')
    cote = coacher.read_wav('cote1mn15.wav')
    descente = coacher.read_wav('descente1mn.wav')
    recup = coacher.read_wav('recup3mn.wav')

    def serie(serie_wav, recup = recup):
        # load files
        cserie = coacher.read_wav(serie_wav)
        cbeeps = beeps()
        tbeeps = coacher.duration(cbeeps)
        # generate prog
        channel =\
              cserie + silence(1*sec)\
            + plat + s1 + cbeeps\
            + silence(2*min-tbeeps) + cbeeps\
            + s1 + cote + s1 + cbeeps\
            + silence(1*min+15*sec-tbeeps) + cbeeps\
            + s1 + descente + s1 + cbeeps\
            + silence(1*min) + cbeeps
        if recup:
            channel += recup + silence(3*min)
        return channel
        
    si = silence(500)
    series = coacher.read_wav('4series.wav')
    channel =\
          series\
        + si + plat\
        + si + cote\
        + si + descente\
        + si + recup\
        + s1\
        + serie('1re-serie.wav')\
        + serie('2e-serie.wav')\
        + serie('3e-serie.wav')\
        + serie('der-serie.wav')
    coacher.save_wav('series.wav',channel)

def retour():
    retour = coacher.read_wav('calme10mn.wav')
    reste5  = coacher.read_wav('reste5mn.wav')
    channel =\
        retour\
        + silence(5*min)\
        + reste5\
        + silence(5*min)\
        + beeps()
    coacher.save_wav('retour.wav',channel)

def playlist(mp3_list, m3u_name = 'seance.m3u'):
    FORMAT_DESCRIPTOR = "#EXTM3U"
    RECORD_MARKER = "#EXTINF"

    fp = file(m3u_name, "w")
    fp.write(FORMAT_DESCRIPTOR + "\n")
    for track in mp3_list:
        fp.write(track+'\n')
    fp.close()

#echauffement()
#lignes_droites()
#series()
#retour()
playlist(['echauffement.mp3','lignes.mp3','series.mp3','retour.mp3'])
