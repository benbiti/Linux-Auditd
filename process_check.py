#!/usr/bin/python


from process_functions import find_process

# Variable assignment of the process name we wish to determine is in state running.

some_process = "rsyslogd"

# Testing to determine if the process identified within the variable process_name is running.

print "The Process", some_process, "is",
if (not find_process(some_process)):
  print "not",
print "in state running."


