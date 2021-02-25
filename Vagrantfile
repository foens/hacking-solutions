Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y python3 python3-pip python3-dev git libssl-dev libffi-dev build-essential binutils-*-linux-gnu tmux gdb
    pip3 install pwntools
    git clone https://github.com/pwndbg/pwndbg.git
    cd pwndbg
    ./setup.sh
  SHELL
end
