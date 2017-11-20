from flask import Flask, request
from flask import send_file
from flask_restful import Resource, Api, reqparse
from car import Motors, Servo
import re
import cv2
import argparse
import numpy as np
from io import BytesIO

def get_args_parser():

    cmd_parser = argparse.ArgumentParser(description='Remote Controlled Car Restful API')
    cmd_parser.add_argument('--devno', dest='devno', type=int, default=0, help='device number of the video capture device')
    cmd_parser.add_argument('--host', dest='host', type=str, default='0.0.0.0', help='hostname; generally localhost or 0.0.0.0')
    cmd_parser.add_argument('--port', dest='port', type=int, default=5000, help='port to expose app on')
    cmd_parser.add_argument('--servo_pin', dest='servo_pin', type=int, default=None, help='gpio pin for servo')
    cmd_parser.add_argument('--servo_max_pw', dest='servo_max_pw', type=int, default=None, help='maximum pulse width for the servo')
    cmd_parser.add_argument('--servo_min_pw', dest='servo_min_pw', type=int, default=None, help='minimum pulse width for the servo')
    cmd_parser.add_argument('--servo_min_ang', dest='servo_min_ang', type=int, default=None, help='minimum_servo_angle')
    cmd_parser.add_argument('--servo_max_ang', dest='servo_max_ang', type=int, default=None, help='maximum_servo_angle')
    cmd_parser.add_argument('--motor_numbers', dest='motor_numbers', nargs='+', type=str, default=None, help='specify the device numbers of the motors')

    return cmd_parser

ACTION = {
    'speed':None,
    'angle':None
}

class Move(Resource):

    def __init__(self, *args, **kwargs):

        self.r_parser = reqparse.RequestParser()
        self.r_parser.add_argument('speed', default=None)
        self.r_parser.add_argument('angle', default=None)

        motor_kwargs = {}
        if kwargs.get('motor_numbers', None) is not None:
            motor_kwargs['motor_numbers'] = kwargs.pop('motor_numbers')
        servo_kwargs = kwargs

        self.motors = Motors(**motor_kwargs)
        self.servo = Servo(**servo_kwargs)

    def get(self):
        #return the action state
        return {'speed': ACTION['speed'], 'angle': ACTION['angle']}
    
    def put(self):
        #take an action here

        #get the action from the request
        args = self.r_parser.parse_args()
       
        #save the action state
        ACTION['speed'] = int(args['speed'])
        ACTION['angle'] = int(args['angle'])
        
        #take the action
        if ACTION['speed'] != None:
            self.motors.set_speed(ACTION['speed'])
        if ACTION['angle'] != None:
            self.servo.set_angle(ACTION['angle'])

class Picture(Resource):
    
    def __init__(self, *args, **kwargs):
        vid_dev_no = kwargs.pop('devno', 0)
        self.cam = cv2.VideoCapture(vid_dev_no)
        super(Picture, self).__init__(*args, **kwargs)

    def get(self):

        ret, frame = self.cam.read()
        shape = np.array(frame.shape)
        frame = np.concatenate([shape, frame.flatten()])
        frame = BytesIO(frame.tobytes())
        return send_file(frame, mimetype='image/jpeg')

if __name__ == '__main__':

    cmd_args = get_args_parser().parse_args()

    move_class_kwargs = {}

    if cmd_args.servo_pin is not None: move_class_kwargs['servo_pin'] = cmd_args.servo_pin
    if cmd_args.servo_max_pw is not None: move_class_kwargs['servo_max_pw'] = cmd_args.servo_max_pw
    if cmd_args.servo_min_pw is not None: move_class_kwargs['servo_min_pw'] = cmd_args.servo_min_pw
    if cmd_args.servo_max_ang is not None: move_class_kwargs['servo_max_ang'] = cmd_args.servo_max_ang
    if cmd_args.servo_min_ang is not None: move_class_kwargs['servo_min_ang'] = cmd_args.servo_min_ang
    if cmd_args.motor_numbers is not None: move_class_kwargs['motor_numbers'] = cmd_args.motor_numbers

    app = Flask(__name__)
    api = Api(app)

    api.add_resource(Move, '/Move', resource_class_kwargs=move_class_kwargs)
    api.add_resource(Picture, '/Picture', resource_class_kwargs={'devno':cmd_args.devno})
    app.run(debug=True, host=cmd_args.host, port=cmd_args.port)
