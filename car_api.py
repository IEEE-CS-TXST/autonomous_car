from flask import Flask, request
from flask import send_file
from flask_restful import Resource, Api, reqparse
from car import Motors, Servo
import re
import cv2
import subprocess
from PIL import Image
from io import StringIO

app = Flask(__name__)
api = Api(app)
motors = Motors()
servo = Servo()
parser = reqparse.RequestParser()
parser.add_argument('speed', default=None)
parser.add_argument('angle', default=None)

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
        args = parser.parse_args()
       
        #save the action state
        ACTION['speed'] = int(args['speed'])
        ACTION['angle'] = int(args['angle'])
        
        #take the action
        if ACTION['speed'] != None:
            motors.set_speed(ACTION['speed'])
        if ACTION['angle'] != None:
            servo.set_angle(ACTION['angle'])

class Picture(Resource):
    
    def __init__(self, *args, **kwargs):
        self.cam = cv2.VideoCapture(0)
        super(Picture, self).__init__(*args, **kwargs)

    def get(self):
        ret, frame = self.cam.read()
        image = Image.fromarray(frame)
        buff = StringIO()
        image.save(buff, 'JPEG')
        ret, img_encoded = cv2.imencode('JPEG', buff.getvalue())
        return send_file(img_encoded)

api.add_resource(Move, '/Move')
api.add_resource(Picture, '/Picture')

if __name__ == '__main__':
    app.run(debug=True, host='localhost')
