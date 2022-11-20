from threading import Lock

cmd_job_lock = None


class Job():
    def __init__(self, name, execution_time, priority, queue_time, progress):
        self.name = name
        self.execution_time = execution_time
        self.priority = priority
        self.queue_time = queue_time
        self.progress = progress


class Node():
    def __init__(self, data, next):
        self.data = data
        self.next = next
