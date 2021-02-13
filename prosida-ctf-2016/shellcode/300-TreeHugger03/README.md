= TreeHugger03 - Shellcode 300 =
Lytter på ctf2016.the-playground.dk:11003

Nøjagtig den samme som TreeHugger01, bortset fra at max_shellcode_size er 6!

Test din shellcode således:
$ MAX_SHELLCODE_SIZE=6 ./treehugger 'Hello, World' < shellcode
Hello, World
