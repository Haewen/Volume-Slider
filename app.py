from flask import Flask
from flask import render_template
from flask import request
import pythoncom

from volume import *
from flask.helpers import url_for
from werkzeug.utils import redirect

app = Flask(__name__)


@app.route('/')
def root():
    pythoncom.CoInitialize()
    sessions = get_session_data()
    return render_template("index.html", sessions=sessions)


@app.route('/volume', methods=["POST"])
def change_volume():
    json = request.get_json()
    pid = int(json["pid"])
    volume = int(json["volume"]) / 100.
    set_volume_for_process(pid, volume)
    return {"pid": pid, "volume": "volume"}


@app.route('/mute', methods=["POST"])
def mute():
    json = request.get_json()
    pid = int(json["pid"])
    to_mute = bool(json["mute"])
    print(to_mute)
    set_mute_process(pid, to_mute)
    return {"pid": pid, "mute": "mute"}


if __name__ == '__main__':
    app.run("0.0.0.0")
