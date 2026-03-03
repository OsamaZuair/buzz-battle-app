import eventlet
eventlet.monkey_patch()  # ضروري جداً أن يكون السطر رقم 1 ليعمل البث المباشر

from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
import os

# اسم التطبيق 'buzz'
buzz = Flask(__name__)
# أضفنا cors_allowed_origins="*" عشان يسمح بالاتصال من أي جوال
socketio = SocketIO(buzz, cors_allowed_origins="*")

winner_name = None

@buzz.route('/')
def index():
    return render_template('index.html')

@buzz.route('/buzz.MP3.mp3')
def serve_audio():
    return send_from_directory(os.path.join(buzz.root_path, 'templates'), 'buzz.MP3.mp3')

@socketio.on('press_event')
def handle_buzz(data):
    global winner_name
    
    # استلام اسم المتسابق من الجوال
    player_name = data.get('name', 'شخص ما')
    
    if winner_name is None:
        winner_name = player_name
        print(f"الفائز هو: {winner_name}")
        emit('winner_announcement', {'winner': winner_name}, broadcast=True)
    else:
        print(f"محاولة ضغط متأخرة من: {player_name}")

@socketio.on('reset_game')
def reset():
    global winner_name
    winner_name = None
    print("تم إعادة ضبط اللعبة!")
    emit('game_restarted', broadcast=True)

if __name__ == '__main__':
    # أزلنا port=5000 و host لأن السيرفر الرسمي هو من يحددهم
    socketio.run(buzz)