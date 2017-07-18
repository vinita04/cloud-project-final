#!/usr/bin/python2

import cgi,os,cgitb,commands

print "Content-Type: text/html\r\n\r\n"
print "";
cgitb.enable()
x=cgi.FieldStorage()
s_ip='192.168.122.200'
#d_name will recv drive name
d_name=x.getvalue('storagename')
#d_size will recv drive size
d_size=x.getvalue('storagesize')
# u_name will recv user name of samba server
u_name=x.getvalue('smbuser')
# cliaddr will recv client address
cliaddr=x.getvalue('cliaddr')

#creating lvm by the name of client drive
commands.getstatusoutput('sudo  lvcreate -V'+d_size+' --name '+d_name+'  --thin drive/nw')
#now format the file with ext4/xfs
commands.getstatusoutput('sudo mkfs.ext4 /dev/drive/'+d_name)
#now create mounting point
commands.getstatusoutput('sudo mkdir /mnt/'+d_name)
# now mounting drive locally
commands.getstatusoutput('sudo mount /dev/drive/'+d_name+' /mnt/'+d_name)
commands.getstatusoutput('sudo chmod 777 /mnt/'+d_name)
# now time for samba server configuration
'''x=commands.getstatusoutput('sudo rpm -q samba')
if x==0:
	print "already installed"
else:
	commands.getstatusoutput('sudo yum install samba* -y')'''
#commands.getstatusoutput('sudo useradd -s /sbin/nologin '+u_name)
#assigning passwd to samba user
#commands.getstatusoutput('(echo 123; echo 123 )|sudo smbpasswd -a '+u_name)
# making entry in exports file
entry='['+d_name+']'+ "\n"+'path=/mnt/'+d_name+"\n"+'writable=yes'+"\n"+'hosts allow='+cliaddr+'\nvalid users='+u_name+' create mask = 775 directory mask = 775'


#appending this var to exports file
f=open('/etc/samba/smb.conf','a')
f.write(entry)
f.write('\n')
f.close()
check,check1=commands.getstatusoutput('sudo systemctl restart smb')
if check == 0:
	c='mkdir /mnt/'+d_name+'\n'+'systemctl start smb'+'\n'+'mount -o username='+u_name+' //'+s_ip+'/'+d_name+' /mnt/'+d_name
	commands.getstatusoutput('sudo touch /var/www/html/obsamba.sh')
	commands.getstatusoutput('sudo chmod 777 /var/www/html/obsamba.sh' )
	f=open('/var/www/html/obsamba.sh','w')
	f.write(c)
	f.write('\n')
	f.close() 
	commands.getstatusoutput('sudo tar cvf ../html/obsamba.tar ../html/obsamba.sh')
	commands.getstatusoutput('sudo chmod 555 ../html/obsamba.tar')
	print "<META HTTP-EQUIV='refresh' content='0; url=/obsamba.tar' />"

else :
	print "error"
