import rospy
import droneMsgsROS.srv
import droneMsgsROS.msg
import aerostack_msgs.srv
import aerostack_msgs.msg
import yaml

# --------------- Public api functions ------------------ #

def executeBehavior(behavior, **args):
  global _event_type

  event_info = {'finished': False, 'result': 'ERROR'}

  uid = 0
  def behaviorEventCallback(msg):
    print(msg.name)
    if msg.name == behavior:
      event_info['result'] = msg.termination_cause
      event_info['finished'] = True

  rospy.Subscriber('behavior_activation_finished', aerostack_msgs.msg.BehaviorActivationFinished, behaviorEventCallback)
  # The subscription to the topic "behavior_activation_finished" must be  active between consecutive calls to the function
  # executeBehavior() to avoid losing messages in this topic. It is important not to un-subscribe the topic 
  # behavior_activation_finished (for example using the function unregister()).

  # Activating a sequential behavior is the same as activating a parallel one, except we wait for the behavior to finish
  ack, uid = activateBehavior(behavior, **args)
 
  if ack:
    while(not event_info['finished']):
      rospy.Rate(10).sleep()

  return event_info['result']


def activateBehavior(behavior, **args):
  activateBehaviorSrv = rospy.ServiceProxy('request_behavior_activation', aerostack_msgs.srv.RequestBehaviorActivation)
  res = activateBehaviorSrv(behavior=aerostack_msgs.msg.BehaviorCommandPriority(name=behavior, arguments=str(args), priority=2))
  if not res.ack:
      print("[ERROR] %s" % res.error_message)
  return res.ack, res.uid


def deactivateBehavior(behavior_uid,name):
  cancelBehavior = rospy.ServiceProxy('request_behavior_deactivation', aerostack_msgs.srv.RequestBehaviorDeactivation)
  res = cancelBehavior(behavior_uid=behavior_uid,name=name)
  return res.ack


def isActiveBehavior(behavior):
  pass


def assertBelief(belief, multivalued=False):
  addBelief = rospy.ServiceProxy('add_belief', droneMsgsROS.srv.AddBelief)
  res = addBelief(belief_expression=belief, multivalued=multivalued)
  return res.success


def retractBelief(belief):
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
