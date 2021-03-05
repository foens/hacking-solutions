# Examining binary properties
## Check security properties
The following requires `pwntools` to be installed:

```
checksec $binary
```

Example output:

```
[*] '/bin/bash'
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    Canary found
    NX:       NX enabled
    PIE:      PIE enabled
    FORTIFY:  Enabled
```

## Check required dynamic libraries
```
readelf -d $binary | grep NEEDED
```

Example output:

```
 0x0000000000000001 (NEEDED)             Shared library: [libtinfo.so.6]
 0x0000000000000001 (NEEDED)             Shared library: [libdl.so.2]
 0x0000000000000001 (NEEDED)             Shared library: [libc.so.6]
```