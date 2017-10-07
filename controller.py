import inputs as inp
import itertools as it

class Controller:

	_device = None

	def __init__(self):
		pass





if __name__ == '__main__':

	devices = inp.DeviceManger()

	print(devices)

	while True:
		k_events = inp.get_key()
		m_events = inp.get_mouse()
		g_events = inp.get_gamepad()

		for event in it.chain(k_events, m_evens, g_events):
			print(event.ev_type, event.code, event.state)

