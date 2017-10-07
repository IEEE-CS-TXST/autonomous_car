from flask import Flask 
from flask_restful import Resource, Api
from car import Motor, Servo

app = Flask(__name__)
api = Api(app)
motor = Motor()
servo = Servo()

class Move(Resource):
	def get(self):
		#do something here
		motor.go(some content)
		servo.go(some content)
		return {'success':'True'}

api.add_resource(Move, '/')

if __name__ == '__main__':
	app.run(debug=True)