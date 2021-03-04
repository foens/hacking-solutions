#!/usr/bin/env python3
import pwn
"""
The goal is to simply 'survive' the experiment by not having the program
crash in the fast_memcpy function.

The problem is that movdqa requires any memory address to be 16-byte aligned.
The solution below bruteforces each round by trying up to 16 different byte offsets.
"""

solution = [8, 16, 32]
solved_rounds = len(solution)
keep_running = True

while keep_running:
    solved_round = False
    for i in range(0, 16):
        with pwn.context.local(log_level='error'):
            io = pwn.remote('pwnable.kr', 9022)
        next_number_to_try = 2 ** (solved_rounds + 3) + i
        io.recvuntil('No fancy hacking, I promise :D\n')
        pwn.info("Round %d: Trying %d (+%d)" % (solved_rounds, next_number_to_try, i))
        for round in range(0, 10):
            if round < solved_rounds:
                io.sendline(str(solution[round]))
            elif round == solved_rounds:
                io.sendline(str(next_number_to_try))
            else:
                io.sendline(str(2 ** (round + 3)))
            io.recv()
        io.recvuntil('ok, lets run the experiment with your configuration\n')
        newlines_per_solved_round = 4
        with pwn.context.local(log_level='error'):
            results = io.recvall()
        lines = results.strip().split(b'\n')
        progress_to_round = int(len(lines) / newlines_per_solved_round) - 1

        if b'flag :' in results:
            pwn.success("Wooohooo. Found flag:\n%s " % lines[len(lines)-1].decode('utf8'))
            keep_running = False
            solved_round = True
            break

        if progress_to_round > solved_rounds:
            solution.append(next_number_to_try)
            solved_rounds += 1
            pwn.success("Yay. Found solution for round %d: %d\nSolution so far: %s" %
                     (solved_rounds, next_number_to_try, solution))
            solved_round = True
            break
    assert solved_round
