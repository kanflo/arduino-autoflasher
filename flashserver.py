#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Raspberry PI Arduino remote flasher
#
# Starts a tornado server listening for file POST from the flashclient.py
# script. Reveive and save file, reset the Arduino and call avrdude to flash the
# received firmware.
#
# You probably don't want this script running on anything connected
# to the Internet :)
#
# github.com/kanflo
#

import tornado
import tornado.ioloop
import tornado.web
import httplib
import os, uuid
from datetime import datetime
import argparse
import subprocess 

__UPLOADPATH__ = "/tmp/autoflash-"
__ATTYPE__ = "atmega328p"

def avr_reset():
	status = subprocess.call(["avrreset"])
	if status != 0:
		print " Failed"
	return status == 0
	
def avr_flash(fname):
	status = subprocess.call(["wc -l %s" % (fname)], shell=True)
#	status = subprocess.call(["cat %s" % (fname)], shell=True)
	status = subprocess.call(["avrdude -p%s -carduino -P/dev/ttyAMA0 -b57600 -D -Uflash:w:%s:i" % (__ATTYPE__, fname)], shell=True)
	if status != 0:
		print " Failed"
	return status == 0

# Kudos to https://gist.github.com/jehiah/398252
class ErrorHandler(tornado.web.RequestHandler):
    """Generates an error response with status_code for all requests."""
    def __init__(self, application, request, status_code):
        tornado.web.RequestHandler.__init__(self, application, request)
        self.set_status(status_code)
    
	# Might be write_error depending on the freshness of your tornado server
    def get_error_html(self, status_code, **kwargs):
		if status_code == 404:
			return "ERROR: Wrong dirty little secret? (%d)" % status_code
		else:
			return "%d: %s" % (status_code, httplib.responses[status_code])
    
    def prepare(self):
        raise tornado.web.HTTPError(self._status_code)

# Kudos to http://technobeans.wordpress.com/2012/09/17/tornado-file-uploads/
class Upload(tornado.web.RequestHandler):
	def post(self):
		fileinfo = self.request.files["file"][0]
		fname = __UPLOADPATH__ + fileinfo['filename'].decode('utf8')
		print "[%s] Received '%s' from %s" % (datetime.now(), fname, self.request.remote_ip)
		extn = os.path.splitext(fname)[1]
		fh = open(fname, 'w')
		fh.write(fileinfo['body'])
		fh.close()
		if not avr_reset():
			self.finish("ERROR: AVR reset failed")
			return
		if not avr_flash(fname):
			self.finish("ERROR: Flashing failed")
			return
		self.finish("Flashing successful")

	def write_error(self, status_code, **kwargs):
		print 'Client request ended in a %d' % (status_code)
		if status_code in [403, 404, 500, 503]:
			self.write('Error %s' % status_code)
		else:
			self.write('Fatal error (%d)' % status_code)


if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("--secret", help="optional secret that the client must provide")
	parser.add_argument("--port", help="port to listen on (defaults to 8888)", type=int)
	args = parser.parse_args()

	port = args.port
	if port == None:
		port = 8888
	secret = args.secret
	if secret == None:
		secret = "flash"

	# Override the tornado.web.ErrorHandler with our default ErrorHandler
	tornado.web.ErrorHandler = ErrorHandler

	application = tornado.web.Application([
		(r"/%s" % secret, Upload),
	], debug=True)

	print "Arduino flash server listening on port %s" % (port)
	application.listen(port)
	try:
		tornado.ioloop.IOLoop.instance().start()
	except KeyboardInterrupt:
		print "Exiting"
