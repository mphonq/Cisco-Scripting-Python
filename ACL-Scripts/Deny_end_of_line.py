import pexpect
import sys
import re
import time
from tabnanny import verbose

#This is an option to read from a file if you don't want to enter the ACL's individually
#This option is not really advised as you have less control over the actions of the script
"""
def readFile():
    try:
        aclList = open("acl.txt", 'r').read().split()

    except IOError as e:
        print "I/O error({0}): {1}".format(e.errno, e.strerror)

    return aclList

"""

def connect():
    host = raw_input("Please enter the host ip: ")
    user = raw_input("Please enter your username: ")
    password = raw_input("Please enter your password: ")
    child = pexpect.spawn('telnet ' + host)
    fout = file('mylog.txt','w')
    child.logfile = fout
    child.expect('Username: ')
    child.sendline(user)
    child.expect('Password: ')
    child.sendline(password)
    child.timeout = 4
    child.expect('#')
    return child


def determineIPVersion(access_list):
        search_ipv4 = (re.search(r'v4', access_list))
        search_ipv6 = (re.search(r'v6', access_list))
        if search_ipv4:
            ip_ver = "v4"
            return ip_ver
        elif search_ipv6:
            ip_ver = "v6"
            return ip_ver
        else:
            print "Could not detect ip version."
            sys.exit(0)

def determineDirection(access_list):
        search_ingress = (re.search(r'in', access_list))
        search_egress = (re.search(r'out', access_list))
        if search_egress:
            direction = "egress"
            return direction
        elif search_ingress:
            direction = "ingress"
            return direction
        else:
            print "Could not determine hardware direction."
            sys.exit(0)

def preCheck(child, access_list, ip_ver, direction):
    if ip_ver == 'v4':
        child.sendline('terminal length 0')
        child.expect('#')
        child.sendline('show access-lists ipv4 ' + access_list)
        child.expect('#')
        print child.before
        child.sendline('\r\n')
        print("\n\n")
        child.sendline('show access-list ' + access_list + 'hardware '+ direction + 'location 0/0/CPU0')
        child.expect('#')
        print child.before
        child.sendline('\r\n')
    elif ip_ver == 'v6':
        child.sendline('terminal length 0')
        child.expect('#')
        child.sendline('show access-lists ipv6 ' + access_list)
        child.expect('#')
        print child.before
        child.sendline('\r\n')
        print("\n\n")
        child.sendline('show access-list ipv6' + access_list + 'hardware '+ direction + 'location 0/0/CPU0')
        child.expect('#')
        print child.before
        child.sendline('\r\n')



def removeAndReplaceLine(child, access_list, ip_ver):
    removeLine = raw_input("Please enter the line you would like to remove and replace: ")
    int(removeLine)
    child.sendline('configure exclusive')
    child.expect('.*#.*')
    if ip_ver == 'v4':
        child.sendline('ipv4 access-list ' + access_list)
        child.expect('.*#.*')
        child.sendline('no ' + removeLine)
        child.expect('.*#.*')
        child.sendline('100000 deny ipv4 any any log')
        child.expect('.*#.*')
        print "This is a confirmation of the line you would like to remove and replace.\n"
        child.sendline('show conf')
        child.expect('.*#.*')
        time.sleep(4)
        child.expect('.*#.*')
        print child.after
        commit = raw_input("Do you want to commit: ")
        commit.lower()
        if commit == "yes":
            child.sendline('commit')
            child.expect('.*#.*')
            child.sendline('exit')
            child.expect('.*#.*')
            child.sendline('exit')
        else:
            child.sendline('abort')
            print("operation aborted")
            sys.exit(0)
    elif ip_ver == 'v6':
        child.sendline('ipv6 access-list ' + access_list)
        child.expect('.*#.*')
        child.sendline('no ' + removeLine)
        child.expect('.*#.*')
        child.sendline('100000 deny ipv6 any any log')
        child.expect('.*#.*')
        print "This is a confirmation of the line you would like to remove and replace.\n"
        child.sendline('show conf')
        child.expect('.*#.*')
        time.sleep(4)
        child.expect('.*#.*')
        print child.after
        ipv6Commit = raw_input("Do you want to commit: ")
        ipv6Commit.lower()
        if ipv6Commit == "yes":
            child.sendline('commit')
            child.expect('.*#.*')
            child.sendline('exit')
            child.expect('.*#.*')
            child.sendline('exit')

        else:
            child.sendline('abort')
            print("operation aborted")
            sys.exit(0)

def main():
    line = raw_input("Please enter the acl you would like to edit: ")
    child = connect()
    ip_ver = determineIPVersion(line)
    direction = determineDirection(line)
    preCheck(child, line, ip_ver, direction)
    removeAndReplaceLine(child, line, ip_ver)
    preCheck(child, line, ip_ver, direction)
    more = raw_input("do you have another acl you would like to edit: ")
    more.lower()
    if more == "yes":
        main()
    else:
        sys.exit("Bye!")

main()
