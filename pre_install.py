#!/usr/bin/python
# Justin Jessup
# 11/23/2011 
# Linux Audit Plan Rsyslog Configuration Tivioli Pre-installation Script


# Establish the date and time the script was installed on. 

import datetime 

now = datetime.datetime.now()
print
print ("Script was installed on:")
print now.strftime("%Y-%m-%d %H:%M")
print

# Determine if RHEL 5 or RHEL 6 is installed and procede with the appropriate rsyslog configuration
# If RHEL 5 is installed then run through the necessary preinstallation configuration changes
# If RHEL 6 is installed - rsyslog is installed by default - so no action is necessary other than 
# deployment of the appropriate esat-rsyslog.conf file

import os

# Open redhat-release file for evaluation to determine if the Host Operating System is either RHEL 6/5/4

f1 = open("/etc/redhat-release", "r")
t1 = f1.read()
f1.close()

# RHEL 6 Rsyslog Re-Configuration Procedures

if ("6" in t1):
	print("Host Operating System is RHEL 6")
	a1 = os.system("rpm -q rsyslog")
	if (a1 == 0):
		print("Confirmed rsyslog is installed")
	else:
		print("Warning rsyslog is not installed please install rsyslog!")
		print("Installing the rsyslog rpm")
		os.system("/bin/rpm -Uvh rsyslog*rpm")
		print("Restarting the rsyslog daemon")
		os.system("/sbin/service rsyslog restart")
		print("Verify status of rsyslogd daemon")
		service_status = os.system("sudo /sbin/service rsyslog status")
		if (service_status == 0):
			print("Verified the rsyslog daemon is in state running")
		else:
			print("rsyslog daemon is NOT running - we will attempt to restart the daemon again")
			os.system("/sbin/service rsyslog restart")
			print("Revaluating to determine that the rsyslog daemon is in state - running")
			check_status_again = os.system("sudo /sbin/service rsyslog status")
			if (check_status_again == 0):
				print("rsyslog daemon - confirmed status - running")
			else:
				print("We were unable to verify that the rsyslog daemon is in state running!")
				print("Please have your Systems Administrator troubleshoot the issues.")
				print("Review the logs at $PATH /var/log/messages to determine root cause of why the rsyslog daemon did not start.")


# RHEL 5 Rsyslog Re-Configuration Procedures

elif ("5" in t1):
	print("Host Operating System is RHEL 5")
	print
	a2 = os.system("rpm -q rsyslog")
	print
	if (a2 == 0):
		print("Confirmed rsyslog is installed")
		print
		print("Backing up the rsyslog.conf file - backup @ /etc/rsyslog.conf.bak")
		os.system("cp /etc/rsyslog.conf /etc/rsyslog.conf.bak; la -al /etc/rsyslog.conf.bak")
		print
		print("We will now install the ESAT rsyslog.conf configuration file")
		os.system("cp esat-rsyslog.conf /etc/rsyslog.conf")
		print
		print("We will not backup audit.rule - backup @ /etc/audit/audit.rules.bak")
		os.system("cp /etc/audit/audit.rules /etc/audit/audit.rules.bak; ls -la /etc/audit/audit.rules.bak")
		print
		print("We will now install the ESAT audit.rules file which meets the IRS Linux Audit Plan Requirements")
		os.system("cp esat-audit.rules /etc/audit/audit.rules")
		f2 = open("/etc/sysconfig/selinux")
		t2 = f2.read()
		if ("enforcing" in t2):
			print("Selinux is enabled on this system we must adjust Selinux enforcement - to allow rsyslog and auditd to function")
			print("Installing the rsyslog rpm")
			os.system("/bin/rpm -Uvh rsyslog*rpm")
			print("Adjusting Selinux context for rsyslogd")
			os.system("/usr/sbin/semanage fcontext -a -t syslogd_exec_t /sbin/rsyslogd")
			print("Adjusting Selinux for klogd")
			os.system("/usr/sbin/semanage fcontext -a -t klogd_exec_t /sbin/rklogd")
			print("Restore selinux context rsyslogd and rklogd")
			os.system("/sbin/restorecon /sbin/rsyslogd /sbin/rklogd")
			print("Restart the rsyslogd daemon to apply Selinux context changes")
			os.system("/sbin/service rsyslog restart")
			print("Verify status of rsyslogd daemon")
			service_status = os.system("sudo /sbin/service rsyslog status")
			if (service_status == 0):
				print("True")
			else:
				print("False")
				
			
		else:
			print("Selinux is NOT enabled on this system")	
			print("Installing the rsyslog rpm")
			os.system("/bin/rpm -Uvh rsyslog*rpm")
			print("Restart the rsyslogd daemon to apply Selinux context changes")
			os.system("/sbin/service rsyslog restart")
			print("Verify status of rsyslogd daemon")
			service_status = os.system("sudo /sbin/service rsyslog status")
			if (service_status == 0):
				print("rsyslog daemon confirmed status - running")
			else:
				print("rsyslog daemon is NOT running - we will attempt to restart the daemon again")
				os.system("/sbin/service rsyslog restart")
				print("Revaluating to determine that the rsyslog daemon is in state - running")
				check_status_again = os.system("sudo /sbin/service rsyslog status")
				if (check_status_again == 0):
					print("rsyslog daemon confirmed status - running")
				else:
					print("We were unable to verify that the rsyslog daemon is in state running!")
					print("Please have your Systems Administrator troubleshoot the issues.")
					print("Review the logs at $PATH /var/log/messages")

