from Adafruit_MotorHAT import Adafruit_MotorHAT
from gpiozero import AngularServo
import atexit

MOTOR_NUMBERS = [3, 4]
SERVO_PIN = 17
SERVO_MIN_PULSE_WIDTH = .0008
SERVO_MAX_PULSE_WIDTH = .0018
SERVO_MIN_ANGLE = -60
SERVO_MAX_ANGLE = 60

class Motors:

	_MH = None
	_motor_numbers = None
	_motors = None
	_speed = 0

	def __init__(self, motor_numbers=MOTOR_NUMBERS):
		#Constructor, take care of setup
		self._motor_numbers = motor_numbers
		atexit.register(self._turn_off_motor)
		self._MH = Adafruit_MotorHAT(addr=0x60)
		self._motors = [self._MH.getMotor(self._motor_numbers[0]),
				self._MH.getMotor(self._motor_numbers[1])]

	def set_speed(self, speed):
		#set the motor speed
		if speed >= 0:
			for motor in self._motors:
				motor.run(Adafruit_MotorHAT.FORWARD)
				self._speed = speed
				motor.setSpeed(speed)
		else:
			for motor in self._motors:
				motor.run(Adafruit_MotorHAT.BACKWARD)
				self._speed = speed
				motor.setSpeed(-1 * speed)

	def get_speed(self):
		#get the motor speed
		return self._speed

	def _turn_off_motor(self):
		#turn off the motor when shutdown
		for motor_number in self._motor_numbers:
			self._MH.getMotor(motor_number).run(Adafruit_MotorHAT.RELEASE)

class Servo:

	_servo = None
	_angle = 0
	_pin = None
	_min_angle = None
	_max_angle = None
	_min_pulse_width = None
	_max_pulse_width = None

	def __init__(self, servo_pin=SERVO_PIN, min_pulse_width=SERVO_MIN_PULSE_WIDTH,
		max_pulse_width=SERVO_MAX_PULSE_WIDTH, min_angle=SERVO_MIN_ANGLE, 
		max_angle=SERVO_MAX_ANGLE):
		#Constructor, take care of setup
		self._pin = servo_pin
		self._min_angle = min_angle
		self._max_angle = max_angle
		self._min_pulse_width = min_pulse_width
		self._max_pulse_width = max_pulse_width

		self._servo = AngularServo(
			pin = self._pin, 
			min_pulse_width = self._min_pulse_width,
			max_pulse_width = self._max_pulse_width,
			min_angle = self._min_angle,
			max_angle = self._max_angle)

		atexit.register(self.deactivate)

	def set_angle(self, angle):
		#turn the servo, respect the parameters
		if angle > 0:
			self._angle = min(angle, self._max_angle)
		else:
			self._angle = max(angle, self._min_angle)

		self._servo.angle = self._angle

	def get_angle(self):
		#return the current servo angle
		return self._angle

	def set_frame_width(self, frame_width):
		#set the frame width
		self._servo.frame_width = frame_width

	def get_frame_width(self):
		#get the frame wieth
		return self._servo.frame_width

	def set_pulse_width(self, pulse_width):
		#set the pulse width
		self._servo.pulse_width = pulse_width

	def get_pulse_width(self):
		return sef._servo.pulse_width

	def deactivate(self):
		#deactivate the servo
		self._servo.value = None

	def is_active(self):
		return self._servo.is_active()

	def value(self):
		return self._servo.value




