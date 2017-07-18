#!/usr/bin/python

import cgi,os,commands
print "Content-Type:text/html"
print ""
x=cgi.FieldStorage()
s_ip='192.168.122.200'

d_name=x.getvalue('storagename')
d_size=x.getvalue('storagesize')
cliaddr=x.getvalue('cliaddr')
commands.getstatusoutput('sudo lvcreate --name '+d_name+' --size '+d_size+'M nfs')
#now format the file with ext4/xfs
commands.getstatusoutput('sudo mkfs.ext4 /dev/nfs/'+d_name)
#now create mounting point
commands.getstatusoutput('sudo mkdir /mnt/'+d_name)
# now mounting drive locally
commands.getstatusoutput('sudo mount /dev/nfs/'+d_name+' /mnt/'+d_name)
# now time for nfs server configuration
x=commands.getstatusoutput('sudo rpm -q nfs-utils')
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
	commands.getstatusoutput('sudo touch /var/www/html/objst.sh')
	commands.getstatusoutput('sudo chmod 777 /var/www/html/objst.sh' )
	f=open('/var/www/html/objst.sh','w')
	f.write(c)
	f.write('\n')
	f.close() 
	commands.getstatusoutput('sudo tar cvf ../html/objst.tar ../html/objst.sh')
	commands.getstatusoutput('sudo chmod 555 ../html/objst.tar')
	print "<META HTTP-EQUIV='refresh' content='0; url=/objst.tar' />"
else:
	print "duplicate entry"
