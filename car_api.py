from flask import Flask, request 
from flask_restful import Resource, Api, reqparse
#from car import Motor, Servo

app = Flask(__name__)
api = Api(app)
#motor = Motor()
#servo = Servo()
parser = reqparse.RequestParser()
parser.add_argument('speed')
parser.add_argument('angle')

ACTION = {
	'speed':None,
	'angle':None
}

class Move(Resource):

	def get(self, action):
		#do something here
		return {'speed': ACTION['speed'], 'angle': ACTION['angle']}

	def put(self, action):
		#take an action here
		args = parser.parse_args()
		print(args)
		ACTION['speed'] = args['speed']
		ACTION['angle'] = args['angle']

		#if ACTION['speed'] != None:
			#motor.set_speed(ACTION['speed'])
		#if ACTION['angle'] != None:
			#servo.set_angle(ACTION['angle'])

api.add_resource(Move, '/<string:action>')

if __name__ == '__main__':
	app.run(debug=True)