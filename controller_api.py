import requests
from time import sleep
from controller import WASDController

if __name__ == '__main__':

	wasd = WASDController()

	while True:
		action = wasd.get_action()
		r = requests.put('http://127.0.0.1:5000/Move', data=action)
		sleep(.05)
