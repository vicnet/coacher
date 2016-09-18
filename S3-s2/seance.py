from coacher import Coacher

# les lignes droites de 80m sont calculees a 30s en gros.
# TODO prevoir un mecanisme pour parametrer la vitesse
# et calculer le temps en fonction de la distance

sec = 1000 # 1000 ms
min = 60*sec # 60s

coacher = Coacher('S3-s2')

def beeps():
    beep1 = coacher.read_wav('beep-07')
    beep2 = coacher.sinewave(freq=1000, volume=28000)
    beeps = beep1+coacher.silence(1000-coacher.duration(beep1))
    return beeps*3+beep2*3

bs = beeps()

ibeep = coacher.sinewave(freq=3000, duration=200, volume=28000)

def silence(t):
    return coacher.silence(t)

# 1 seconde de silence avant beeps
s1 = silence(1*sec)
# separateur intermots
si = silence(500)

def course(t, tb=1*min):
    """Running silence.
    As silence but with intermediate bips and half time"""
    # generate half time
    middle = ibeep + silence(200) + ibeep
    tmiddle = coacher.duration(middle)
    tibeep = coacher.duration(ibeep)
    channel = []
    for ti in range(0, int(t/2-tb-tb/2), tb):
        channel += silence(tb-tibeep)
        channel += ibeep
    channel += silence(t/2-coacher.duration(channel)-tmiddle/2)
    channel =\
          channel\
        + middle\
        + channel
    return channel

def step(t, tb=1*min):
    """Running silence.
    As silence but with intermediate bips, no half time"""
    # generate half time
    tibeep = coacher.duration(ibeep)
    channel = []
    for ti in range(0, int(t-tb-tb/2), tb):
        channel += silence(tb-tibeep)
        channel += ibeep
    channel += silence(t-coacher.duration(channel))
    return channel

def expli_seance():
    plat = coacher.read_wav('plat2mn')
    cote = coacher.read_wav('cote1mn15')
    descente = coacher.read_wav('descente1mn')
    recup = coacher.read_wav('recup3mn')
    series = coacher.read_wav('5series')
    channel =\
          series\
        + si + plat\
        + si + cote\
        + si + descente\
        + si + recup
    return channel

def explication():
    channel  = coacher.read_wav('semaine3')
    channel += s1+coacher.read_wav('seance2')
    channel += s1*2+coacher.read_wav('footing25mn')
    channel += si+coacher.read_wav('5lignes')
    channel += si+expli_seance()
    channel += si+coacher.read_wav('calme10mn')
    channel += s1*2
    coacher.save_wav('explication', channel)

def echauffement():
    footing = coacher.read_wav('footing25mn')
    reste15 = coacher.read_wav('reste15mn')
    reste5  = coacher.read_wav('reste5mn')
    channel =\
        footing\
        + step(10*min)\
        + reste15\
        + step(10*min)\
        + reste5\
        + step(5*min)
    coacher.save_wav('echauffement',channel)

def lignes_droites():
    def ligne(ligne_wav, recup_wav='recup'):
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
    lignes = coacher.read_wav('5lignes')
    channel = \
          lignes + silence(1*sec)\
        + ligne('1re-ligne')\
        + ligne('2e-ligne')\
        + ligne('3e-ligne')\
        + ligne('4e-ligne')\
        + ligne('der-ligne')
    coacher.save_wav('lignes',channel)

def serie(serie_wav):
    # load files
    plat = coacher.read_wav('plat2mn')
    cote = coacher.read_wav('cote1mn15')
    descente = coacher.read_wav('descente1mn')
    recup = coacher.read_wav('recup3mn')
    cserie = coacher.read_wav(serie_wav)
    cbeeps = beeps()
    tbeeps = coacher.duration(cbeeps)
    # generate prog
    channel =\
          cserie + silence(1*sec)\
        + plat + s1 + cbeeps\
        + course(2*min-tbeeps,30*sec) + cbeeps\
        + s1 + cote + s1 + cbeeps\
        + course(1*min+15*sec-tbeeps) + cbeeps\
        + s1 + descente + s1 + cbeeps\
        + course(1*min) + cbeeps\
        + recup + course(3*min,30*sec)
    coacher.save_wav(serie_wav, channel)

def series():
    channel =\
        expli_seance()\
        + s1
    coacher.save_wav('series',channel)

def retour():
    retour = coacher.read_wav('calme10mn')
    reste5  = coacher.read_wav('reste5mn')
    channel =\
        retour\
        + step(5*min)\
        + reste5\
        + step(5*min)\
        + beeps()
    coacher.save_wav('retour',channel)

explication()
echauffement()
lignes_droites()
series()
serie('1re-serie')
serie('2e-serie')
serie('3e-serie')
serie('4e-serie')
serie('der-serie')
retour()
coacher.save_playlist()

#['explication.mp3', 'echauffement.mp3', 'lignes.mp3', 'series.mp3', 'retour.mp3']
