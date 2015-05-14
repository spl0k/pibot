#!/usr/bin/env python
# coding: utf-8

from flask import Flask, render_template, Response, request
import time
from devices import Devices
from camera import Camera
from motors import Motors

app = Flask(__name__)
Devices.set_classes([ Camera, Motors ])

@app.route('/')
def index():
	Devices.startup()
	return render_template('index.html')

def generate_stream(cam):
	while True:
		frame = cam.get_frame()
		if not frame:
			app.logger.warn('Camera sent an empty frame')
			time.sleep(0.1)
			frame = cam.get_frame()
			if not frame:
				app.logger.error('Frame still null')
				break

		yield b'--mjpegboundary\r\n' + \
			b'Content-Type: image/jpeg\r\n' + \
			b'Content-Length: ' + str(len(frame)) + b'\r\n' + \
			b'\r\n' + \
			frame + \
			b'\r\n'

@app.route('/stream')
def stream():
	cam = Devices.get_device_instance(Camera)
	return Response(generate_stream(cam), mimetype = 'multipart/x-mixed-replace; boundary=mjpegboundary')

@app.route('/move', methods = [ 'POST' ])
def move():
	commands = [
		[ Motors.backward_left,  Motors.static_left,  Motors.forward_left  ],
		[ Motors.backward,       Motors.stop,         Motors.forward       ],
		[ Motors.backward_right, Motors.static_right, Motors.forward_right ]
	]
	x, y = map(lambda k: int(request.form[k]), [ 'x', 'y' ])
	commands[x + 1][y + 1](Devices.get_device_instance(Motors))
	return '{}'

if __name__ == '__main__':
	import argparse

	argparser = argparse.ArgumentParser(add_help = False)
	argparser.add_argument('-h', '--host', default = '0.0.0.0')
	argparser.add_argument('-p', '--port', type = int, default = 5000)
	argparser.add_argument('-d', '--debug', action = 'store_true')
	argparser.add_argument('-t', '--threaded', action = 'store_true')
	args = argparser.parse_args()

	app.run(host = args.host, port = args.port, debug = args.debug, threaded = args.threaded)

