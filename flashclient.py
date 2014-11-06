#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Raspberry PI Arduino remote flasher
#
# Start flashserver.py on your Raspberry Pi and use this script do upload an
# Arduino hex file for flashing.
#
# github.com/kanflo
#

import requests
import argparse
import os

def upload_file(file_name, host, port, secret):
	print "Uploading '%s' to %s:%d" % (os.path.basename(file_name), host, port)
	try:
		url = 'http://%s:%s/%s' % (host, port, secret)
		files = {'file': (os.path.basename(file_name), open(file_name, 'rb'), 'application/binary', {'Expires': '0'})}
		r = requests.post(url, files=files)
		print "Server responded: %s" % (r.text)
	except requests.exceptions.ConnectionError:
		print "ERROR: Could not connect to host"
	except IOError:
		print "ERROR: File not found"


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--host", help="host where flashserver is running (defaults to localhost)")
	parser.add_argument("--port", help="well, port (defaults to 8888)", type=int)
	parser.add_argument("--secret", help="optional secret that must match that of the server")
	parser.add_argument("file", help="file to upload")
	args = parser.parse_args()

	host = args.host
	if host == None:
		host = "127.0.0.1"

	port = args.port
	if port == None:
		port = 8888

	secret = args.secret
	if secret == None:
		secret = "flash"

	upload_file(args.file, host, port, secret)
