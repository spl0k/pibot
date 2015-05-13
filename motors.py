# coding: utf-8

import time
from threading import Timer, Lock
import RPi.GPIO as GPIO

class Motors(object):
	PIN_ENABLE = 12
	PIN_LEFT_F = 26
	PIN_LEFT_R = 19
	PIN_RIGHT_F = 13
	PIN_RIGHT_R = 6

	__timer = None
	__timer_lock = Lock()

	def __init__(self):
		if Motors.__timer:
			return

		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)

		GPIO.setup(Motors.PIN_ENABLE,  GPIO.OUT)
		GPIO.setup(Motors.PIN_LEFT_F,  GPIO.OUT)
		GPIO.setup(Motors.PIN_LEFT_R,  GPIO.OUT)
		GPIO.setup(Motors.PIN_RIGHT_F, GPIO.OUT)
		GPIO.setup(Motors.PIN_RIGHT_R, GPIO.OUT)

		GPIO.output(Motors.PIN_LEFT_F,  0)
		GPIO.output(Motors.PIN_LEFT_R,  0)
		GPIO.output(Motors.PIN_RIGHT_F, 0)
		GPIO.output(Motors.PIN_RIGHT_R, 0)
		GPIO.output(Motors.PIN_ENABLE,  1)

		with self.__timer_lock:
			Motors.__timer = Timer(5, Motors.__timeout)
			Motors.__timer.start()

	def drive(self, left, right):
		with self.__timer_lock:
			Motors.__timer.cancel()
			Motors.__timer = Timer(5, Motors.__timeout)
			Motors.__timer.start()

		if left == 0:
			GPIO.output(Motors.PIN_LEFT_F, 0)
			GPIO.output(Motors.PIN_LEFT_R, 0)
		elif left > 0:
			GPIO.output(Motors.PIN_LEFT_F, 1)
			GPIO.output(Motors.PIN_LEFT_R, 0)
		elif left < 0:
			GPIO.output(Motors.PIN_LEFT_F, 0)
			GPIO.output(Motors.PIN_LEFT_R, 1)

		if right == 0:
			GPIO.output(Motors.PIN_RIGHT_F, 0)
			GPIO.output(Motors.PIN_RIGHT_R, 0)
		elif right > 0:
			GPIO.output(Motors.PIN_RIGHT_F, 1)
			GPIO.output(Motors.PIN_RIGHT_R, 0)
		elif right < 0:
			GPIO.output(Motors.PIN_RIGHT_F, 0)
			GPIO.output(Motors.PIN_RIGHT_R, 1)

	def stop(self):
		self.drive(0, 0)

	def forward(self):
		self.drive(1, 1)

	def backward(self):
		self.drive(-1, -1)

	def forward_left(self):
		self.drive(0, 1)

	def forward_right(self):
		self.drive(1, 0)

	def backward_left(self):
		self.drive(0, -1)

	def backward_right(self):
		self.drive(-1, 0)

	def static_left(self):
		self.drive(-1, 1)

	def static_right(self):
		self.drive(1, -1)

	@classmethod
	def __timeout(cls):
		GPIO.output(Motors.PIN_LEFT_F,  0)
		GPIO.output(Motors.PIN_LEFT_R,  0)
		GPIO.output(Motors.PIN_RIGHT_F, 0)
		GPIO.output(Motors.PIN_RIGHT_R, 0)
		GPIO.output(Motors.PIN_ENABLE,  0)

		with cls.__timer_lock:
			cls.__timer = None

