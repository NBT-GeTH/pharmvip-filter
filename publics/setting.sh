#!/bin/bash
path_tmp="/mnt/_tmp"
drive="$1"
check_path=$(which conda)
check_conda=$(echo $?)
if [ $check_conda -eq 0 ]; then
    ENV_BASE=$(conda info | grep "base environment" | awk '{print $4}')
    source $ENV_BASE/etc/profile.d/conda.sh
    SHELL_LEVEL=$(conda info | grep 'shell level' | grep -o -E "[0-9]+")
    for (( n=SHELL_LEVEL; n>=0; n-- ));
    do
        conda deactivate
    done
    echo -e '\n>>> Conda Deactivate'
else
    echo -e '>>> Not found Conda'
fi
cd ~/
if [ -d "${path_tmp}" ]; then
    umount ${path_tmp}
    mount -t drvfs ${drive} ${path_tmp}
else
    mkdir ${path_tmp}
    mount -t drvfs ${drive} ${path_tmp}
fi
check_path=$(which tabix)
check_tabix=$(echo $?)
if [ $check_tabix -eq 1 ]; then
    echo -e 'Wait Install Tabix ......'
    apt-get install tabix -y
else
    echo -e '>>> Tabix Already Installed'
fi

check_path=$(which samtools)
check_samtools=$(echo $?)
if [ $check_samtools -eq 1 ]; then
    echo -e 'Wait Install Samtools ......'
    apt-get install samtools -y
else
    echo -e '>>> Samtools Already Installed'
fi

check_path=$(which bcftools)
check_bcftools=$(echo $?)
if [ $check_bcftools -eq 1 ]; then
    echo -e 'Wait Install Bcftools ......'
    apt-get install -y bcftools
else
    echo -e '>>> Bcftools Already Installed'
fi