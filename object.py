#!/usr/bin/python

import cgi,os,commands
print "Content-Type:text/html\r\n\r\n"
print "";
x=cgi.FieldStorage()
data=x.getvalue('ch')

if data=="cans" :
	#print "<a href=/objst.html>"
	#print "click here"
	#print "</a>"
	print "<META HTTP-EQUIV='refresh' content='0; url=/objst.html' />"
elif data=="etes" :
	#print "<META HTTP_EQUIV='refresh' content='0; url=/obextend.html' />"
	print "<META HTTP-EQUIV='refresh' content='0; url=/obextend.html' />"



