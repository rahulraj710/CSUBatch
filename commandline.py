import commandline_global
import main_global
import os
import jobqueue

# Help table
helpmenu = [
    "run <job> <time> <pri>: Submit a job named <job>,\n\t\t\texecution time is <time>\n\t\t\tpriority is <pri>.",
    "list: display the job status.",
    "fcfs: change the scheduling policy to FCFS.",
    "sjf: change the scheduling policy to SJF.",
    "priority: change the scheduling policy to priority.",
    "quit: exit CSUBatch",
    None
]


# Run
def cmd_run(nargs, args):
    if nargs < 2:
        print("Invalid command. Enter 'run <job> <time> <priority>\n\n")
        return commandline_global.EINVAL
    jobName = args[1]
    # If job exists, add it too queue.
    if os.path.exists(jobName):
        executionTime = commandline_global.DEFAULTEXECTIME
        priority = commandline_global.DEFAULTPRIORITY

        # See if there is a defined burst time.
        if len(args) >= 3:
            if int(args[2]) != 0:
                executionTime = int(args[2])

        # See if there is a defined priority.
        if len(args) >= 4:
            if args[3] != 0:
                priority = int(args[3])

        jobqueue.newJob(jobName, executionTime, priority)

    else:
        print("The job was not found. Please ensure that it is the same directory as CSUBatch.\n")

    return 0


# Menu
def showmenu(menu):
    i = 0
    while menu[i]:
        print(menu[i])
        i += 1
    print("\n")


def cmd_helpmenu(n, a):
    showmenu(helpmenu)
    return 0


# Quit
def cmd_quit(nargs, args):
    print("Total number of jobs submitted: {}".format(jobqueue.getTotalJobs()))
    print("Total waiting time: {}".format(jobqueue.getTotalWaitTime()))
    print("Total execution time {}".format(jobqueue.getTotalExecTime()))
    print("Thank you for using CSUBatch.\n")

    exit(0)


# List
def cmd_list(n, a):
    jobqueue._list()
    return 0


def cmd_fcfs(n, a):
    jobqueue.changeType(1)
    return 0


def cmd_sjf(n, a):
    jobqueue.changeType(2)
    return 0


def cmd_priority(n, a):
    jobqueue.changeType(3)
    return 0


#  Command table
cmdTable = [
    ["?\n", cmd_helpmenu],
    ["h\n", cmd_helpmenu],
    ["help\n", cmd_helpmenu],
    ["run", cmd_run],
    ["run\n", cmd_run],
    ["list\n", cmd_list],
    ["list", cmd_list],
    ["fcfs\n", cmd_fcfs],
    ["sjf\n", cmd_sjf],
    ["priority\n", cmd_priority],
    ["q\n", cmd_quit],
    ["quit\n", cmd_quit],
    ["exit\n", cmd_quit],
    [None, None]
]


# Process a single command

# Process a single command
def cmd_dispatch(cmd):
    cmd = cmd.strip()
    args = None
    nargs = 0
    word = None
    context = None
    i = None
    result = None

    if len(cmd) == 0:
        return 0

    args = cmd.split(" ")
    nargs = len(args)

    if nargs == 0:
        return 0

    if nargs >= commandline_global.MAXMENUARGS:
        print("Command line has too many words.\n")
        return commandline_global.E2BIG

    i = 0
    while cmdTable[i][0] is not None:
        if cmdTable[i][0] and (args[0] == cmdTable[i][0].strip()):
            # Call function throught the cmd_table
            result = cmdTable[i][1](nargs, args)
            return result
        i += 1

    print("{arg0}: Command not found. Use 'help' command for a list of commands.\n".format(arg0=args[0]))
    return commandline_global.EINVAL


def commandLineLoop():
    i = 0
    print("Welcome to CSUBatch.\n")

    # Main loop
    while True:
        print("Please enter your command. Type 'help' for a list of commands.\n")
        buffer = input(">>> ")
        cmd_dispatch(buffer)

    return 0
