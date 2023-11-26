# Linux Fundamentals

## Overview
- There are multiple flavours of Linux. We will start learning `Ubuntu`.
- We will be using [RaspberryPI 5](https://www.raspberrypi.com/products/raspberry-pi-5/) to explore this tutorial.

## Modules
- [Installation](#installation)
- Package Manager
- [System Init](#system-init)
- User & Roles
- File System
- Networking
- Processes
- Monitoring
- Shell Scripting
- [Commands](#commands)
- [Reference](#reference)

### Installation
- Download Raspberry Pi Imager from [here](https://www.raspberrypi.com/software/)
- Load SD card and flash 64bit Ubuntu Server as below
  - Operating System navigate: `Other general-purpose OS -> Ubuntu -> Ubuntu Server 23.10 (64-BIT)`
  - Storage: Select Flash Drive
  - Setting: Configure below
    - hostname: `As per your desire`
    - Enable ssh: `Use password authentication`
    - Set username and password: `As per your desire`
    - Configure wireless LAN: `As per your WIFI`
    - Set locale setting: `Set timezone & Keyboard Layout`
    ![](../00-Images/pi-imager.png)
- Static IP Address from Raspberry pi. 
  - This will change continuously.
  - To avoid this, login to `Wifi router -> Network -> DHCP Server -> Address Reservation`
  - Identify `MAC ID` of Raspberry Pi and start allocating an address range.
  - Reboot pi.
- Enable network
  ```bash
  sudo apt update
  sudo apt install net-tools
  hostname
  ifconfig
  shutdown now
  ```
- Access Raspberry pi from the Internet.
  - Login to [no-ip](https://www.noip.com/)
  - Goto `Dynamic DNS -> Create Hostname`
    ![](../00-Images/no-ip-hostname.png)
  - Goto `Wifi Router -> Dynamic DNS -> Register No-IP UserName, Password, Domain & Enable WAN IP Binding`. This step will help to automtically update Router public IP with No-IP Hostname.
  - Goto `Wifi Router -> Nat Forwarding -> DMZ -> Enter Pi IP Address & Enable`
- Testing
  - Windows Powershell Command
    ```powershell
    Test-NetConnection `no-ip domain` -p 22
    ```

### System Init
- It is the first process on boot (as PID 1) and acts as init system that brings up and maintains userspace services.
- `SystemD` is a system and service manager for Linux operating systems.
- It serves as an init system, which means it is responsible for initializing the user space and managing system services during the boot process.
- The most notable feature of SystemD was its parallelization capabilities and dependency-based service control logic, which allowed your system to start multiple processes in parallel, indirectly improving the boot time.
- SystemD is frequently misunderstood as a `daemon`, but it’s actually a software suite for Linux. It offers `systemctl`, a command-line tool to manage system services, often referred to as `daemons` or `systemd units`, to help you with common system administrator tasks.
- SystemD also introduces the concept of `units - a dependency system between various entities` to manage various services in your system, such as a service unit, mount unit, socket unit, slice unit, and so on, where units are referred to as configuration files.
- All the registered services are available at `/etc/systemd/system`.
- Before SystemD, `SystemV or Init` was used by Linux distros and `service` command is used by administrations to manage SystemV resources. Init services are available at `/etc/init.d/`
- In Microsoft Windows world this is similar to `cmd -> msconfig`

### Commands
- Check Temperature
  ```bash
  vcgencmd measure_temp
  ```
- Check Voltage - Good if code is `0x0`
  ```bash
  vcgencmd get_throttled
  dmesg | grep voltage
  ```
### Reference
- [PXE Booting](https://linuxhit.com/raspberry-pi-pxe-boot-netbooting-a-pi-4-without-an-sd-card/)
  
