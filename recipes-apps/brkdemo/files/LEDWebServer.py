"""
--------------------------------------------------------------------------
Octavo Systems - OSD33MP157c-BRK Demo
--------------------------------------------------------------------------
License:
Copyright 2020 - Octavo Systems LLC
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright notice,
this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors
may be used to endorse or promote products derived from this software without
specific prior written permission.
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------
This file was modifed from the tutorial found here:
https://www.e-tinkers.com/2018/04/how-to-control-raspberry-pi-gpio-via-http-web-server/

It is a simple webserver used to display a single page and interact with the I/O
--------------------------------------------------------------------------
"""
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

#the actual hardware interface
import brkLed

host_name = ''  # bind to all interfaces
host_port = 8080


class MyServer(BaseHTTPRequestHandler):
    """ A special implementation of BaseHTTPRequestHander for reading data from
        and control GPIO of the OSD32MP1-BRK
    """

    def do_HEAD(self):
        """ do_HEAD() can be tested use curl command
            'curl -I http://server-ip-address:port'
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def _redirect(self, path):
        self.send_response(303)
        self.send_header('Content-type', 'text/html')
        self.send_header('Location', path)
        self.end_headers()

    def do_GET(self):
        """ do_GET() can be tested using curl command
            'curl http://server-ip-address:port'
        """
        # load the HTML template
        html = self.fileToStr('ledTemplate.html')
        # get the status of the D1 Green LED
        d1g_status = brkLed.ledStatus("d1g")
        d1g_disabled = self.setDisabled(d1g_status)

        # get the status of the D1 RED LED
        d1r_status = brkLed.ledStatus("d1r")
        d1r_disabled = self.setDisabled(d1r_status)

        # get the status of the D2 Green LED
        d2g_status = brkLed.ledStatus("d2g")
        d2g_disabled = self.setDisabled(d2g_status)

        self.do_HEAD()
        #return the completed  template
        self.wfile.write(html.format(**locals()).encode("utf-8"))

    def fileToStr(self, fileName):
        """Return a string containing the contents of the named file."""
        fin = open(fileName);
        contents = fin.read();
        fin.close()
        return contents

    def setDisabled(self, status):
        """
        returns a list to diable the appropriate button based on the status
        :param status: that current status
        :return: a list with the appropraite strings to disable the correct button given the status
        """
        if status =="OFF":
            return ["disabled", "", ""]
        if status == "ON":
            return ["", "disabled", ""]
        if status =="FLASHING":
            return ["", "", "disabled"]

    def do_POST(self):
        """ do_POST() can be tested using curl command
            'curl -d "submit=On" http://server-ip-address:port'
        """
        #get the POST agruments and parse them
        content_length = int(self.headers['Content-Length'])  # Get the size of data
        post_data = self.rfile.read(content_length).decode("utf-8")  # Get the data
        post_data = parse_qs(post_data)

        #pass the appropriate parameters based on which button was pressed
        if "d1g" in post_data:
            brkLed.ledSET("d1g", post_data["d1g"][0].lower())
        elif "d1r" in post_data:
            brkLed.ledSET("d1r", post_data["d1r"][0].lower())
        elif "d2g" in post_data:
            brkLed.ledSET("d2g", post_data["d2g"][0].lower())

        self._redirect('/')  # Redirect back to the root url'''

if __name__ == '__main__':
    #Reset all of the LEDs
    brkLed.ledRest()

    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()

