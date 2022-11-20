from enum import Enum

isRunning = 1

cmd_queue_lock = None
cmd_buf_not_empty = None
scheduling_thread = None
dispatching_thread = None


class Check(Enum):
    YES = 0
    NO = 1


# Getter and setter to determine if program is running

def getRunning():
    global isRunning
    return isRunning


def setRunning(newIsRunning):
    global isRunning
    isRunning = newIsRunning
