#!/bin/bash
filename="${1%.*}"
lame --decode data/original/$filename.mp3 data/$filename.wav
