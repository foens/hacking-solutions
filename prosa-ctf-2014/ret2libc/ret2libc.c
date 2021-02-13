#include <stdio.h>
#include <string.h>
#include <signal.h>
#include <stdlib.h>
#include <dlfcn.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>

char buffer1[256];

static int create_server(unsigned short port) {
    int server;
    int flags;
    struct sockaddr_in addr;

    server = socket(AF_INET, SOCK_STREAM, 0);
    if (server < 0) {
        return -1;
    }

    flags = 1;
    if (setsockopt(server, SOL_SOCKET, SO_REUSEADDR, &flags, sizeof(flags)) < 0) {
        close(server);
        return -1;
    }

    addr.sin_family = AF_INET;
    addr.sin_port = htons(port);
    addr.sin_addr.s_addr = htonl(INADDR_ANY);

    if (bind(server, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
        close(server);
        return -1;
    }

    if (listen(server, 10) < 0) {
        close(server);
        return -1;
    }

    return server;
}

void child_died(int sig) {
    wait(&sig);
}

void handle_client(int client) {
    char buffer2[128];
    void * mprotect_ptr;
    mprotect_ptr = dlsym(0, "mprotect");

    dprintf(client, "Hello and welcome to this small ret2libc challenge.\nInteresting fact: mprotect is at 0x%08lx.\nNow give me a maximum of %d bytes which I'll place at 0x%08lx.\n", (long unsigned int)mprotect_ptr, sizeof(buffer1), (long unsigned int)buffer1);
    if (read(client, buffer1, sizeof(buffer1)) > 0) {
        dprintf(client, "Thanks a lot, now I'll read a maximum of %d bytes from you into a %d byte stack buffer.\n", sizeof(buffer2) * 4, sizeof(buffer2));
        if (read(client, buffer2, sizeof(buffer2) * 4) > 0) {
            dprintf(client, "There, all should be set now. Goodbye.\n");
        }
    }
}

int main(int argc, char ** argv) {
    int server, client, debug = (argc > 2 && strcmp(argv[2], "debug") == 0);

    if ((server = create_server(argc > 1 ? atoi(argv[1]) : 9988)) > 0) {
        if (!debug) {
            signal(SIGCHLD, child_died);
            daemon(0, 0);
        }
        while (1) {
            if ((client = accept(server, NULL, NULL)) < 0) {
                exit(1);
            }
            if (!debug && fork()) {
                close(client);
            } else {
                close(server);
                handle_client(client);
                close(client);
                return 0;
            }
        }
    } else {
        fprintf(stderr, "Could not create server socket.\n");
    }
    return 0;
}
