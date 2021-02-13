from pwn import *

context(arch = 'i386', os = 'linux')

PROGRAM = './bepolite'
#ELF(PROGRAM)

def connect():
	#p = process(PROGRAM)
	p = remote("ctf2016.the-playground.dk", 13002)
	p.recvuntil('Good day to you sir/madam. How may I help you today?\n')
	p.sendline('Good day.')
	return p

def list_directory(directory):
	p = connect()
	p.sendline('Would you be so kind as to provide me with a list of items in the ' + directory + ' directory please?')
	candidates = []
	while True:
		try:
			line = p.recvline(keepends = False)
			if line == "" or line == 'How rude!':
				break
			print line
			if line == "flag":
				print directory + "flag"
				return read_file(directory + "/flag")
			candidates.append(line)
		except:
			print directory + " is not a directory"
			break
	for dir in candidates:
		if list_directory(directory + dir):
			return True
	
def read_file(file):
	p = connect()
	p.sendline('I wonder, would it be too much to ask for the content of ' + file +'?')
	print p.recv()
	return True
	

list_directory('./')
#read_file('./rDbAY37dbJ/UOGPir7rRm/a9UeuuTFP4/flag')