import utils
import pyinotify
import imp
import sys
import os
import traceback

_mission_loaded = False
_mission = imp.new_module('empty_mission')
_started = False
_notifier = None

class _Handler(pyinotify.ProcessEvent):
    def process_IN_MODIFY(self, event):
        _onMissionChanged()

def start():
    global _notifier, _mission_path, _started, _watch_manager, _watch

    _watch_manager = pyinotify.WatchManager()
    _notifier = pyinotify.ThreadedNotifier(_watch_manager, _Handler())
    _notifier.start()
    _watch = _watch_manager.add_watch(_mission_path, pyinotify.IN_MODIFY)
    _started = True


def stop():
    global _started
    _started = False

def setMission(mission_path):
    global _mission_path, _mission_name, _notifier, _watch_manager, _watch
    _mission_path = mission_path
    _mission_name = mission_path.split('/')[-1].split('.')[0]
    _loadMission()
    if _notifier is not None:
        _watch_manager.rm_watch(_watch.values())
        _notifier.stop()

def getMission():
    global _mission_loaded, _mission
    return _mission_loaded, _mission

def _onMissionChanged():
    global _started
    if _started:
        _loadMission()

def _loadMission():
    global _mission_path, _mission_name, _mission, _mission_loaded

    if not os.access(_mission_path, os.R_OK):
        print("[ERROR] Can't open mission file '%s'" % _mission_path)
        _mission_loaded = False
        return []

    try:
        _mission = imp.load_source(_mission_name, _mission_path)
    except:
        traceback.print_exception(*sys.exc_info()[:2], tb=None, limit=0)
        print("[ERROR] Mission could not be loaded")
        _mission_loaded = False
        return []

    if not hasattr(_mission, "mission"):
        print("[ERROR] No mission() function found")
        _mission_loaded = False
        return []

    _mission_loaded = True
    print("[INFO] Mission loaded")
    return []
