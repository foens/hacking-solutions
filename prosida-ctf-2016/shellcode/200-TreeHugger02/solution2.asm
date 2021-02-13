
solution2.o:     file format elf32-i386


Disassembly of section .text:

00000000 <shellcode>:
   0:	55                   	push   ebp
   1:	89 e5                	mov    ebp,esp
   3:	8b 45 08             	mov    eax,DWORD PTR [ebp+0x8]
   6:	81 78 08 ef be ad de 	cmp    DWORD PTR [eax+0x8],0xdeadbeef
   d:	74 05                	je     14 <shellcode+0x14>
   f:	83 c0 4c             	add    eax,0x4c
  12:	eb f2                	jmp    6 <shellcode+0x6>
  14:	83 c0 0c             	add    eax,0xc
  17:	5d                   	pop    ebp
  18:	c3                   	ret    

Disassembly of section .text.startup:

00000000 <main>:
   0:	55                   	push   ebp
   1:	31 c0                	xor    eax,eax
   3:	89 e5                	mov    ebp,esp
   5:	5d                   	pop    ebp
   6:	c3                   	ret    
