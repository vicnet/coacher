#!/bin/bash
filename="${1%.*}"
lame $filename.wav $filename.mp3 -V2 --vbr-new -q0 --lowpass 19.7
