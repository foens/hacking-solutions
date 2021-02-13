shellcode:
  	   	push   ebp
  	   	mov    ebp,esp
  	   	mov    eax,DWORD PTR [ebp+0x8]
   f:	   	cmp    DWORD PTR [eax],0xdeadbeef
  	   	lea    eax,[eax+0x4]
  	   	jne    f
  	   	pop    ebp
  	   	ret    

