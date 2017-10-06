from flask import Flask 
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Move(Resource):
	def get(self):
		#do something here
		return {'success':'True'}

api.add_resource(Move, '/')

if __name__ == '__main__':
	app.run(debug=True)