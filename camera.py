# coding: utf-8

import io
import time
from threading import Lock
import picamera
import devices

class Camera(devices.Device):
	__frame = None
	__lock = Lock()

	def lock(func):
		def wrapper(*args, **kwargs):
			with Camera.__lock:
				return func(*args, **kwargs)
		return wrapper

	@lock
	def __init__(self):
		self.__cam = picamera.PiCamera()
		self.__cam.resolution = (320, 240)
		self.__cam.hflip = True
		self.__cam.vflip = True

		self.__cam.start_preview()
		time.sleep(2)

		self.__memstream = io.BytesIO()
		self.__iter = self.__cam.capture_continuous(self.__memstream, 'jpeg', use_video_port = True)

	@lock
	def get_frame(self):
		devices.Devices.notify_activity()
		return self.__frame

	@lock
	def update(self):
		self.__iter.next()
		self.__memstream.seek(0)
		self.__frame = self.__memstream.read()
		self.__memstream.seek(0)
		self.__memstream.truncate()

	@lock
	def shutdown(self):
		self.__frame = None
		self.__iter.close()
		self.__cam.stop_preview()
		self.__cam.close()

