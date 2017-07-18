#!/usr/bin/python2

import os,time,string,commands


s_ip="192.168.122.200"



# installing iscsi 
x=os.system('rpm -q iscsi-initiator-utils')
if x==0:
	print "already installed"
else:
	os.system('yum install iscsi-initiator-utils -y')


commands.getstatusoutput('systemctl enable iscsid iscsi')
commands.getstatusoutput('systemctl start iscsid iscsi')
# sending a discover packet to iscsi target server0
s=commands.getoutput('iscsiadm --mode discovery --type sendtargets --portal '+s_ip)
print s
# login to target server with received iqn to access the hdd
if ' ' in s:
	l=s.rsplit(' ',1)[0]
	r=s.rsplit(' ',1)[1]
print l
print r

commands.getstatusoutput('iscsiadm -m node -T '+r+' -l')
#commands.getstatusoutput('')

