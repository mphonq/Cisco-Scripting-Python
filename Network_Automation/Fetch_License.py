#coding=utf-8

import pexpect
import sys
import os
from threading import Thread



def connectToDevice(host): 

    try:
        username = raw_input("Please enter your username: ")
        #host = raw_input("Please enter the host ip or hostname: ") 
        child = pexpect.spawn("ssh " + username +"@"+ str(host))
        child.expect("Password: ")
        password = raw_input("Please enter your password: ")
        child.sendline(password)
        child.timeout = 4
        child.expect('.*#.*')
        print 'connected to device!!!!\n'
        print child.before
        return child

    except pexpect.ExceptionPexpect :
        error = file('mylog.txt', 'w')
        child.logfile = error
        print "Login failed check the log file"


def readFile():

    print "You are now working in directory: \n"
    workingDir = os.getcwd()
    print workingDir
    dir = str(raw_input("Ïs this the right directory?"))
    if dir == "yes":
        fileName = str(raw_input("Please enter the file name including the extension: "))
        file = open(fileName)
        return file.readlines()

    elif dir == "no":
        getdir = str(raw_input("Please enter the directory: "))
        if os.path.exists(getdir):
            os.chdir(getdir)
            print "You are now working in directory: \n"
            print workingDir
            fileName = str(raw_input("Please enter the file name including the extension: "))
            newFile = open(fileName)
            return newFile.readlines()
        else:
            os.mkdir(getdir)
            os.chdir(getdir)
            print "You are now working in directory: \n"
            print workingDir
            fileName = str(raw_input("Please enter the file name including the extension: "))
            newFile = open(fileName)
            return newFile.readlines()


def writeToCSV(data):

    try:
        outputFile = open('output2.txt', 'a')
        outputFile.write(data)
        print "Data written to file!"
        outputFile.close()


    except Exception:
        sys.exit("Could not write to file")


def checkLicense(child):

    child.sendline('terminal length 0')
    child.expect('.*#.*')
    child.sendline('show license | i license')
    child.expect('#')
    writeToCSV(str(child.before))
    child.sendline('sh license usage | i "In use | Yes"')
    child.expect('#')
    writeToCSV(str(child.before))
    child.flush()




def main():

    host = readFile()

    for i in range (0, host.__len__()):
        child = connectToDevice(host[i])
        Thread(target=checkLicense(child)).start()
    sys.exit("All your data has been sent to the file specified. Goodbye!")

main()
