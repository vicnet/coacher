#!/bin/bash
filename="${1%.*}"
lame --decode $filename.mp3 $filename.wav
