import jobqueue_global
from jobqueue_global import Job, Node
import main_global
from threading import Lock
import datetime

numJobs = 0
schedulingType = 1
totalJobs = 0
totalTurnTime = 0
totalExecTime = 0
totalWaitTime = 0
throughput = 0
schedulingTypeString = "FCFS"
head = None
current = None


def getTotalJobs():
    global totalJobs
    return totalJobs


def getTotalTurnTime():
    global totalTurnTime
    return totalTurnTime


def getTotalExecTime():
    global totalExecTime
    return totalExecTime


def getTotalWaitTime():
    global totalWaitTime
    return totalWaitTime


def getThroughput():
    global throughput
    return throughput


def create():
    jobqueue_global.cmd_job_lock = Lock()
    main_global.cmd_queue_lock.acquire()


def peek():
    global head
    return head


def pointerSet(newNode):
    global head
    global current

    if head == None:
        return

    current = head

    if schedulingType == 1:
        # FCFS
        while current.next is not None and current.data.queue_time < newNode.data.queue_time:
            current = current.next
    else:
        while current.next is not None:
            current = current.next


def enqueue(newNode):
    global head
    global current
    global numJobs
    global totalJobs

    if head is None or current is None:
        head = newNode
        numJobs += 1
        totalJobs += 1
        return 0

    nodeWasSet = 0  # Keep track of weather node was enqued correctly
    if schedulingType == 1:
        # FCFS
        current.next = newNode
        nodeWasSet = 1
    elif schedulingType == 2 and newNode.data.executionTime < current.data.executionTime:
        # SJF
        newNode.next = current
        nodeWasSet = 1
    elif schedulingType == 3 and newNode.data.priority < current.data.priority:
        newNode.next = current
        nodeWasSet = 1

    if nodeWasSet == 0:
        if current.next is None:
            current.next = newNode
        else:
            newNode.next = current.next
            current.next = newNode

    numJobs += 1
    totalJobs += 1
    return 0


def getWaitTime(newNode):
    global current
    waitTime = 0
    current = head
    while current is not None and current is not newNode:
        waitTime += current.data.execution_time
        current = current.next

    return waitTime


# Remove job and associated node from queue
def dequeue():
    global head
    old = head
    if old.next is None:
        head = None
    else:
        head = head.next

    global numJobs
    numJobs -= 1
    return old


def newJob(jobName, jobExecTime, jobPriority):
    # Create new job
    newJ = Job(jobName, jobExecTime, jobPriority, datetime.datetime.now(), 0)

    # Aquire time added to queue (used for FCFS algorithm)
    global totalExecTime
    totalExecTime = totalExecTime + jobExecTime

    # Create node for job
    newNode = Node(newJ, None)
    pointerSet(newNode)
    jobqueue_global.cmd_job_lock.acquire()
    enqueue(newNode)
    jobqueue_global.cmd_job_lock.release()

    if numJobs == 1:
        # main_global.cmd_buf_not_empty.notify()
        main_global.cmd_queue_lock.release()

    waitTime = 0
    if numJobs > 1 and newNode is not None:
        waitTime = getWaitTime(newNode)
        global totalWaitTime
        totalWaitTime = waitTime

    print(
        "\nJob {} was submitted.\nTotal number of jobs in the queue: {}\nExpected waiting time: {}\nScheduling Policy: {}\n\n".format(
            jobName, numJobs, waitTime, schedulingTypeString))
    return 0


def removeJob():
    _ = dequeue()


def _list():
    print("Total number of jobs in the queue: {}\n".format(numJobs))
    print("Scheduling Policy: {}\n".format(schedulingTypeString))
    global head
    if head == None:
        print(
            "\nThe job queue is currently empty. The 'run' command allows you to add new job.\nType 'help' for more information.\n")
        return

    print("Name\t\tCPU_Time\t\tPriority\tArrival_time")
    global current
    current = head

    while current is not None:
        currentJob = current.data
        jobTime = currentJob.queue_time
        jobProgress = " "
        if current.data.progress == 1:
            jobProgress = "Run"

        print("\n{}\t\t{}\t\t\t{}\t\t{}:{}:{}\n".format(currentJob.name, currentJob.execution_time, currentJob.priority,
                                                        jobTime.hour, jobTime.minute, jobTime.second))

        current = current.next


def getNumJobs():
    global numJobs
    return numJobs


def sort(thisNode):
    for i in range(numJobs):
        for j in range(i + 1, numJobs):
            if schedulingType == 1:
                if thisNode[i].data.queue_time > thisNode[j].data.queue_time and thisNode[i].data.progress != 1:
                    temp = thisNode[i]
                    thisNode[i] = thisNode[j]
                    thisNode[j] = temp
            elif schedulingType == 2:
                if thisNode[i].data.execution_time > thisNode[j].data.execution_time and thisNode[i].data.progress != 1:
                    temp = thisNode[i]
                    thisNode[i] = thisNode[j]
                    thisNode[j] = temp
            elif schedulingType == 3:
                if thisNode[i].data.priority > thisNode[j].data.priority and thisNode[i].data.progress != 1:
                    temp = thisNode[i]
                    thisNode[i] = thisNode[j]
                    thisNode[j] = temp


# Get and set scheduling type
def setSchedulingType(newSchedulingType):
    global schedulingType
    global schedulingTypeString
    temp = schedulingType
    schedulingType = newSchedulingType
    if schedulingType == 1:
        schedulingTypeString = "FCFS"
    elif schedulingType == 2:
        schedulingTypeString = "SJF"
    elif schedulingType == 3:
        schedulingTypeString = "Priority"


def getSchedulingType():
    return schedulingType


# Change the scheduling policy
def changeType(newType):
    if schedulingType == newType:
        msg = ""
        if numJobs == 1:
            msg = "{} job has been rescheduled.".format(numJobs)
        else:
            msg = "{} jobs has been rescheduled.".format(numJobs)
        print("Scheduling policy already set to {}. " + msg + "\n".format(schedulingTypeString))
        return 1
    setSchedulingType(newType)
    # main_global.cmd_queue_lock.release()
    main_global.cmd_queue_lock.acquire()
    changeOrder()
    main_global.cmd_queue_lock.release()
    print("Scheduling policy has been switched to {}. All the {} waiting jobs have been rescheduled.\n".format(
        schedulingTypeString, numJobs))
    return 0


# Reorder nodes when type is changed
def changeOrder():
    if numJobs >= 1:
        global current
        global head

        thisNode = []
        for i in range(0, numJobs):
            thisNode.append(i)
        current = head

        for i in range(numJobs):
            thisNode[i] = current
            current = current.next

        sort(thisNode)
        head = thisNode[0]
        current = head

        for i in range(numJobs):
            current.next = thisNode[i]
            current = current.next

        current.next = None
    else:
        print("Scheduling policy set to {}. No jobs have been rescheduled.\n".format(schedulingTypeString))
