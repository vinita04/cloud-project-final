#!/usr/bin/python

import cgi,os,commands
print "Content-Type:text/html"
print ""
x=cgi.FieldStorage()
s_ip='192.168.122.200'

d_name=x.getvalue('storagename')
d_size=x.getvalue('storagesize')
cliaddr=x.getvalue('cliaddr')
f,g=commands.getstatusoutput('sudo lvcreate -V'+d_size+'G --name '+d_name+' --thin redvg/adhoc')
'''if f==0:
	print "done"
else:
	print "wrong"
'''
#now format the file with ext4/xfs
a,b=commands.getstatusoutput('sudo mkfs.ext4 /dev/redvg/'+d_name)
'''if a==0:
	print "done" 
else:
	print "error"
'''
#now create mounting point
commands.getstatusoutput('sudo mkdir /mnt/'+d_name)
# now mounting drive locally
d=commands.getoutput('sudo mount /dev/redvg/'+d_name+' /mnt/'+d_name)
print d
# now time for nfs server configuration
x,y=commands.getstatusoutput('sudo rpm -q nfs-utils')
if x==0:
	print "already installed"
else:
	commands.getstatusoutput('sudo yum install nfs-utils -y')
# making entry in exports file
entry='/mnt/'+d_name+'   '+cliaddr+'(rw,no_root_squash)'
#appending this var to exports file
f=open('/etc/exports','a')
f.write(entry)
f.write('\n')
f.close()
# finally  starting  nfs  service  and service  persistant 
commands.getstatusoutput('sudo systemctl   restart  nfs-server')
commands.getstatusoutput('sudo systemctl   enable  nfs-server')

check,check1=commands.getstatusoutput('sudo exportfs -r')
if check == 0:
	c='mkdir /media/'+d_name+'\n'+'mount '+s_ip+':/mnt/'+d_name+' /media/'+d_name
	commands.getstatusoutput('sudo touch /var/www/html/obbulk.sh')
	commands.getstatusoutput('sudo chmod 777 /var/www/html/obbulk.sh' )
	f=open('/var/www/html/obbulk.sh','w')
	f.write(c)
	f.write('\n')
	f.close() 
	commands.getstatusoutput('sudo tar cvf ../html/obbulk.tar ../html/obbulk.sh')
	commands.getstatusoutput('sudo chmod 555 ../html/obbulk.tar')
	print "<META HTTP-EQUIV='refresh' content='0; url=/obbulk.tar' />"
else:
	print "duplicate entry"
