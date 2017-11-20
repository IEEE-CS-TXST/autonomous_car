import requests
from time import sleep
from controller import WASDController
import argparse
import cv2
from io import BytesIO
import numpy as np
from queue import Queue, Empty
from threading import Thread 

controllers = {'WASDController':WASDController}

def cleanup():
    cv2.destroyAllWindows()
    exit(1)

def get_args_parser():
    parser = argparse.ArgumentParser(description='Control remote controlled car')
    parser.add_argument('ip_address', type=str, help='the IP address of the car')
    parser.add_argument('--controller', dest='controller', type=str, default='WASDController', help='the class of controller to be used')
    parser.add_argument('--delay', dest='delay', type=float, default=.2, help='the time delay of the event loop')

    return parser

def decode_image_and_display(img_buff):
    
    img_data = np.fromstring(img_buff, dtype=np.uint64)
    shape = tuple(img_data[:3])
    frame = img_data[3:].reshape(shape)
    frame = frame.astype(np.uint8)

    cv2.imshow('DisplayWindow', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cleanup()

def enqueue_action(queue, controller):
    while True:
        queue.put_nowait(controller.get_action())

def dequeue_action(queue):
    try:
        return queue.get_nowait()
    except Empty:
        return None

if __name__ == '__main__':

    args = get_args_parser().parse_args()
    Controller = controllers[args.controller]
    controller = Controller()
    ip_address = args.ip_address
    delay = args.delay
    prev = None
    q = Queue()
    t = Thread(target=enqueue_action, args=(q, controller))
    t.daemon = True
    t.start()

    while True:
        
        action = dequeue_action(q)
        if action and action != prev:
            print(action)
            r = requests.put('http://' + ip_address + ':5000/Move', data=action)
            prev = action
        p = requests.get('http://' + ip_address + ':5000/Picture')
        decode_image_and_display(p.content)

        sleep(delay)
