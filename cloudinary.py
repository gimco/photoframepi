#!/usr/bin/env python

import sys
import json
import urllib
import time
from os.path import isfile
from datetime import datetime

STOP_FILE = '/tmp/stop-photo-frame-pi'

CLOUDINARY_API = 'https://XXX:YYYY@api.cloudinary.com/v1_1/gimco/resources/image?max_results=500&direction=asc&start_at=%s'
created_at = '2017-01-01'

while not isfile(STOP_FILE):
    try:
        url = CLOUDINARY_API % created_at
        print str(datetime.now()), ' Buscando nuevos ficheros > ', created_at 
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        for resource in data['resources']:
            image = 'images/' + resource['public_id'] + '.jpg'
            url = resource['url']
            created_at = resource['created_at']
            print 'Comprobando existencia de ' + image
            if not isfile(image):
                print 'Downlading ' + image
                urllib.urlretrieve(url, image)
    except: print 'Error!', sys.exc_info()
    print 'Fin de comprobacion, esperando 10 segundos'
    time.sleep(10)
