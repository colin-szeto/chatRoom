from flask import Flask, render_template, request, redirect
from flask_socketio import SocketIO, join_room, leave_room
from flask_login import current_user
from socket import *

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/pretty')
def prettyPage():
    return render_template("chat/chatCSS.html")

@app.route("/chat")
def chat():

    room = request.args.get("room")
    username = request.args.get("username")
    if room:
        # return render_template('chat/chat.html', username=current_user.username, room=room)
        # return render_template('chat/chat.html', username=username, room=room)
        return render_template('chat/chatAreaCss.html', username=username, room=room, ip_address=ip_address, port_=port_ )
    else:
        return redirect('/chatIndex')

@app.route("/chatOld")
def chat_old():
    room = request.args.get("room")
    username = request.args.get("username")
    if room:
        # return render_template('chat/chat.html', username=current_user.username, room=room)
        # return render_template('chat/chat.html', username=username, room=room)
        return render_template('chat/chat.html', username=username, room=room, ip_address=ip_address, port_=port_ )
    else:
        return redirect('/chatIndex')

@app.route("/chatIndex")
def chatIndex():
    return render_template('chat/chat_index.html')

@app.route("/chatArea")
def chatArea():
    return render_template('chat/chatAreaCss.html')


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

ip_address = "127.0.0.1"
port_ = "3030"
if __name__ == "__main__":
    # runs the application on the repl development server
    socketio.run(app, debug=True, host=ip_address, port=port_)