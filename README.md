# FSND-Project-Item-Catalog

In this project,students will develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

## Getting Started

These instructions will show you how to run the application locally.

### Prerequisites

* [Vagrant](https://www.vagrantup.com/)
* [Virtual Box](https://www.virtualbox.org/)
* [Python 2.7](https://www.python.org/downloads/release/python-2713/)

### Installing
1. Install [Virtual Box](https://www.virtualbox.org/)
  1. VirtualBox is the software that actually runs the virtual machine.
2. Install  [Vagrant](https://www.vagrantup.com/)
  1. Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem.
3. Download the VM configuration:
  1. Clone the repo by running the following command from the command prompt
    1. `$ git clone https://github.com/jefferygraham992/FSND-Project-Item-Catalog.git`
  2. Change to the  application directory
    1. `$ cd /FSND-Project-Item-Catalog`
  3. Change directory to the vagrant directory inside (this directory contains the VM confidguration)
    1. `$ cd /vagrant`
4. Start the virtual machine:
  1. From your terminal, inside the vagrant subdirectory, run the command **vagrant up**. This will cause Vagrant to download the Linux operating system and install it.
    1. `$ vagrant up`
  2. When vagrant up is finished running, you can run **vagrant ssh** to log in to your newly installed Linux VM.
    1. `$ vagrant ssh`
  3. Change directory to /vagrant
    1. `$ cd /vagrant`
  4. Change directory to /vagrant
    1. `$ cd  /catalog`
5. Create the database
  1. `$  python thomascatalog.db`
6. Run the **thomastrains.py** file to to prepopulate the database with som items
  1. `$  python thomastrains.py`
7. Run the **project.py** file to run the application locally
  1. `$  python project.py`
8. Open a web browser and visit [http://localhost:8000](http://localhost:8000)
