#!/usr/bin/python2

import os,commands,socket,time

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind(("",8888))
data2=s.recvfrom(10)
choice=data2[0]
if choice=='1':
	data3=s.recvfrom(10)
	d_name1=data3[0]
	data4=s.recvfrom(10)
	d_size1=data4[0]
	os.system('lvextend  --size +'+d_size1+' hoja/'+d_name1)
	os.system('resize2fs /dev/hoja/'+d_name1)
elif choice=='2':
	#data will recv drive name
	data=s.recvfrom(20)
	d_name=data[0]
	#data1 will recv drive size
	data1=s.recvfrom(20)
	d_size=data1[0]
	#cliaddr will store address of client
	cliaddr=data[1][0]
	print d_size
	print d_name
	#creating lvm by the name of client drive
	os.system('lvcreate -V'+d_size+' --name '+d_name+' --thin hoja/vini')

	#now format the file with ext4/xfs
	os.system('mkfs.ext4 /dev/hoja/'+d_name)
	#now create mounting point
	os.system('mkdir /mnt/'+d_name)
	# now mounting drive locally
	os.system('mount /dev/hoja/'+d_name+' /mnt/'+d_name)

	# now time for nfs server configuration
	x=os.system('rpm -q nfs-utils')
	if x==0:
		print "already installed"
	else:
		os.system('yum install nfs-utils -y')

	# making entry in exports file
	entry='/mnt/'+d_name+'   '+cliaddr+'(rw,no_root_squash)'
	#appending this var to exports file

	f=open('/etc/exports','a')
	f.write(entry)
	f.write('\n')
	f.close()
	# finally  starting  nfs  service  and service  persistant 
	#os.system('systemctl   restart  nfs-server')
	#os.system('systemctl   enable  nfs-server')
	check=os.system('exportfs -r')
	if check==0 :
		s.sendto("done",data1[1])
	else :
		print "plz check ur code"
	
