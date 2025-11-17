# HPC Simulation with VirtualBox and Ubuntu Server

This guide demonstrates how to automate the creation of a VirtualBox VM with Ubuntu Server using **cloud-init**. Once the base VM image is created, it can be cloned to deploy multiple instances quickly.

## 1. Download Ubuntu Server ISO
Download the Ubuntu Server ISO, e.g.:
```
ubuntu-24.04.3-live-server-amd64.iso
```
You can choose any Ubuntu Server version you prefer.

## 2. Create a VirtualBox VM
Use the following commands to create a base VM:
```
# Create VM
VBoxManage createvm --name "ubuntu-base" --ostype Ubuntu_64 --register

# Configure RAM and CPU
VBoxManage modifyvm "ubuntu-base" --memory 2048 --cpus 2 --nic1 nat

# Create a virtual disk
VBoxManage createmedium disk --filename ~/VirtualBox\ VMs/ubuntu-base/ubuntu-base.vdi --size 20000

# Attach the disk
VBoxManage storagectl "ubuntu-base" --name "SATA Controller" --add sata --controller IntelAhci

VBoxManage storageattach "ubuntu-base" --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium ~/VirtualBox\ VMs/ubuntu-base/ubuntu-base.vdi

# Attach the Ubuntu ISO
VBoxManage storagectl "ubuntu-base" --name "IDE Controller" --add ide
VBoxManage storageattach "ubuntu-base" --storagectl "IDE Controller" --port 0 --device 0 --type dvddrive --medium ~/Download/ubuntu-24.04.3-live-server-amd64.iso
```

Replace the ISO path with the location where you downloaded your Ubuntu Server ISO.

## 3. Prepare Cloud-Init ISO
Cloud-init allows you to automatically configure the VM during its first boot.
### 3.1 Create Cloud-Init Configuration Files

`user-data`
```
#cloud-config
hostname: my-default-vm
manage_etc_hosts: true

users:
  - name: admin
    groups: [sudo]
    shell: /bin/bash
    sudo: ["ALL=(ALL) NOPASSWD:ALL"]
    ssh_import_id:
      - gh:your-github-username

packages:
  - htop
  - git
  - curl

runcmd:
  - echo "Default VM setup complete" > /etc/motd
```
`meta-data`
```
instance-id: ubuntu-base-001
local-hostname: my-default-vm
```
### 3.2 Generate Cloud-Init ISO
Run the following command to create the cloud-init seed ISO:
```
genisoimage -output seed.iso -volid cidata -joliet -rock user-data meta-data
```
## 4. Boot VM and Install Ubuntu
Start the VM:
```
VBoxManage startvm "ubuntu-base" --type headless
```
- The Ubuntu Server installer will boot.
- Cloud-init will automatically configure users, install packages, and set the hostname.
- Complete any minimal installation steps if required (e.g., network setup, SSH).

## 5. Clone VM for Multiple Instances
Once the base VM is ready, clone it to create multiple instances:
```
VBoxManage clonevm "ubuntu-base" --name "ubuntu-vm1" --register
VBoxManage clonevm "ubuntu-base" --name "ubuntu-vm2" --register
```
You can repeat this command to create as many VMs as needed.
