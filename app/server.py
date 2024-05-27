from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from app.serial_communication import SerialCommunication

app = Flask(__name__)
api = Api(app)

serial_comm = SerialCommunication(port='COM3')  # Cambiar por el puerto adecuado

class SendMessage(Resource):
    def post(self):
        data = request.get_json()
        message = data.get('message')
        if message:
            serial_comm.send_message(message)
            return {'status': 'Message sent'}, 200
        return {'error': 'No message provided'}, 400

class ReceiveMessage(Resource):
    def get(self):
        message = serial_comm.receive_message()
        if message:
            return {'message': message}, 200
        return {'message': 'No message received'}, 200

api.add_resource(SendMessage, '/send')
api.add_resource(ReceiveMessage, '/receive')

if __name__ == '__main__':
    app.run(debug=True)
