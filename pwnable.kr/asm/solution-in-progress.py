#!/usr/bin/env python3
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./asm')


# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start():
    """Start the exploit against the target."""
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif args.LOCAL:
        return process([exe.path] + argv, *a, **kw)
    else:
        return remote('pwnable.kr', 9026)


# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
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
io = start()

io.interactive()
