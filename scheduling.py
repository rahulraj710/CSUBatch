import main_global
import jobqueue_global
import jobqueue


def scheduling(isScheduling):
    # Run while the program is considered "running" and there are jobs to schedule.
    while main_global.getRunning() == 1 or jobqueue.peek() is not None:
        main_global.cmd_buf_not_empty.acquire()
        main_global.cmd_queue_lock.acquire()
        newIsScheduling = isScheduling

        head = jobqueue.peek()  # get job from job queue head
        if head is not None:
            if head.data is not None:
                if head.data.progress != 0:
                    jobqueue_global.cmd_job_lock.acquire()
                    head.data.progress = 1  # YES #job is considered running
                    newIsScheduling = 1
                    jobqueue_global.cmd_job_lock.release()

        main_global.cmd_buf_not_empty.notify()
        main_global.cmd_queue_lock.release()  # unlock queue
    return None
