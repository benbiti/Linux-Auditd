#!/usr/bin/python

import os, subprocess, re

# Find the process we wish to determine is in state running.

def find_process(process_name):
  ps = subprocess.Popen("ps -ef | grep " +process_name+ " | grep -v grep", shell=True, stdout=subprocess.PIPE)
  output = ps.stdout.read()
  ps.stdout.close()
  ps.wait()
  return process_name in output
