import utils
import mission_loader
import sys
import rospy
from droneMsgsROS.msg import CompletedMission
import traceback

_started = False

def start():
    global _mission_thread, _started

    if _started:
        print("[ERROR] Mission has already been started")
        return

    valid, _mission = mission_loader.getMission()
    if not valid:
        print("[ERROR] No correct mission file found")
        return

    def mission():
        global _started
        mission_loader.stop()
        completed_mission_pub = rospy.Publisher('completed_mission', CompletedMission,queue_size=1)
        completed_mission_msg = CompletedMission()
        try:
            _mission.mission()
            completed_mission_msg.result = "Completed Mission"
        except SystemExit:
            # This means the thread was killed by me
            # Consider doing an emergency land
            print("[INFO] Mission aborted")
            completed_mission_msg.result = "Aborted Mission"
        except:
            traceback.print_exception(*sys.exc_info()[:2], tb=None, limit=0)
            print("[ERROR] Runtime error encountered in mission")
        completed_mission_pub.publish(completed_mission_msg)
        _started = False
        mission_loader.start()

    _mission_thread = utils.KThread(target=mission)
    _mission_thread.start()
    _started = True


def stop():
    global _mission_thread, _started
    if not _started:
        print("[ERROR] Mission hasn't been started")
        return

    _mission_thread.kill()
    _mission_thread.join()
    _started = False


def isStarted():
    global _started
    return _started
