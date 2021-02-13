#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <dirent.h>

#define USERNAME_MAX 32
#define PASSWORD_MAX 32

typedef struct {
    char name[USERNAME_MAX];
    char password[PASSWORD_MAX];
} user_t;

void __attribute__((noreturn)) handle_alarm(int sig __attribute__((unused))) {
    exit(0);
}

int authenticate(user_t * user __attribute__((unused))) {
    FILE * file;
    int good = 0, i, j;
    char line[USERNAME_MAX + 1 + PASSWORD_MAX + 1]; /* Enough for username, a colon, a password and a null terminator */
    char name[USERNAME_MAX];
    char password[PASSWORD_MAX];

    if ((file = fopen("users.db", "r"))) {
        while (good == 0 && !feof(file)) {
            memset(line, 0, sizeof(line));
            memset(name, 0, sizeof(name));
            memset(password, 0, sizeof(password));

            fgets(line, sizeof(line), file);
            for (i = 0; line[i] && line[i] != ':'; i++) {
                name[i] = line[i];
            }
            i++; /* go past colon */
            for (j = 0; line[i] && line[i] != '\n'; i++, j++) {
                password[j] = line[i];
            }

            good = (strcmp(user->name, name) == 0 && strcmp(user->password, password) == 0);
        }
        fclose(file);
    }

    return good;
}

user_t * report_unauthorized_access(char * filename, user_t * user) {
    FILE * file;
    char message[USERNAME_MAX + 8]; /* Enough for "Name: " , a name, a newline and a null terminator */

    memset(message, 0, sizeof(message));
    strcpy(message, "Name: ");
    strcat(message, user->name);
    strcat(message, "\n");

    if ((file = fopen(filename, "a"))) {
        fwrite(message, 1, strlen(message), file);
        fclose(file);
    }
    return user;
}

void read_mail(user_t * user, char * mail_to_read) {
    FILE * mailfile;
    char buffer[256];
    int bytes_read;
    strcpy(buffer, "mails/");
    strcat(buffer, user->name);
    strcat(buffer, "/");
    strcat(buffer, mail_to_read);

    if ((mailfile = fopen(buffer, "r"))) {
        printf("------------------------------\n");
        while (!feof(mailfile)) {
            bytes_read = fread(buffer, 1, sizeof(buffer), mailfile);
            fwrite(buffer, 1, bytes_read, stdout);
        }
        fclose(mailfile);
        printf("\n------------------------------\n");
    } else {
        printf("No such mail!\n");
    }
}

void read_mail_menu(user_t * user) {
    char mail_path[7 + USERNAME_MAX]; /* Enough for "mails/", a name and a null terminator */
    char mail_to_read[256];
    DIR * dir;
    struct dirent * entry;
    int count = 0;

    strcpy(mail_path, "mails/");
    strcat(mail_path, user->name);

    printf("Which mail would you like to read? (%s)\n", mail_path);
    if ((dir = opendir(mail_path))) {
        while ((entry = readdir(dir))) {
            if (entry->d_type != DT_DIR) {
                count++;
                printf(" - %s\n", entry->d_name);
            }
        }
        closedir(dir);
        if (count) {
            printf("Choice: ");
            memset(mail_to_read, 0, sizeof(mail_to_read));
            fgets(mail_to_read, sizeof(mail_to_read), stdin);
            mail_to_read[strlen(mail_to_read) - 1] = 0; /* Remove newline */
            read_mail(user, mail_to_read);
        } else {
            printf("You have no mails!\n");
        }
    }
}

int read_number() {
    char buffer[16];
    fgets(buffer, sizeof(buffer), stdin);
    return atoi(buffer);
}

void run_mailserver(user_t * user) {
    int choice;
    do {
        printf("What would you like to do?\n1) Read mail\n2) Exit\nChoice: ");
        choice = read_number();
        if (choice == 1) {
            read_mail_menu(user);
        }
    } while (choice != 2);
}

int main(int argc __attribute__((unused)), char *argv[] __attribute__((unused))) {
    char buffer[256];
    user_t user;

    setvbuf(stdout, NULL, _IONBF, 0);
    signal(SIGALRM, handle_alarm);
    alarm(60);

    memset(buffer, 0, sizeof(buffer));
    memset(&user, 0, sizeof(user_t));

    printf("Welcome to the mailbox.\nEnter username: ");
    fgets(buffer, sizeof(buffer), stdin);
    buffer[strlen(buffer) - 1] = 0; /* Remove newline */
    strncpy(user.name, buffer, USERNAME_MAX);

    printf("Password: ");
    fgets(buffer, sizeof(buffer), stdin);
    buffer[strlen(buffer) - 1] = 0; /* Remove newline */
    strncpy(user.password, buffer, USERNAME_MAX);

    if (authenticate(&user)) {
        printf("Good boy!\n");
        run_mailserver(&user);
    } else {
        printf("Sorry, bad credentials.\n");
        report_unauthorized_access("bad_logins.log", &user);
    }

    
    return 0;
}
