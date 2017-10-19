import requests
from time import sleep
from controller import WASDController
import argparse

controllers = {'WASDController':WASDController}

def get_args_parser():
    parser = argparse.ArgumentParser(description='Control remote controlled car')
    parser.add_argument('ip_address', type=str, help='the IP address of the car')
    parser.add_argument('--controller', dest='controller', type=str, default='WASDController', help='the class of controller to be used')
    parser.add_argument('--delay', dest='delay', type=float, default=.2, help='the time delay of the event loop')

    return parser


if __name__ == '__main__':

    args = get_args_parser().parse_args()
    Controller = controllers[args.controller]
    controller = Controller()
    ip_address = args.ip_address
    delay = args.delay
    action_prev = None

    while True:
        
        action = controller.get_action()
        if action != action_prev:
            r = requests.put('http://' + ip_address + ':5000/Move', data=action)
            action_prev = action
        sleep(delay)
