= TreeHugger02 - Shellcode 200 =
Lytter på ctf2016.the-playground.dk:11002

Nøjagtig den samme som TreeHugger01, bortset fra at max_shellcode_size er 20!

Forresten, koden som opretter træet ser sådan her ud:

treenode_t * create_random_tree(int num_nodes) {
    int i;
    treenode_t * nodes = calloc(num_nodes, sizeof(treenode_t));
    for (i = 0; i < num_nodes; i++) {
        nodes[i].pattern = i;
        ....
    return nodes;
}

Test din shellcode således:
$ MAX_SHELLCODE_SIZE=20 ./treehugger 'Hello, World' < shellcode
Hello, World
