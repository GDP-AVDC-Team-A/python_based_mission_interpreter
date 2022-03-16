#!/usr/bin/env python2
import rospy
import sys
import os
from std_srvs.srv import Empty
from droneMsgsROS.srv import openMissionFile
import mission_handler
import mission_loader

def setup():
    # Turn off stdout buffering
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)

    rospy.init_node('executive_api_process')

    mission_name = rospy.get_param('~mission')
    stack_dir = rospy.get_param('~stack_directory')
    drone_id = rospy.get_param('~drone_id')
    mission_configuration_folder = rospy.get_param('~mission_configuration_folder')
  
    mission_path = '%s/%s' % (mission_configuration_folder, mission_name)

    mission_loader.setMission(mission_path)
    mission_loader.start()


def start(arg):
    mission_handler.start()
    return []

def stop(arg):
    mission_handler.stop()
    return []

def selectMissionFile(req):
    if mission_handler.isStarted():
        print("[ERROR] Can't change mission file while mission is running")
        return {'ack': False}
    mission_loader.stop()
    mission_loader.setMission(req.mission_file_path)
    mission_loader.start()
    return {'ack': True}

if __name__=='__main__':
    setup()
    rospy.Service("~start", Empty, start)
    rospy.Service("~stop", Empty, stop)
    rospy.Service("~select_mission_file", openMissionFile, selectMissionFile)
    rospy.spin()
