# This repository
Contains resources or solutions to various hacking challenges.

# Resources
## Learning material
* Prosa Hacking Workshop for Noobs
    *  [Youtube vidoes](https://www.youtube.com/channel/UCkrcc5UJDJdHwzRMxZgU0QQ/videos?view=0&shelf_id=0&sort=dd)
    *  [workshop vm](https://github.com/RobertLarsen/ProsaWorkshop)
    *  Course material
        * [00-intro](http://www.the-playground.dk/00-intro.html)
        * [01-reversing](http://www.the-playground.dk/01-reversing.html)
        * [02-exploitation](http://www.the-playground.dk/02-exploitation.html)
        * [03-shellcoding](http://www.the-playground.dk/03-shellcoding.html)

## Guides
* [Compiling GDB and GDBserver](guides/compile-gdb-and-gdbserver.md)
* [Enabling core dumps](guides/enabling-core-dumps.md)
* [Examine binary properties](guides/examining-binary-properties.md)
* [Privilege escalation](guides/privilege-escalation.md)

## Challenges
* CTF's
    * [Prosa CTF 2013](http://ctf2013.the-playground.dk/index.php?page=udfordringer)
    * [Prosa CTF 2014](http://ctf2014.the-playground.dk/index.php?page=udfordringer)
    * [Haaukins Aarhus](https://aarhus.haaukins.com)
* Challenge sites
    * [Overthewire - Narnia](https://overthewire.org/wargames/narnia/) 
    * [pwnable.kr](https://pwnable.kr/play.php)
    * [pwnable.tw](https://pwnable.tw/challenge/)
    * [RingZer0 Team Online CTF](https://ringzer0ctf.com/challenges)
    * [Hacker Gateway](https://www.hackergateway.com/challenges)
    * [HackTheBox](https://www.hackthebox.eu/)

## Tools
* [pwntools](https://github.com/Gallopsled/pwntools)
* [Ghidra](https://ghidra-sre.org/)
* [pwndgdb](https://github.com/pwndbg/pwndbg)

### Install pwntools
Tested on WSL1 Ubuntu 20.04:

```
sudo apt-get install python3 python3-pip python3-dev git libssl-dev libffi-dev build-essential binutils-*-linux-gnu
sudo pip3 install pwntools
```

### Ubuntu 20.04 VM with pwntools and pwngdb

On Windows:

* Install [Vagrant](https://www.vagrantup.com/downloads)
* Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
* In Windows Command Promt `cmd`, execute the commands below while being in the directory containing the `Vagrantfile` file:

```
vagrant up
vagrant ssh
```
