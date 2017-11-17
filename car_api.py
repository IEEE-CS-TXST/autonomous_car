from flask import Flask, request
from flask import send_file
from flask_restful import Resource, Api, reqparse
from car import Motors, Servo
import re
import cv2
import argparse
import numpy as np
from io import BytesIO

app = Flask(__name__)
api = Api(app)
motors = Motors()
servo = Servo()
r_parser = reqparse.RequestParser()
r_parser.add_argument('speed', default=None)
r_parser.add_argument('angle', default=None)

def get_args_parser():

    cmd_parser = argparse.ArgumentParser(description='Remote Controlled Car Restful API')
    cmd_parser.add_argument('--devno', dest='devno', type=int, default=0, help='device number of the video capture device')
    cmd_parser.add_argument('--host', dest='host', type=str, default='0.0.0.0', help='hostname; generally localhost or 0.0.0.0')
    cmd_parser.add_argument('--port', dest='port', type=int, default=5000, help='port to expose app on')
    return cmd_parser

ACTION = {
    'speed':None,
    'angle':None
}

class Move(Resource):

    def get(self):
        #return the action state
        return {'speed': ACTION['speed'], 'angle': ACTION['angle']}
    
    def put(self):
        #take an action here

        #get the action from the request
        args = r_parser.parse_args()
       
        #save the action state
        ACTION['speed'] = int(args['speed'])
        ACTION['angle'] = int(args['angle'])
        
        take the action
        if ACTION['speed'] != None:
            motors.set_speed(ACTION['speed'])
        if ACTION['angle'] != None:
            servo.set_angle(ACTION['angle'])

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
    api.add_resource(Move, '/Move')
    api.add_resource(Picture, '/Picture', resource_class_kwargs={'devno':cmd_args.devno})
    app.run(debug=True, host=cmd_args.host, port=cmd_args.port)
