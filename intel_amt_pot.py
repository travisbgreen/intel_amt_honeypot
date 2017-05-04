#!/usr/bin/env python3
import sys
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer

'''
inspired by https://isc.sans.edu/forums/diary/Do+you+have+Intel+AMT+Then+you+have+a+problem+today+Intel+Active+Management+Technology+INTELSA00075/22364/

Inteneded to be run with packet capture in front, e.g. 
sudo tcpdump -nnvv -i eth0 -w intel_AMT_honeypot.pcap 'portrange 16992-16994 or port 623 or port 624'
'''

PORT_NUMBERS = [16992, 16993, 16994, 16995, 623, 624]

html = '''
0294
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" >
<html><head><link rel=stylesheet href=styles.css>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Intel&reg; Active Management Technology</title></head>
<body>
<table class=header>
<tr><td valign=top nowrap>
<p class=top1>Intel<font class=r><sup>&reg;</sup></font> Active Management Technology
<td valign="top"><img src="logo.gif" align="right" alt="Intel">
</table>

<h1>Log On</h1>
<P>Log on to Intel&reg; Active Management Technology on this computer.
<P><form METHOD="GET" action="index.htm"><h2><input type=submit value="  Log On... ">
</h2></form></body></html>

0
'''

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.server_version = 'Intel(R) Active Management Technology 7.1.70'
        self.sys_version = ''
        self.protocol_version = 'HTTP/1.1'
        try:
            if self.path=="/":
                self.send_response(303)
                self.send_header('Location', '/logon.htm')
                self.send_header('Content-length', '0')
                self.end_headers()
            if self.path=="/logon.htm":
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Transfer-Encoding', 'chunked')
                self.send_header('Cache-Control', 'no cache')
                self.send_header('Expires', '26 Oct 1995 00:00:00 GMT')
                self.end_headers()
                self.wfile.write(bytes(html, "utf-8"))
            return
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

def main():
    servers = [HTTPServer(('', port_number), MyHandler) for port_number in PORT_NUMBERS]
    for httpd in servers:
        Thread(target=httpd.serve_forever).start()
        print(httpd)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)