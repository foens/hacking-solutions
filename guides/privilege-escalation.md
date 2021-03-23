# Privilege escalation
## What can execute as root without password

```
sudo -l
```

## SETENV in /etc/sudoers
If `SETENV` is allowed, an `LD_PRELOAD` trick can be used to obtain root.

Use the following: https://www.exploit-db.com/exploits/7129

## Find SUID/SGID binaries

```
find / -perm -u=s -type f 2>/dev/null
find / -perm -g=s -type f 2>/dev/null
```

Look here for how to use special binaries with SUID: https://gtfobins.github.io
