from flask import Flask, request, abort, render_template
from flask_socketio import SocketIO, send, emit

from osc import Client

app = Flask(__name__)

socketio = SocketIO(app, cors_allowed_origins="*")

# to keep track of active clients
clients = []

client = Client()
print("Setting up OSC client at", client.ip, "and port", client.port)


@app.route("/")
def hello():
    return render_template("index.html")


# event used to parse the MIDI data from the socket connection
@socketio.on('midi')
def handle_midi(json):
    # key = json['key']
    print("\n")
    client.send("THIS IS FROM THE SERVER")
    return "Success"


# incoming unnamed message events
@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


# connection event
@socketio.on('connect')
def handle_connect():
    print("Client connected with ID: " + request.sid)
    clients.append(request.sid)
    pass


# disconnection event
@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected with ID: " + request.sid)
    clients.remove(request.sid)
    pass


if __name__ == '__main__':
    # print('Flask configs', app.config)
    host = "127.0.0.1"
    port = 5000
    print("Setting up web server on", host, "at port", port)
    socketio.run(
        app,
        host=host,
        port=port,
        debug=False,
        use_reloader=True
    )