gcc -m32 -c solution.c -o solution.o
objdump -Mintel -d solution.o > solution.asm
<ret asm fil s� kun den n�dvendige kode er tilstede og ingen absolute jumps>
asm -c i386 < opgave.asm