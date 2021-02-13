# The syscall challenge
```
I made a new system call for Linux kernel.
It converts lowercase letters to upper case letters.
would you like to see the implementation?

Download : http://pwnable.kr/bin/syscall.c


ssh syscall@pwnable.kr -p2222 (pw:guest)
```

# Information gathering
When logging in, a system boots in qemu which emulates an 32bit armv7. Thus, we need to create an arm7 binary. The target is arm-linux-gnuabihf.

# Idea
The `sys_upper` function can be called from userspace by executing an SVC instruction with
the syscall number of 223.
The function does not validate that the pointers come from userspace, so if running a split
user/kernel space memory model, we could:

 - Read kernel memory by setting the `in` to some kernel address and `out` to a userspace address.
 - Write kernel memory by copying from userspace to kernel space.

Since the system call is executed with kernel privileges, we would like to execute in that context.
Maybe we can overwrite the syscall address to point to userspace executable memory, thus
getting to run code in the kernel context.
To avoid overwriting another system call, a four-byte string could be passed. No null termination
is written.

# Moving binary to target and executing it
The compiled binary has to be moved to the target.

This has been done by:

- cat binary | base64 > base64.out
- copy contents of base64.out
- ssh syscall@pwnable.kr -p2222
- vi /tmp/in
- Typing `i` to go into insertion mode
- paste
- Typing `<esc>` followed by `:wq <enter>` to write and quit
- cat /tmp/in | base64 -d > /tmp/out
- chmod 777 /tmp/out
- ./tmp/out