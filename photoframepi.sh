#!/bin/bash

BASE_DIR=/home/pi/photoframepi
STOP_FILE=/tmp/stop-photo-frame-pi
IMAGE_LIST=/tmp/photo-frame-pi.list

rm $STOP_FILE

# Iniciar la descarga de imágenes de cloudinary
cloudinary.py &

cd $BASE_DIR
while [ ! -f $STOP_FILE ] ; do
    ls -1t images/* | head -n 25 > | sort -R > $IMAGE_LIST
    fbi -1 -noverbose -a -t 8 logo.png > /dev/null 2>&1
    fbi -1 -noverbose -blend 1000 -a -t 2 -u -l $IMAGE_LIST > /dev/null 2>&1
done
rm $STOP_FILE
