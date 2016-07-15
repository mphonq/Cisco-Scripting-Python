import paramiko
import sys


class Connect(object):
    username = 'ccie'
    password = 'ccie'
    def __init__(self, ip, username, pwd):
        self.ip = ip
        self.username = username
        self.pwd = pwd

    def connect_to_device(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect('192.168.178.152', username = self.username, password = self.password)

    def sendCommands(self,cmd):
        (iin,out,err) = self.ssh.exec_command(cmd)
        if out:
            for line in out.readlines():
                    print line
        else:
                print "GoodBye"
                self.ssh.close()

def main(cmd):
        device = Connect.Connect
        device.connect_to_device()
        device.rundevicecmd(cmd)

cmd= sys.argv[1]
if _name_==_main_
    main(cmd)