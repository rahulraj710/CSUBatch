from jobqueue import peek
import dispatching_global
import main_global
import jobqueue
import jobqueue_global
from main_global import Check, getRunning
import os

from scheduling import scheduling

isDispatching = None


# Check if program is scheduling
def getSchedulingCheck():
    dispatching_global.schedulingCheck = 0  # NO
    return dispatching_global.schedulingCheck


def setIsDispatching(newIsDispatching):
    global isDispatching
    isDispatching = newIsDispatching


def getIsDispatching():
    global isDispatching
    return isDispatching


def dispatching():
    pid = None
    while getRunning() == 1 or jobqueue.peek() is not None:
        main_global.cmd_buf_not_empty.acquire()
        main_global.cmd_queue_lock.acquire()
        if dispatching_global.schedulingCheck == 1:
            runCheck = None
            my_args = []

            my_args.append(peek().data.executionTime)

            pid = os.fork()
            if pid == -1:
                print("Fork Error!")
            elif pid == 0:
                os.execv(peek().data.name, my_args)
                print("Error with execv(). Exiting.")
                exit()
            else:
                while os.WNOHANG(os.waitpid(pid, runCheck))[1] == 0:
                    continue
                jobqueue_global.cmd_job_lock.acquire()
                jobqueue.removeJob()
                jobqueue_global.cmd_job_lock.release()

            dispatching_global.schedulingCheck = 0

        # next line here
        main_global.cmd_buf_not_empty.notify()
        main_global.cmd_queue_lock.release()
