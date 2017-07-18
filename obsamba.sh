mkdir /mnt/vkl
systemctl start smb
mount -o username=vai //192.168.122.200/vkl /mnt/vkl
