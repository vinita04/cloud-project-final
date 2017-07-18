#!/usr/bin/python2

import os,time,socket

s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s_ip="192.168.122.97"
s_port=9999

drive_name=raw_input("enter name of drive : ")
drive_size=raw_input("enter size in MB : ")

s.sendto(drive_name,(s_ip,s_port))
s.sendto(drive_size,(s_ip,s_port))

res=s.recvfrom(4)
if res[0]=="done":
	os.system('mkdir /media/'+drive_name)
	os.system('mount '+s_ip+':/mnt/'+drive_name+' /media/'+drive_name)	
else :
	print "no response from storage cloud"
