from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
import os

# اسم التطبيق 'buzz'
buzz = Flask(__name__)
socketio = SocketIO(buzz)

# متغير عشان نحدد إذا فيه فائز ضغط قبلك
winner_name = None

@buzz.route('/')
def index():
    return render_template('index.html')

# التعديل هنا: نحدد المسار بدقة لملف الصوت
@buzz.route('/buzz.MP3.mp3')
def serve_audio():
    # هنا نقول له: ابحث في مجلد templates عن ملف الصوت
    # تأكد أن اسم الملف مطابق تماماً لما هو في جهازك
    return send_from_directory(os.path.join(buzz.root_path, 'templates'), 'buzz.MP3.mp3')

@socketio.on('press_event')
def handle_buzz(data):
    global winner_name
    
    print("--- SUCCESS! ---")
    
    if winner_name is None:
        winner_name = "Osama" # وضعنا اسمك هنا للفوز!
        print(f"WINNER: {winner_name}")
        emit('winner_announcement', {'winner': winner_name}, broadcast=True)
    else:
        print("Someone already pressed!")

@socketio.on('reset_game')
def reset():
    global winner_name
    winner_name = None
    print("Game Reset!")
    emit('game_restarted', broadcast=True)

if __name__ == '__main__':
    print("--- BUZZ Server is Starting ---")
    # host='0.0.0.0' ضرورية جداً ليعمل على الآيفون
    socketio.run(buzz, host='0.0.0.0', port=5000, debug=True)