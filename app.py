#!/usr/bin/env python
# coding: utf-8

from flask import Flask, render_template, Response
from camera import Camera

app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

def generate_stream(cam):
	while True:
		frame = cam.get_frame()
		yield b'--mjpegboundary\r\n' + \
			b'Content-Type: image/jpeg\r\n' + \
			b'Content-Length: ' + str(len(frame)) + b'\r\n' + \
			b'\r\n' + \
			frame + \
			b'\r\n'

@app.route('/stream')
def stream():
	return Response(generate_stream(Camera()), mimetype = 'multipart/x-mixed-replace; boundary=mjpegboundary')

if __name__ == '__main__':
	import argparse

	argparser = argparse.ArgumentParser(add_help = False)
	argparser.add_argument('-h', '--host', default = '0.0.0.0')
	argparser.add_argument('-p', '--port', type = int, default = 5000)
	argparser.add_argument('-d', '--debug', action = 'store_true')
	argparser.add_argument('-t', '--threaded', action = 'store_true')
	args = argparser.parse_args()

	app.run(host = args.host, port = args.port, debug = args.debug, threaded = args.threaded)

