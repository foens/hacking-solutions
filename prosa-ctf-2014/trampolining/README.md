# The task
http://ctf2014.the-playground.dk/index.php?page=trampolining

# Tips
* http://ctf2014.the-playground.dk/index.php?page=trampolining-tip-1
* http://ctf2014.the-playground.dk/index.php?page=trampolining-tip-2

## A command to find trampolining instructions:
`ROPgadget --binary trampolining |grep -E ': ((call)|(jmp)) ((eax)|(esp))'`