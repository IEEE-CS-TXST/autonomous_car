import requests
from time import sleep

if __name__ == '__main__':
	while True:
		r = requests.get('http://127.0.0.1:5000')
		print(r.content)
		sleep(2)
