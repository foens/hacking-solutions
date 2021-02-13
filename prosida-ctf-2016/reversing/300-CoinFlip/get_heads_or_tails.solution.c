#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void main(int argc, char** argv)
{
	if(argc != 6)
	{
		printf("Error\n");
		exit(1);
	}
	int hour = atoi(argv[1]);
	int minute = atoi(argv[2]);
	int second = atoi(argv[3]);
	int timezone = atoi(argv[4]);
	int tryNumber = atoi(argv[5]);
	
	
	time_t currentTime = time(0);
	struct tm *tm = localtime(&currentTime);
	
	tm->tm_hour = hour;
	tm->tm_min = minute;
	tm->tm_sec = second;
	
	time_t time = mktime(tm);
	
	srand(time);
	while(tryNumber >= 0)
	{
		long long int random = rand();
		int tails = (random & 1) == 1;
		if(tryNumber == 0)
		{
			if(tails)
				printf("tails\n");
			else
				printf("heads\n");
		}
		tryNumber--;
	}
}