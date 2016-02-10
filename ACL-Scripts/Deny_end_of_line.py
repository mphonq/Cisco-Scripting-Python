import pexpect
import sys
import re
from tabnanny import verbose


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
    child = pexpect.spawn('ssh %s@%s' % (user, host))
    child.timeout = 4
    child.expect('password:')
    child.sendline(password)
    child.expect('#')
    return child
"""


def determineIPVersion(line):
    counter = len(line)
    for i in range(0, counter):
        access_list = line[i]
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

def determineDirection(line):
    counter = len(line)
    for i in range(0, counter):
        access_list = line[i]
        search_ingress = (re.search(r'in', access_list))
        search_egress = (re.search(r'out', access_list))
        if search_egress:
            direction = "egress"
            return direction
        elif search_ingress:
            direction = "ingress"
            return direction
        else:
            print "could not determine direction."
            sys.exit(0)
    """
    for i in range(len(access_list)):
        current_ACL = access_list[i]
        print current_ACL

    child.sendline('terminal length 0')
    child.expect('#')
    child.sendline('show ipv4 ' + access_list)
    child.expect('#')
    print child.before
    child.sendline('\r\n')
    print("\n\n")
    child.sendline('show access-list ' + access_list + 'hardware '+ direction + 'location 0/0/CPU0')
    child.expect('#')
    print child.before
    child.sendline('\r\n')



def removeAndReplaceLine(child, access_list):
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
    commit = raw_input("Do you want to commit: ")
    commit.lower()
    if commit == "yes":
        child.expect('.*#.*')
        child.sendline('commit')
    else:
        child.sendline('abort')
        print("operation aborted")
        sys.exit(0)
    child.sendline('exit\n')

def postCheck(child):
    preCheck(child)

"""


def main():
    line = readFile()
    # child = connect()
    determineIPVersion(line)
    determineDirection(line)
    # removeAndReplaceLine(child, line)
    # postCheck(child)


main()
