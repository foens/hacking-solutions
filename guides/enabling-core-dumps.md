# Enable core dumps
## Set unlimited core dump size

```
ulimit -S -c unlimited
```
### If above command fails:
A hard limit for core files might be set. Check:

```
cat /proc/self/limits
```

## Set core dump location
Normal core dump location is specified in `/proc/sys/kernel/core_pattern`. To generate simple core files:

```
echo core > /proc/sys/kernel/core_pattern
```

# Disable core dumps

```
ulimit -S -c 0
```