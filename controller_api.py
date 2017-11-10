import requests
from time import sleep
from controller import WASDController
import argparse
import cv2
from io import StringIO
from PIL import Image

controllers = {'WASDController':WASDController}

def get_args_parser():
    parser = argparse.ArgumentParser(description='Control remote controlled car')
    parser.add_argument('ip_address', type=str, help='the IP address of the car')
    parser.add_argument('--controller', dest='controller', type=str, default='WASDController', help='the class of controller to be used')
    parser.add_argument('--delay', dest='delay', type=float, default=.2, help='the time delay of the event loop')

    return parser

def decode_image_and_display(img_buff, window):
    
    img = Image.open(img_buff)
    ret = cv2.imdecode(img.getdata(), 0)
    cv2.imshow(window, img_buff)

if __name__ == '__main__':

    args = get_args_parser().parse_args()
    Controller = controllers[args.controller]
    controller = Controller()
    ip_address = args.ip_address
    delay = args.delay
    action_prev = None
    window = 'DisplayWindow'
    cv2.namedWindow(window)

    while True:
        
        action = controller.get_action()
        if action != action_prev:
            r = requests.put('http://' + ip_address + ':5000/Move', data=action)
            p = requests.get('http://' + ip_address + ':5000/Picture')
            decode_image_and_display(StringIO(p.text), window)

        sleep(delay)
