import jobqueue
import threading
from multiprocessing import Condition
from threading import Lock
import main_global
import scheduling
import dispatching
import commandline


def main():
    # Initialize lock and condition variables
    main_global.cmd_queue_lock = Lock()
    main_global.cmd_buf_not_empty = Condition()

    jobqueue.create()

    # Create threads
    main_global.scheduling_thread = threading.Thread(target=scheduling.scheduling,
                                                     args=(dispatching.getSchedulingCheck(),))
    main_global.dispatching_thread = threading.Thread(target=dispatching.dispatching, args=[])

    main_global.scheduling_thread.daemon = True
    main_global.scheduling_thread.start()

    main_global.dispatching_thread.daemon = True
    main_global.dispatching_thread.start()
    commandline.commandLineLoop()
    main_global.cmd_buf_not_empty.notify()
    main_global.cmd_queue_lock.release()

    # Main will not continue until threads are complete.
    main_global.scheduling_thread.join()
    main_global.dispatching_thread.join()


main()
