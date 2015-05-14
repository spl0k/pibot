# coding: utf-8

from threading import Thread, Lock
import time
import traceback

class Device(object):
	def update(self):
		pass

	def shutdown(self):
		pass

class Devices(object):
	__thread = None
	__lock = Lock()
	__devices = {}
	__last_activity = 0

	@classmethod
	def set_classes(cls, dev_classes):
		if not dev_classes or not isinstance(dev_classes, list):
			raise Exception('Expecting a list')

		if any(map(lambda c: not issubclass(c, Device), dev_classes)):
			raise Exception ('One of the element is not a Device class')

		cls.__classes = dev_classes

	@classmethod
	def notify_activity(cls):
		with cls.__lock:
			if not cls.__thread:
				raise Exception('Thread not started!')

			cls.__last_activity = time.time()

	@classmethod
	def get_device_instance(cls, dev_class):
		if not issubclass(dev_class, Device):
			raise Exception('Trying to get something that is not a Device')

		cls.startup()
		return cls.__devices[dev_class]

	@classmethod
	def startup(cls):
		with cls.__lock:
			if cls.__thread:
				return

			if not hasattr(cls, '_Devices__classes'):
				raise Exception('Device classes not set')

			cls.__devices = { c: c() for c in cls.__classes }
			cls.__last_activity = time.time()
			cls.__thread = Thread(target = cls.__worker)
			cls.__thread.start()

	@classmethod
	def __worker(cls):
		while True:
			for device in cls.__devices.itervalues():
				try:
					device.update()
				except:
					traceback.print_exc()

			with cls.__lock:
				if time.time() - cls.__last_activity > 5:
					break

		for device in cls.__devices.itervalues():
			try:
				device.shutdown()
			except:
				traceback.print_exc()

		with cls.__lock:
			cls.__devices = {}
			cls.__last_activity = 0
			cls.__thread = None

