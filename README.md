# Brief

This package is a process for interpreting a mission plan. The operator can specify a mission in PML language (Python-based Mission specification Language) and this process interprets such a specification, generating the appropriate orders for the rest of processes in Aerostack to carry out the mission.

# Services

- **~select_mission_file** ([droneMsgsROS/openMissionFile](https://bitbucket.org/joselusl/dronemsgsros/src/master/srv/openMissionFile.srv))  
Load a mission file written in PML.


# Subscribed Topics

- **behavior_event** ([aerostack_msgs/BehaviorEvent](https://bitbucket.org/visionaerialrobotics/aerostack_msgs/src/master/msg/BehaviorEvent.msg))  
Notification that a behavior has ended.


# Configuration Files

- **mission.py**  
The mission specification is written in a Python file, called mission.py, using the PML language.

---

# Process Development

**Maintainer:** Alberto Camporredondo ([alberto.camporredondo@gmail.com](mailto:alberto.camporredondo@gmail.com))

**Contributors:**

- Guillermo De Fermin ([gdefermin@gmail.com](mailto:gdefermin@gmail.com))
