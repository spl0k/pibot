# coding: utf-8

import RPi.GPIO as GPIO
import devices

class Motors(devices.Device):
	PIN_ENABLE = 12
	PIN_LEFT_F = 26
	PIN_LEFT_R = 19
	PIN_RIGHT_F = 13
	PIN_RIGHT_R = 6

	def __init__(self):
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

	def drive(self, left, right):
		devices.Devices.notify_activity()

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

	def shutdown(self):
		GPIO.output(Motors.PIN_LEFT_F,  0)
		GPIO.output(Motors.PIN_LEFT_R,  0)
		GPIO.output(Motors.PIN_RIGHT_F, 0)
		GPIO.output(Motors.PIN_RIGHT_R, 0)
		GPIO.output(Motors.PIN_ENABLE,  0)

