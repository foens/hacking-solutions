void __attribute__((noreturn)) handle_alarm(int sig __attribute__((unused))) {
    exit(0);
}

void decode(char[] buffer, char* currentBufferEntry)
{
	
}

int main(int argc, char* argv[])
{
	char[] var38;
	int var28 = 0;
	char[128] buffer;
	signal(SIGALRM, handle_alarm);
	alarm(60);
	setvbuf(stdout, NULL, _IONBF, 0);
	setvbuf(stderr, NULL, _IONBF, 0);
	memset(buffer, 0, sizeof(buffer));
	int var3c;
	
	char input;
	while((var28/4)*3 < 128)
	{
		input = getc(stdin)
		if(input == EOF)
			break;
		if(input == 10) // '\n'
			break;
		
		var38[var28 & 3] = input;
		var28++;
		if(var28 & 3 == 0) // Every 4 reads
		{
			decode(&buffer, &buffer+((var28-1)/4)*3)
			/*var3c = ((var28 -1)/4)*2;
			something2 = ((var28 -1)/4)*5;
			decode(var38, something2)*/
		}
	}
	if(input == EOF)
		exit(0);
	
	int[2] pipefd;
	if(pipe(pipefd) != 0)
		return 0;
	
	
}