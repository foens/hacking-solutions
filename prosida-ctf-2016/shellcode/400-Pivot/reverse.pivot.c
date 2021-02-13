void __attribute__((noreturn)) handle_alarm(int sig __attribute__((unused))) {
    exit(0);
}

int main(int argc, char* argv[])
{
	int counter = 0; // var18
	char buffer[1024]; // var1c
	signal(SIGALRM, handle_alarm);
	alarm(60);
	
	memset(buffer, 0, sizeof(buffer));
	
	while(counter < sizeof(buffer)-1)
	{
		unsigned int **b_loc = __ctype_b_loc();
		int *esi = b_loc[0];
		char input = getchar();
		buffer[counter] = input;
		current++;		
		unsigned int* pointer = input;
		pointer *= 2;
		pointer += esi;
		int a = *pointer;
		if((a & 0x4000) == 0) // binary: 0100 0000 0000 0000
			break;
	}
	
	(&buffer[0])();
	return 0;
}