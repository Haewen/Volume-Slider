from pycaw.pycaw import AudioUtilities


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
