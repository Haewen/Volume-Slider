from __future__ import print_function

from ctypes import POINTER, cast

from comtypes import CLSCTX_ALL

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


def get_sessions():
    return AudioUtilities.GetAllSessions()


def get_session_data():
    sessions = get_sessions()
    data = []
    for session in sessions:
        if session.Process:
            volume = session.SimpleAudioVolume
            session_data = {}
            session_data["name"] = session.Process.name()
            session_data["process_id"] = session.Process.pid
            session_data["is_muted"] = volume.GetMute()
            session_data["volume"] = volume.GetMasterVolume()
            data.append(session_data)
    return data


def get_session(pid):
    sessions = get_sessions()
    for session in sessions:
        if session.Process and session.Process.pid == pid:
            volume = session.SimpleAudioVolume
            session_data = {}
            session_data["name"] = session.Process.name()
            session_data["process_id"] = session.Process.pid
            session_data["is_muted"] = volume.GetMute()
            session_data["volume"] = volume.GetMasterVolume()
            return session_data
    return None


def get_session_volume(pid):
    sessions = get_sessions()
    for session in sessions:
        volume = session.SimpleAudioVolume
        if session.Process and session.Process.pid == pid:
            return volume
    return None


def set_mute_process(pid, mute):
    volume = get_session_volume(pid)
    if volume:
        volume.SetMute(1 if mute else 0, None)


def set_volume_for_process(pid, volume_level):
    volume = get_session_volume(pid)
    if volume:
        # volume is between 0.0 and 1.0
        volume_value = min(1.0, max(0.0, volume_level))
        volume.SetMasterVolume(volume_value, None)


def get_volume_for_process(pid):
    volume = get_session_volume(pid)
    if volume:
        return volume.GetMasterVolume()


def get_mute_for_process(pid):
    volume = get_session_volume(pid)
    if volume:
        return volume.GetMute()


def get_master_session():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))


def get_master_data():
    session = get_master_session()
    master_data = {}
    master_data["is_muted"] = session.GetMute()
    master_data["volume"] = session.GetMasterVolumeLevelScalar()
    return master_data


def get_master_volume():
    session = get_master_session()
    return session.GetMasterVolumeLevelScalar()


def get_mute_master():
    session = get_master_session()
    return session.GetMute()


def set_master_volume(volume_level):
    session = get_master_session()
    session.SetMasterVolumeLevelScalar(volume_level, None)


def set_mute_master(mute):
    session = get_master_session()
    session.SetMute(1 if mute else 0, None)
