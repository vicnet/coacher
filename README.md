Script python pour géréner des programmes d'entrainement audio à partir de fichiers audio et de génération audio.

Utilisation
-----------

Pour l'instant (avant d'en faire un package ou d'avoir un format d'entrée),
modifier le fichier `coacher.py` directement pour inclure les instructions.

Le script ne gère en entrée que des fichiers wav en 22050 Hz.

Il génère un ou des fichiers wav aussi en 22050 Hz.

Il vaut mieux convertir les sorties en mp3 pour des raisons de volume de données.

Sous linux, la ou les sorties du script peuvent etre converties en mp3 avec lame
`lame <fichier.wav> <fichier.mp3>`

Sources audio
-------------

Les instructions sont générées avec le site:
  http://www.fromtexttospeech.com/
de synthèse vocale à partir de texte.
Remarque: seule la voie masculine française semble fonctionner...

Le script n'accepte pour l'instant que des fichiers wav en 22050 Hz.

Convertir les fichiers mp3 avec `lame --decode <fichier.mp3> <fichier.wav>`
Le script `d.sh` (alias d) effectue la convertion d'un fichier.

Pour écouter un fichier, vous pouvez utiliser vlc: `cvlc --play-and-exit <fichier>`

Astuces
-------

- générer des petits fichiers séparés et créer une playlit
  cela permet de passer à la suite de l'entraienement
  avec la touche 'avance rapide'
- insérer des notions de temps et des bips réguliers pour
  - entendre que la lecture est toujours active
    (que l'applicaiton audio ne s'est pas planté)
  - savoir où l'on en est, car on cours à fond par exemple,
    2mn çà parait très très long et on a besoin de repères
  - à la moitié du temps, cela permet aussi de savoir
    quand faire demi-tour !
