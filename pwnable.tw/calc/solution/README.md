# Bugs
There are many bugs:

* The code does not allow to use `0`, however, that happens with a `strcmp(v, "0")`. A value such as `00` is still allowed.
* If the value after `atoi` conversion is `<= 0` then the value is not pushed to the pool. This allows us to calculate on earlier values
* The pool and op_stack only have room for 100 values. However, if more are used, they could be overflown.

# Writeup
It is possible to read and write offsets on the stack. A specific offset can be read to obtain the absolute address of the stack. The binary uses stack canaries, but these can be skipped and a small ROP chain that calls `mprotect` to circumvent `NX` protection can be made. Afterwards, shellcode to open `/bin/sh` can be executed to obtain a shell.
