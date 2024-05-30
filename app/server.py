from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from app.serial_communication import SerialCommunication
import threading
import time

app = Flask(__name__)
CORS(app)  # Esto permite todas las solicitudes de CORS
api = Api(app)
socketio = SocketIO(app, cors_allowed_origins="*")

try:
    serial_comm = SerialCommunication(port='COM13')  # Cambiar por el puerto adecuado
except serial.SerialException as e:
    print(f"Error al abrir el puerto serial: {e}")

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

def listen_to_serial():
    while True:
        message = serial_comm.receive_message()
        if message:
            print(f"Mensaje recibido del puerto COM: {message}")  # Log para diagnóstico
            socketio.emit('serial_message', {'message': message})
        time.sleep(1)  # Añadir una pequeña pausa para evitar que el bucle consuma demasiados recursos

if __name__ == '__main__':
    thread = threading.Thread(target=listen_to_serial)
    thread.daemon = True
    thread.start()
    socketio.run(app, debug=True)
