import pexpect
import sys
from tabnanny import verbose


access_list = raw_input("Please enter the name of the ACL to be modified: ")

def connect():
    host = raw_input("Please enter the host ip: ")
    user = raw_input("Please enter your username: ")
    password = raw_input("Please enter your password: ")
    child = pexpect.spawn('ssh %s@%s' % (user, host))
    child.timeout = 4
    child.expect('password:')
    child.sendline(password)
    child.expect('#')
    return child

            #child.sendline('configure exclusive')
            #child.expect('\(config)\)#')

def preCheck(child):

    child.sendline('terminal length 0')
    child.expect('#')
    child.sendline('show ipv4 ' + access_list)
    child.expect('#')
    print child.before
    child.sendline('\r\n')
    print("\n\n")
    hardware_direction = raw_input("Please enter the direction of the ACL in hardware: ")
    child.sendline('show access-list ' + access_list + 'hardware '+ hardware_direction + 'location 0/0/CPU0')
    child.expect('#')
    print child.before
    child.sendline('\r\n')



def removeAndReplaceLine(child):
    removeLine = raw_input("Please enter the line you would like to remove and replace: ")
    int(removeLine)
    child.sendline('configure exclusive')
    child.expect('.*#.*')
    child.sendline('ipv4 access-list ' + access_list)
    child.expect('.*#.*')
    child.sendline('no ' + removeLine)
    child.expect('.*#.*')
    child.sendline('100000 deny ipv4 any any log')
    child.expect('.*#.*')
    child.sendline('show conf')
    child.expect('.*#.*')
    print child.before
    forward = raw_input("Do you want to commit: ")
    forward.lower()
    if forward == "yes":
        child.expect('.*#.*')
        child.sendline('commit')
    else:
        child.sendline('abort')
        print("operation aborted")
        sys.exit(0)


def postCheck(child):
    preCheck(child)


def main():
    child = connect()
    preCheck(child)
    removeAndReplaceLine(child)
    postCheck(child)
main()