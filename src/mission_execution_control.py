import rospy
import droneMsgsROS.srv
import droneMsgsROS.msg
import aerostack_msgs.srv
import aerostack_msgs.msg
import yaml

# --------------- Public api functions ------------------ #


def startTask(task, **args):
  stop_info = {'finished': False, 'result': 'ERROR'}
  start_task_srv = rospy.ServiceProxy('start_task', aerostack_msgs.srv.StartTask)
  res = start_task_srv(task=aerostack_msgs.msg.TaskCommand(name=task, parameters=str(args), priority=2))
  if not res.ack:
      print("[ERROR] %s" % res.error_message)
  return res.ack

def executeTask(task, **args):
  stop_info = {'finished': False, 'result': 'ERROR'}
  start_task_srv = rospy.ServiceProxy('start_task', aerostack_msgs.srv.StartTask)
  res = start_task_srv(task=aerostack_msgs.msg.TaskCommand(name=task, parameters=str(args), priority=2))
  if not res.ack:
      print("[ERROR] %s" % res.error_message)

  def taskStoppedCallback(msg):
    if msg.name == task:
      #print(msg.name)
      stop_info['result'] = msg.termination_cause
      stop_info['finished'] = True
  rospy.Subscriber('task_stopped', aerostack_msgs.msg.TaskStopped, taskStoppedCallback)
  while(not stop_info['finished']):
    rospy.Rate(30).sleep()
  return stop_info['finished'], stop_info['result']

def stopTask(task):
  stop_task_srv = rospy.ServiceProxy('stop_task', aerostack_msgs.srv.StopTask)
  res = stop_task_srv(name=task)
  return res.ack

# --------------- Public api functions ------------------ #
def addBelief(belief, multivalued=False):
  addBelief = rospy.ServiceProxy('add_belief', droneMsgsROS.srv.AddBelief)
  res = addBelief(belief_expression=belief, multivalued=multivalued)
  return res.success


def removeBelief(belief):
  removeBelief = rospy.ServiceProxy('remove_belief', droneMsgsROS.srv.RemoveBelief)
  res = removeBelief(belief_expression=belief)
  return res.success


def queryBelief(expression):
  res = _query(expression)
  unification = yaml.load(res.substitutions)
  return (res.success, unification)


def trueBelief(expression):
  res = _query(expression)
  return res.success


def consultPlanner(planner, **args):
  pass


# --------------- Private functions and variables ------------------ #


def _query(expression):
  executeQuery = rospy.ServiceProxy('query_belief', aerostack_msgs.srv.QueryBelief)
  return executeQuery(query=expression)
