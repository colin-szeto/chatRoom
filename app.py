from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO, join_room, leave_room
from flask_login import current_user

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template("home.html")

@app.route("/chat")
def chat():

    room = request.args.get("room")
    if room:
        return render_template('chat/chat.html', username=current_user.username, room=room)
    else:
        return redirect('/chatIndex')

@app.route("/chatIndex")
def chatIndex():
    return render_template('chat/chat_index.html')


@socketio.on('send_message')
def handle_send_message_event(data):
    app.logger.info("{} has joined the room {}".format(data['username'],
                                                       data['room'],
                                                       data['message']))
    # ensure message in corresponding room
    socketio.emit('receive_message', data, room=data['room'])

@socketio.on('join_room')
def handle_join_room_event(data):
    # saving the time that joined the room
    app.logger.info("{} has joined the room {}".format(data['username'], data['room']))
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])

@socketio.on('leave_room')
def handle_leave_room_event(data):
    app.logger.info("{} has left the room {}".format(data['username'], data['room']))
    leave_room(data['room'])
    socketio.emit('leave_room_announcement', data, room=data['room'])

if __name__ == "__main__":
    # runs the application on the repl development server
    socketio.run(app, debug=True, host='127.0.0.1', port='5000')