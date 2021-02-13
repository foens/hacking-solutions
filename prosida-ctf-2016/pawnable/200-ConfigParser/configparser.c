#include <ctype.h>
#include <unistd.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <signal.h>
#include <sys/types.h>

typedef int (setting_callback_t)(char * key, char * val, void * data);

typedef struct {
    uint16_t port;
    char addr[16];
    char file_path[256];
} config_t;

void __attribute__((noreturn)) handle_alarm(int sig __attribute__((unused))) {
    exit(0);
}

char * parse(char * data, int size, setting_callback_t callback, void * user_data) {
    struct {
        int i;
        int j;
        int line;
        char key[16];
        char val[64];
    } local_data;

    local_data.line = 0;
    local_data.i = 0;
    while (local_data.i < size) {
        memset(&local_data.val, 0, sizeof(local_data.val));
        memset(&local_data.key, 0, sizeof(local_data.key));
        while (local_data.i < size && isblank(data[local_data.i])) {
            local_data.i++;
        }
        local_data.j = 0;
        while (local_data.i < size && data[local_data.i] != '=') {
            local_data.key[local_data.j++] = data[local_data.i++];
        }
        local_data.i++;
        local_data.j = 0;
        while (local_data.i < size && data[local_data.i] != '\n') {
            local_data.val[local_data.j++] = data[local_data.i++];
        }
        local_data.i++;
        local_data.line++;
        if (local_data.key[0] && local_data.val[0]) {
            if (callback(local_data.key, local_data.val, user_data) == 0) {
                printf("Unrecognized config option on line %d: %s\n", local_data.line, local_data.key);
                break;
            }
        }
    }
    return data;
}

int handle_keys(char * key, char * value, void * user_data) {
    config_t * conf = user_data;
    int was_recognized = 1;

    if (strcmp(key, "host") == 0) {
        strncpy(conf->addr, value, 15);
    } else if (strcmp(key, "port") == 0) {
        conf->port = atoi(value);
    } else if (strcmp(key, "path") == 0) {
        strncpy(conf->file_path, value, 255);
    } else {
        was_recognized = 0;
    }

    return was_recognized;
}

int main(int argc __attribute__((unused)), char *argv[] __attribute__((unused))) {
    char buffer[1024];
    int bytes_read;
    config_t config;

    setvbuf(stdout, NULL, _IONBF, 0);
    signal(SIGALRM, handle_alarm);
    alarm(60);

    memset(&config, 0, sizeof(config_t));
    bytes_read = read(0, buffer, sizeof(buffer));
    parse(buffer, bytes_read, handle_keys, &config);
    /* Now that we have parsed the received configuration, let's do nothing with it */
    
    return 0;
}
