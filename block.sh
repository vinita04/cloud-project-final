chmod 666 /etc/iscsi/initiatorname.iscsi
echo InitiatorName=iqn.1994-05.com.redhat:f889f2723f48 > /etc/iscsi/iniinitiatorname.iscsi
systemctl start start iscsid iscsi
iscsiadm --mode discovery --type sendtargets --portal 192.168.122.200
iscsiadm -m node -T iqn.2016-01.com.example:vishu -l
