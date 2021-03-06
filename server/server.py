from flask import Flask, request, abort, render_template
from flask_socketio import SocketIO, send, emit

from osc import Client

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['ENV'] = 'development'

socketio = SocketIO(app, cors_allowed_origins="*")



#####   OSC client

clients = []
ips = ["127.0.0.1", "10.24.227.10"]
port = 3000

for ip in ips:
    client = Client(ip, port)
    print("Setting up OSC client at", client.ip, "and port", client.port)
    clients.append(client)

######

@app.route("/")
def hello():
    return render_template("index.html")


# event used to parse the MIDI data from the socket connection
@socketio.on('midi')
def handle_midi(json):
    chord = json['chord']
    if chord:
        print("Chord received", chord)
        for client in clients:
            print("Sending chord", chord, "to IP", client.ip)
            client.send(chord, "/chords")
        return "Success"
    else:
        return "Failure"


# incoming unnamed message events
@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)


# connection event
@socketio.on('connect')
def handle_connect():
    print("Client connected with ID: " + request.sid)
    pass


# disconnection event
@socketio.on('disconnect')
def handle_disconnect():
    print("Client disconnected with ID: " + request.sid)
    pass


if __name__ == '__main__':
    print('Flask configs', app.config)
    # host = "127.0.0.1"
    host = "0.0.0.0"
    port = 5000
    print("Setting up web server on", host, "at port", port)
    socketio.run(
        app,
        host=host,
        port=port,
        debug=False,
        use_reloader=True
    )