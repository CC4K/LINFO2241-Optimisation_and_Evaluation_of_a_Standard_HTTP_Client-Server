# LINFO2241: Project setup

Welcome to this installation guide ! We'll guide you through the setup of LINFO2241's project :)

## SSH Setup (Mandatory for Mac users, not necessary if you have a bare-metal Linux install)

***If you are using a MacOS computer you won't be able to do the project at all***, you must setup your SSH access to UCLouvain network to work on this project. To do so, you have two options:

### The automated way

Do this INGInious exercice: https://inginious.info.ucl.ac.be/course/welcome-ingi then add the private key to your .ssh directory (explained below).

### The manual way (Nice skill to have)

You must go **physically** to the Intel room in Réaumur building and connect to a computer. Once connected, simply follow the following steps:

#### On your computer

Generate a key that will be used to communicate safely with UCLouvain Network (I'm sure you don't want your wonderful project to leak to other students ;)). You just have to open a terminal and type the following:

```bash
ssh-keygen -t ed25519 -C "John Doe's nice ssh key !"
eval "$(ssh-agent -s)"
#Linux
ssh-add ~/.ssh/id_ed25519
#MacOS
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
```
Simply follow the steps on the screen and set a password if you want additional security (You'll have to enter it each time you want to connect to UCLouvain, so keep it in mind).

Now, you can simply show your key with:

```bash
cat ~/.ssh/id_ed25519.pub
# It should output something like "ssh-ed25519 AAAAC3N..."
```

Keep the result of this command in mind, you'll need it in the next steps.

#### On the Intel computer

Once logged in a computer in the Intel Room, open a terminal and run:

```bash
vi ~/.ssh/authorized_keys 
```

This command will open a in-terminal text editor. Don't panic, this will be over soon.

Type `i` to enter in insertion mode, and type the output of the command from the previous step (The weird thing starting with `ssh-ed25519 AAA...`). The funny part is that the output of the command was on your MacOS laptop and now you have to retype it on the Intel computer. You can be brave and retype it yourself or send it through any channel (Usually, by mail) to then simply copy/paste it. Once done, press `Esc` and type `:wq` to save and leave the editor.

Alternatively you can use nano to edit the file, but learning a few vi commands is handy.

```bash
nano ~/.ssh/authorized_keys 
```

### Back on your computer

Now, you should be able to connect to the SSH gateway by typing this in a terminal:

```bash
ssh YourID@studssh.info.ucl.ac.be -o ForwardAgent=yes -i ~/.ssh/id_ed25519
```

Where you replace `YourID` by your UCLouvain identifier. "-o ForwardAgent=yes" is used to forward your ssh agent (think your ssh credentials), it is useful when you use the studssh as a gateway to connect to the the actual machines. It avoids the need to transfer you ssh key directly to studssh. This is good practice. You can also copy paste you ***private*** ssh key to the .ssh folder of you studssh gateway.

Then you can connect to the Intel room servers using

```bash
ssh didacXX
```
where XX is the id of the machine you want to connect to (didac01 for instance). You can find a list of the servers available [here](https://wiki.student.info.ucl.ac.be/Mat%C3%A9riel/SalleIntel).  
If the connection doesn't work, please reach out to an assistant, we'll fix that.

#### Using a ssh config (recommended)

You are highly encouraged to use an ssh config to simplify the connection to the remote computers.

~/.ssh/config:

```bash
# Replace $YOURUSERNAME by your UCLouvain username
Host studssh
  HostName studssh.info.ucl.ac.be
  User $YOURUSERNAME
  ForwardX11 yes
  ForwardX11Trusted yes
  ForwardAgent yes
  IdentityFile ~/.ssh/$YOURKEY
  ServerAliveInterval 60

Host didac*
  Hostname %h
  User $YOURUSERNAME
  ForwardX11 yes
  ForwardX11Trusted yes
  ForwardAgent yes
  ServerAliveInterval 60
  ProxyCommand ssh studssh -W %h:%p
```

From your computer, you can use

```bash
ssh didac01
```

***If you use VSCode as your text editor, the SSH extension is very convenient to code remotely. Use it!***

## Prerequisites

For this project, you'll need **Linux**. If your machine is running on Windows or MacOS, please do not panic.

- **For Windows users**: Please setup WSL through the tutorial [here](https://learn.microsoft.com/en-us/windows/wsl/install). The default Ubuntu distribution will do just fine.
- **For Mac users**: You'll need to connect to UCL servers through SSH. Just follow the steps in the previous section.

You'll need basic compilation tools to work on this project. If you're working on UCLouvain's servers (which you should if your computer is running MacOS or Windows), they are already installed. For the others, the procedure depends on which distribution you're running. It should go be one of the following :  

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install build-essential libpcre3-dev zlib1g-dev libssl-dev
```

### Fedora

```bash
sudo dnf install make automake gcc gcc-c++ kernel-devel pcre-devel zlib-devel
```

### ArchLinux/Manjaro (not officially supported)

```bash
sudo pacman -S base-devel pcre2 zlib openssl
```

## Download repositories and build

If you haven't cloned the repository yet, open a terminal, then type:

```bash
git clone git@forge.uclouvain.be:LINFO2241/linfo2241-project-2024-2025-student.git LINFO2241-2024-2025
```

Then, you can move to the project directory:

```bash
cd LINFO2241-2024-2025
export PROJECT_PATH=$PWD
```

## Server setup


```bash
# Downloading NGINX
wget https://nginx.org/download/nginx-1.23.0.tar.gz
tar -xzf nginx-1.23.0.tar.gz
rm nginx-1.23.0.tar.gz
mv nginx-1.23.0/ nginx/
# Download required extension
git clone https://github.com/Taymindis/nginx-link-function.git
# You should include the nginx-link-function header into the c include path
export C_INCLUDE_PATH=$PROJECT_PATH/nginx-link-function/src
# Compile nginx
cd nginx
# NGINX will be installed here, we will have two versions, one for debug and one for performance
mkdir install_release
mkdir install_debug
# Release version
# WARNING: Read below !
# When configuring a project, you can often specify a prefix. Here it is given by the long
# argument --prefix. This argument specifies where the project will be installed on your system.
# By default it will install at the root of your system and you would thus need root (sudo) access.
# Here we specify a path in our project directory so we don't need root access.
./configure --add-module=$PROJECT_PATH/nginx-link-function --prefix=$PROJECT_PATH/nginx/install_release
make
make install
# Debug version, this specifies that the project should be compiled with debugging symbols.
# For this project, this is specificied using the long option --with-debug.
./configure --add-module=$PROJECT_PATH/nginx-link-function --prefix=$PROJECT_PATH/nginx/install_debug --with-debug
make
make install
```
💡: **Note** : To debug using the debugging version, you should learn the basics of using *gdb* and/or *valgrind*. You can find more information on the [official website](https://www.gnu.org/software/gdb/) and [here](https://valgrind.org/). Learning these tools is not mandatory, but it will make your life much easier.

⚠️ **Warning** : If you close your terminal, you might need to reuse these two commands or your code may not compile anymore :

```bash
# From the root directory of the project
export PROJECT_PATH=$PWD
export C_INCLUDE_PATH=$PROJECT_PATH/nginx-link-function/src
```

TIPS: you can specify compiler flags with `--with-cc-opt`

```bash
./configure --add-module=$PROJECT_PATH/nginx-link-function --prefix=$PROJECT_PATH/nginx/install --with-cc-opt='-O0 -g'
```

Congratulations, you're just a few steps away from the end of this tutorial! There are just a few changes to apply.

First, you must create log files for the application:  

```bash
touch $PROJECT_PATH/nginx/install_release/logs/error.log
touch $PROJECT_PATH/nginx/install_debug/logs/error.log
```

Now, you're ready for the final step of this guide: building your project!

```bash
cd $PROJECT_PATH/project/server_implementation
# Creating the build directory
mkdir build
# Compiling the project
make -B build
```

To run the server in release mode you can simply do :

```bash
make run_release
```

If you want more debugging information you can use the run_debug target (should be the default target when developing) :

```bash
make run_debug
```

We also provide you with another target that runs the server, runs [GDB](https://sourceware.org/gdb/), attaches to the worker process and continues the execution. This is ***very*** useful for debugging.

```bash
make run_gdb
```

Finally, we provide a Valgrind target that can be useful to detect wrong memory access:

```bash
make run_valgrind
```

⚠️ **Warning** : if you use `make run` instead of `make run_debug`, NGINX won't show errors even when they are present. When developing prefer the `run_debug` and `run_gdb` targets.

To debug your code, you should encapsulate your code in functions and put them in the `utils/utils.c` file. A Makefile and a main function are available in the `tests/` folder.

🚨 **Troubleshooting**: 
- If you are still having troubles with the setup, we provide you a script at the root of the project that you can use to fully build the project. Even though this script should work, it is recommended to follow the steps above to understand what is happening. To use the script, simply run the following command in your terminal :

```bash
# Compiling the whole project
bash init_project.sh
```
- If you are seeing weird bugs or crashes, you should check that you **Don't use the `malloc` or `free` functions** from the C standard library. See the project statement for more information.

## Testing the provided server

The server we provide you with is a simple HTTP server that responds with "Hello, World!".

There are multiple ways to generate HTTP requests. Later in the project, you will use [WRK](https://github.com/wg/wrk) to automate traffic generation. For now, we will use [WGET](https://www.gnu.org/software/wget/) to test your server. You can use the following command :

```bash
wget localhost:8888 -q -O -
```

**_NOTE:_**  for some distribution you may need to use wget -4 localhost:8888 -q -O -.

You should see **Hello, World!** appear in your terminal. Dont forget to first run the server with the `make run_debug` command in another terminal.

Feel free to use whatever means you like for sending requests, it is not part of the evaluation (for now :D).

Other solutions can be:

- **[curl](https://gist.github.com/subfuzion/08c5d85437d5d4f00e58)**: another command-based client similar to wget
- **[Insomnia](https://insomnia.rest/)**: An application with a graphical user interface
- **[Postman](https://www.postman.com/)**: Like Insomnia, but it's proprietary software


## Project 1 - Testing your server

For the first evaluation, you will have to modify the provided server and implement the algorithm described statement of the first project (instructions are on Moodle!).

To construct a correct request, we provide you with a [script](student_helper/send_request.sh).

You can use it like this:

```bash
bash ./student_helper/send_request.sh
```

The expected output is:

```bash
5805837,35882937
```

## Project 2 - Performance measurement

### Generate traffic

To measure the performance of your server, you could rely on a script that uses wget to send requests and collects the metrics your are interested in, such as the latency and the throughput. In practice this is not as easy as it sounds. Fortunately there exist tools that can automate that for us. For this project, we will use [WRK2](https://github.com/giltene/wrk2) to generate http traffic. 

WRK can be scripted using [LUA](https://www.lua.org/). The language should be installed by default on recent Ubuntu and Fedora distributions. Don't worry, this language is easy to pick. Small tip: the arrays start at index 1 and not 0, this could be a bit confusing. 

#### Installing WRK

You should install WRK2 by cloning it from [here](https://github.com/giltene/wrk2):

```bash
# From the root of the project
git clone git@github.com:giltene/wrk2.git 
cd wrk2
make
```

We provide you with a [script](project/wrk_scripts/simple_scenario.lua) that you can use to generate traffic for your server. You can run it like this:

```bash
env matsize=64 patterns_size=64 nb_patterns=2 ./wrk2/wrk http://localhost:8888/ -R1024 -s project/wrk_scripts/simple_scenario.lua
```

There are 3 environment variables used to set the factors. `matsize` is the size of the matrix, `patterns_size` is the size of the patterns and `nb_patterns` is the number of patterns. You can change these values to test your server with different configurations. Additionally, you can change the `-R` parameter which sets the number of requests sent per second.   

### Using NPF

During the practicals, you had the opportunity to use [NPF](https://github.com/tbarbette/npf). As a reminder, here are the correct steps to install npf in a private environment:

```bash
# Create a venv
python3 -m venv venv
# Activate the venv
. venv/bin/activate 
# Install npf
pip install npf
```

**If you open another terminal, you will have to activate the venv again.**

For the project, you are free to use any tool you want to automate your scripts. NPF is a good choice because it is easy to use and can be used to generate graphs easily, but using bash or Python scripts is fine too. 