#include <stdio.h>
#include <stdlib.h>

void authenticate(int secret) {
    char name[32];
    puts("Hello there, could you tell me your name please?");
    fflush(stdout);
    gets(name);
    if(secret == 0xcafebabe)
    {
	puts("Welcome administrator");
        fflush(stdout);
        system("/bin/sh");
    } else
    {
        puts("Sorry, but you are not authenticated");
        fflush(stdout);
    }
}
int main(int argc, char *argv[]) {
    authenticate(0xaabbccee);
    return 0;
}
