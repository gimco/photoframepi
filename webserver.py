#!/usr/bin/env python

from SimpleHTTPServer import SimpleHTTPRequestHandler
import SocketServer
import cgi
import datetime
import shutil
import re

STOP_FILE = '/tmp/stop-photo-frame-pi'
KEEP_RUNNING = True

class PhotoHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        global KEEP_RUNNING
        if self.path == '/stop':
            open(STOP_FILE, 'a').close()
            KEEP_RUNNING = False
        else:
            return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'] })
        if not form.has_key('photo'): return
        fileitem = form['photo']
        if not fileitem.file: return

        time = datetime.datetime.now().strftime('%Y%m%d.%H%M%S.')
        sanitized_filename = "".join(re.findall(r'[\w._-]', fileitem.filename))
        outpath = os.path.join('images', time + sanitized_filename)
        with open(outpath, 'wb') as fout:
            shutil.copyfileobj(fileitem.file, fout, 100000)
        call(["exiftran", "-i", "-a", outpath])

        self.send_response(301)
        self.send_header('Location','/thanks.html')
        self.end_headers()

PORT = 8000
httpd = SocketServer.TCPServer(("", PORT), PhotoHandler)
while KEEP_RUNNING:
    httpd.handle_request()
