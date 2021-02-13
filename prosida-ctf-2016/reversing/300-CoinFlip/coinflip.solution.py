from pwn import *

context(arch = 'i386', os = 'linux')

PROGRAM = './coinflip'
#ELF(PROGRAM)

def get_heads_or_tails(hour, minute, second, zone, tryNumber):
	import subprocess
	command = './get_heads_or_tails ' + hour + ' ' + minute + ' ' + second + ' ' + zone + ' ' + str(tryNumber);
	p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	line = p.stdout.readlines()[0].strip()
	assert line == 'heads' or line == 'tails', 'Expected heads or tails but got: ' + line + '\nExecuted command:\n' + command
	return line

#p = process(PROGRAM)
p = remote("ctf2016.the-playground.dk", 13003)
line = p.recvline()
print line
m = re.search('It is now (\d\d):(\d\d):(\d\d) ([+-]\d\d\d\d) and I give you 30 seconds to win 100 c', line)
if not m:
	print "Error"
	exit(1)
hour = m.group(1)
minute = m.group(2)
second = m.group(3)
zone = m.group(4)

for i in range (0,100):
	#print p.recvuntil('Heads or tails?:')
	head_or_tail = get_heads_or_tails(hour, minute, second, zone, i)
	print head_or_tail
	p.sendline(head_or_tail)
	#print p.recvline()
	
for i in range (0,100):
	print p.recvuntil('Heads or tails?:')
	print p.recvline()
	
print p.recvline()
print p.recv()