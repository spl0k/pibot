# coding: utf-8

import time
import io
from threading import Thread, Condition
import picamera

class Camera(object):
	__thread = None
	__frame = None
	__frame_cond = None
	__last_read = 0

	def __init__(self):
		if Camera.__thread:
			return

		if not Camera.__frame_cond:
			Camera.__frame_cond = Condition()

		Camera.__thread = Thread(target = self.__capture)
		Camera.__thread.start()

		with Camera.__frame_cond:
			Camera.__frame_cond.wait()

	def get_frame(self):
		Camera.__last_read = time.time()
		with Camera.__frame_cond:
			return Camera.__frame

	@classmethod
	def __capture(cls):
		with picamera.PiCamera() as cam:
			cam.resolution = (320, 240)
			cam.hflip = True
			cam.vflip = True

			cam.start_preview()
			time.sleep(2)

			stream = io.BytesIO()
			for _ in cam.capture_continuous(stream, 'jpeg', use_video_port = True):
				stream.seek(0)
				with cls.__frame_cond:
					cls.__frame = stream.read()
					cls.__frame_cond.notify()
				stream.seek(0)
				stream.truncate()

				if cls.__last_read > 0 and time.time() - cls.__last_read > 10:
					break

		with cls.__frame_cond:
			cls.__frame = None
		cls.__thread = None
		cls.__last_read = 0

