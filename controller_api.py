import requests
from time import sleep
from controller import WASDController

if __name__ == '__main__':

	wasd = WASDController()

	while True:
		action = wasd.get_action()
		r = requests.put('http://192.168.43.11:5000/Move', data=action)
		sleep(.05)
