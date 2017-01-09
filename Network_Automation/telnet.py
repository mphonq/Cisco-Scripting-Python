import sys
import pexpect



login_to_router = raw_input("Please enter the name of the device to login to: ")


hosts = {'R1': '192.168.178.88', 'R2': '192.168.178.88', 'R3': '192.168.178.88', 'R4': '192.168.178.88', 'R5': '192.168.178.88', 'R6': '192.168.178.88',  'R7': '192.168.178.88', 'R8': '192.168.178.88', 'R9': '192.168.178.88', 'R10': '192.168.178.88'}

ports = {'R1': '17000', 'R2': '17004', 'R3': '17006', 'R4': '17008', 'R5': '17010', 'R6': '17012', 'R7': '17014', 'R8': '170164', 'R9':'17018', 'R10': '17002'}

def connectToHost():
	child = pexpect.spawn('telnet ' + hosts[login_to_router] + '  ' + ports[login_to_router])
	print child.after
	return child

def interact(child):
	child.interact()
	if child.isalive():
		child.sendline('exit')
		child.close
	if child.isalive():
		print ('Child did not exit gracefully')
	else:
		print ('Child exited gracefully.')

def baseline_eigrp_classic(child):
	numberOfnetworks = int(raw_input("Please enter the number of networks you would like to advertise: "))
	as_number = raw_input("Please enter the eigrp as number: ")
	child.sendline('\r' + '\r')
	child.sendline('config t')
	child.expect('.*#.*')
	child.sendline('router eigrp ' + as_number)
	child.expect('.*#.*')
	for i in range(0, numberOfnetworks):
		if i < numberOfnetworks:
			address = raw_input("Please enter network address you would like to advertise: ")
			child.sendline('network ' + address)
	child.expect('.*#.*')
	child.sendline(chr(26))



def baseline_eigrp_named(child):
	numberOfnetworks = int(raw_input("Please enter the number of networks you would like to advertise: "))
	as_name = raw_input("Please enter the eigrp process name: ")
	as_number = raw_input("Please enter the eigrp as number: ")
	child.sendline('\r' + '\r')
	child.sendline('config t')
	child.expect('.*#.*')
	child.sendline('router eigrp ' + as_name)
	child.expect('.*#.*')
	child.sendline('address-family ipv4 unicast autonomous-system' + as_number)
	for i in range(0, numberOfnetworks):
		if i < numberOfnetworks:
			address = raw_input("Please enter network address you would like to advertise: ")
			child.sendline('network ' + address)
	child.expect('.*#.*')
	child.sendline(chr(26))


def main():
	secondChild = connectToHost()
	interactive = raw_input("Do you want to proceed to interactive mode? ")
	if interactive == "yes":
		interact(secondChild)
	elif interactive == "no":
		classic = raw_input("Do you want to classic or name mode? ")
		if classic == "classic":
			baseline_eigrp_classic(secondChild)
		elif classic == "named":
				baseline_eigrp_named(secondChild)
	else:
		sys.exit("Unkown input relaunch the program!")

main()
