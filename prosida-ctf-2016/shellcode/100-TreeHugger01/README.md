= TreeHugger01 - Shellcode 100 =
Lytter på ctf2016.the-playground.dk:11001
Eksekverer den shellcode, som du sender den.

Processen opretter et stort balanceret binært søgetræ. Elementerne ser sådan ud:

#define MAX_STRING_LENGTH 64
typedef struct _treenode_t {
    struct _treenode_t * left;
    struct _treenode_t * right;
    unsigned int pattern;
    char text[MAX_STRING_LENGTH];
} treenode_t;

Ét element har pattern = 0xdeadbeef.

Find det og returner adressen på dets 'text' member.

Koden, som læser og eksekverer shellcoden ser sådan her ud:

char * (*shellcode)(treenode_t*);
shellcode = mmap(NULL, 4096, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
read(0, shellcode, MIN(max_shellcode_size, 1024));
printf("%s\n", shellcode(&nodes[0]));
exit(0);

max_shellcode_size er 1024!

Elementet, som du skal lede efter, får sin text initialiseret ud fra første argument til programmet, så du kan teste din shellcode således:

$ MAX_SHELLCODE_SIZE=1024 ./treehugger 'Hello, World' < shellcode
Hello, World
