#!/usr/bin/python

import cgi,os,commands
print "Content-Type:text/html"
print ""
x=cgi.FieldStorage()
s_ip='192.168.122.200'

d_name=x.getvalue('storagename')
d_size=x.getvalue('storagesize')

commands.getstatusoutput('sudo lvextend --size +'+d_size+'M /dev/nfs/'+d_name)
#now format the file with ext4/xfs
c,c1=commands.getstatusoutput('sudo resize2fs /dev/nfs/'+d_name)
if c==0:
	print "done"

