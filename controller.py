import inputs as inp
import itertools as it
from time import sleep


class WASDController:

	_angle = 0
	_speed = 0
	_MAX_SPEED = 255
	_MAX_ANGLE = 60
	_MIN_ANGLE = -60
	_input = None

	def __init__(self):
		#the input function to pass
		self._input = inp.get_key

	def set_angle(self, key):
		#turn the car
		if key == 'KEY_A':
			self._angle = max(self._angle - 10, self._MIN_ANGLE)
		elif key == 'KEY_D':
			self._angle = min(self._angle + 10, self._MAX_ANGLE)

	def set_speed(self, key):
		#drive the car
		if key == 'KEY_W':
			self._speed = min(self._speed + 20, self._MAX_SPEED)
		elif key == 'KEY_S':
			self._speed = max(self._speed - 20, 0)

	def get_angle(self):
		return self._angle

	def get_speed(self):
		return self._speed

	def get_keys(self):
		return [event.code for event in self._input()]

	def get_action(self):
		#return an action
		keys = self.get_keys()

		for key in keys:
			self.set_angle(key)
			self.set_speed(key)

		return {'speed': self._speed, 'angle': self._angle}
