# Compile gdb and cross compile gdbserver
## Vagrantfile
You can use this `Vagrantfile` to:

- build gdb that can:
  - debug many architectures but only run on your host.
  - use python such that `pwndbg` is supported.
- build gdbserver for `mipsel`. Change if you need another architecture.

```
Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"

  config.vm.provider "virtualbox" do |v|
    v.memory = 4096
    v.cpus = 8
  end

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    # Install gcc for the correct cross-architecture
    apt-get install -y build-essential texinfo bison flex python3 python3-dev gcc-mipsel-linux-gnu g++-mipsel-linux-gnu
  SHELL

  config.vm.provision "shell", privileged:false, inline: <<-SHELL
    # Fetch gdb, update version if needed
    git clone --depth 1 --branch gdb-10.1-release git://sourceware.org/git/binutils-gdb.git

    # Build gdb
    mkdir -p ~/build-gdb
    cd ~/build-gdb
    ~/binutils-gdb/configure --prefix $(pwd)/install --enable-targets=all --with-python=/usr/bin/python3
    make -j$(nproc) all-gdb
    make install -C gdb

    # Build gdbserver
    mkdir -p ~/build-gdbserver
    cd ~/build-gdbserver
    # Specify correct host and use correct CC for the cross-architecture
    ~/binutils-gdb/configure --prefix $(pwd)/install --host=mipsel-linux-gnu CC="mipsel-linux-gnu-gcc" CXX="mipsel-linux-gnu-g++" LDFLAGS="-static" --disable-gdb
    make -j$(nproc) all-gdbserver
    make install -C gdbserver
  SHELL
end
```
