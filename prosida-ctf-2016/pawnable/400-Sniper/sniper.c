#include <stdio.h>
#include <signal.h>
#include <unistd.h>
#include <stdlib.h>

void handle_alarm(int sig __attribute__((unused))) {
    exit(0);
}

void pwn_me() {
    char buffer[128];
    printf("Let's cut the crap...this one needs precision and a bit of brute forcing!\n");
    read(0, buffer, 137);
}

int main(int argc __attribute__((unused)), char *argv[] __attribute__((unused))) {
    setvbuf(stdout, NULL, _IONBF, 0);
    signal(SIGALRM, handle_alarm);
    alarm(10);

    pwn_me();
    return 0;
}
