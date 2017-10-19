from flask import Flask, request 
from flask_restful import Resource, Api, reqparse
from car import Motors, Servo

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
            
api.add_resource(Move, '/Move')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
