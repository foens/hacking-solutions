shellcode:
      	push   ebp
      	mov    ebp,esp
      	sub    esp,0x28
      	cmp    DWORD PTR [ebp+0x8],0x0
      	jne    bv
      	mov    eax,0x0
      	jmp    qqq
  bv:      	mov    eax,DWORD PTR [ebp+0x8]
     	mov    eax,DWORD PTR [eax+0x8]
     	cmp    eax,0xdeadbeef
     	jne    f
     	mov    eax,DWORD PTR [ebp+0x8]
     	add    eax,0xc
     	jmp    qqq
  f:  mov    eax,DWORD PTR [ebp+0x8]
     	mov    eax,DWORD PTR [eax]
     	mov    DWORD PTR [esp],eax
     	call   shellcode
     	mov    DWORD PTR [ebp-0xc],eax
     	cmp    DWORD PTR [ebp-0xc],0x0
     	je     asdf
     	mov    eax,DWORD PTR [ebp-0xc]
     	jmp    qqq
  asdf:      	mov    eax,DWORD PTR [ebp+0x8]
       	mov    eax,DWORD PTR [eax+0x4]
       	mov    DWORD PTR [esp],eax
       	call   shellcode
  qqq:      	leave  
        	ret    

