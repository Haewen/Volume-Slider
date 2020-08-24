from flask import Flask
from flask import render_template
from flask import request
import pythoncom
import sys
import os

from volume import *
from flask.helpers import url_for
from werkzeug.utils import redirect


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


if getattr(sys, 'frozen', False):
    template_folder = resource_path('templates')
    static_folder = resource_path('static')
    app = Flask(__name__, template_folder=template_folder,
                static_folder=static_folder)
else:
    app = Flask(__name__)


@app.route('/')
def root():
    pythoncom.CoInitialize()
    sessions = get_session_data()
    master = get_master_data()
    return render_template("index.html", sessions=sessions, master=master)


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
    set_mute_process(pid, to_mute)
    return render_template("card.html", session=get_session(pid))


@app.route('/mutemaster', methods=["POST"])
def mutemaster():
    json = request.get_json()
    to_mute = bool(json["mute"])
    set_mute_master(to_mute)
    return render_template("master_card.html", master=get_master_data())


@app.route('/mastervolume', methods=["POST"])
def mastervolume():
    json = request.get_json()
    volume = int(json["volume"]) / 100.
    set_master_volume(volume)
    return {"volume": volume}


if __name__ == '__main__':
    app.run("0.0.0.0")
