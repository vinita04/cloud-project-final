#!/usr/bin/python2

import cgi,cgitb,os,commands
print "Content-Type:text/html\r\n\r\n"
print "";
cgitb.enable()
x=cgi.FieldStorage()
s_ip='192.168.122.200'
#d_name will recv drive name
d_name=x.getvalue('stname')
#d_size will recv drive size
d_size=x.getvalue('stsize')
#creating lvm by the name of client drive
commands.getstatusoutput('sudo lvcreate -V'+d_size+' --name '+d_name+' --thin osy/des')
# now time for scsi server configuration
ch,ch1=commands.getstatusoutput('sudo rpm -q targetcli')
if ch==0:
	print "Already Installed"
else:
	commands.getstatusoutput('sudo yum install targetcli -y')

commands.getstatusoutput('sudo systemctl start target')
commands.getstatusoutput('sudo systemctl enable target')
#os.system('sudo targetcli')
#os.system('sudo targetcli backstores/fileio create testfile /tmp/fileio 500M write_back=false')
commands.getstatusoutput('sudo targetcli backstores/block create name='+d_name+' dev=/dev/osy/'+d_name)
commands.getstatusoutput('sudo targetcli iscsi/ create iqn.2016-01.com.example:'+d_name)
commands.getstatusoutput('sudo targetcli iscsi/iqn.2016-01.com.example:'+d_name+'/tpg1/')
#os.system('sudo targetcli iscsi/iqn.2016-01.com.example:target/tpg1/luns/ create /backstores/fileio/testfile')
commands.getstatusoutput('sudo targetcli iscsi/iqn.2016-01.com.example:'+d_name+'/tpg1/luns/ create /backstores/block/'+d_name)
#os.system('sudo cat /etc/iscsi/initiatorname.iscsi')
commands.getstatusoutput('sudo targetcli iscsi/iqn.2016-01.com.example:'+d_name+'/tpg1/acls/')
commands.getstatusoutput('sudo targetcli iscsi/iqn.2016-01.com.example:'+d_name+'/tpg1/acls/ create iqn.1994-05.com.redhat:f889f2723f48')
commands.getstatusoutput('sudo targetcli iscsi/iqn.2016-01.com.example:'+d_name+'/ exit')
commands.getstatusoutput('sudo netstat -antup | grep 3260')
#commands.getstatusoutput('sudo systemctl start firewalld')
#commands.getstatusoutput('sudo firewall-cmd --permanent --add-port=3260/tcp')
#commands.getstatusoutput('sudo firewall-cmd --reload')

entry='chmod 666 /etc/iscsi/initiatorname.iscsi\necho InitiatorName=iqn.1994-05.com.redhat:f889f2723f48 > /etc/iscsi/iniinitiatorname.iscsi\nsystemctl start start iscsid iscsi\niscsiadm --mode discovery --type sendtargets --portal 192.168.122.200\niscsiadm -m node -T iqn.2016-01.com.example:'+d_name+' -l'
commands.getstatusoutput('sudo touch /var/www/html/block.sh')
commands.getstatusoutput('sudo chmod 777 /var/www/html/block.sh')
f=open('/var/www/html/block.sh','w')
f.write(entry)
f.write('\n')
f.close()
commands.getstatusoutput('sudo tar -cvf ../html/block.tar ../html/block.sh')
commands.getstatusoutput('sudo chmod 555 ../html/block.tar')
print "<META HTTP-EQUIV='refresh' content='0; url=/block.tar' />"

