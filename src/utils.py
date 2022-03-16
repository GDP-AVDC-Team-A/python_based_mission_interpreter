import sys
import trace
import threading


# Source: https://mail.python.org/pipermail/python-list/2004-May/281944.html
#
# This code module allows you to kill threads.  The
# class KThread is a drop-in replacement for
# threading.Thread.  It adds the kill() method, which
# should stop most threads in their tracks.

# ---------------------------------------------------------------------
# KThread: A killable Thread implementation.
# ---------------------------------------------------------------------
class KThread(threading.Thread):
  """A subclass of threading.Thread, with a kill() method."""
  def __init__(self, *args, **keywords):
    threading.Thread.__init__(self, *args, **keywords)
    self.killed = False

  def start(self):
    """Start the thread."""
    self.__run_backup = self.run
    self.run = self.__run      # Force the Thread to install our trace.
    threading.Thread.start(self)

  def __run(self):
    """Hacked run function, which installs the trace."""
    sys.settrace(self.globaltrace)
    self.__run_backup()
    self.run = self.__run_backup

  def globaltrace(self, frame, why, arg):
    if why == 'call':
      return self.localtrace
    else:
      return None

  def localtrace(self, frame, why, arg):
    if self.killed:
      if why == 'line':
        raise SystemExit()
    return self.localtrace

  def kill(self):
    self.killed = True


color = {
  'red': '\e[31m',
  'green': '\e[32m',
  'yellow': '\e[33m',
  'blue': '\e[34m',
  'reset': '\e[0m',
}
