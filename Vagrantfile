Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/focal64"

  # When using Windows as host and Linux as guest and the shared folder is on
  # NTFS, then the file permissions are not executable.
  config.vm.synced_folder ".", "/vagrant", mount_options: ["fmode=700"]

  config.vm.provision "shell", inline: <<-SHELL
    apt-get update
    apt-get install -y python3 python3-pip python3-dev git libssl-dev libffi-dev build-essential binutils-*-linux-gnu tmux gdb
    pip3 install pwntools
  SHELL

  config.vm.provision "shell", privileged:false, inline: <<-SHELL
    git clone https://github.com/pwndbg/pwndbg.git
    cd pwndbg
    ./setup.sh
  SHELL
end
