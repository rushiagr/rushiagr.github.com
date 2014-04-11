---
layout: post
title: "OpenStack in an hour with DevStack"
date: 2014-04-03 22:01
comments: true
categories: [tech, openstack, cloud]
---

So you found out a cool new technology "OpenStack" and want to try it real quick? Or probably you are hired in a company for your Python skills and now you are supposed to work on OpenStack in the shortest possible time? Fear not, it is not that hard to get started. [DevStack](http://devstack.org) is your friend-in-need. No, don't click that hyperlink just yet :)


<!--more-->

To put it in a sentence, DevStack is "OpenStack in a box". You just need a popular Linux based distribution with 2GB RAM and you're all set to start. DevStack is basically a set of scripts which will install all the important OpenStack services in your computer. For this, it will first download all the essential packages, pull in the OpenStack code from various OpenStack projects, and set everything up for you to try out all of it.


NOTE: DO NOT set up DevStack for production clouds.

Here, in this tutorial, I'll be setting up DevStack in a 64-bit Ubuntu 12.04 virtual machine. All your virtual machine needs to have is an Internet connection, and 2GB RAM.

NOTE: Do not run any of the script as a root user, unless specified otherwise explicitly.

### Getting started
Install git
	sudo apt-get install git

Clone the DevStack repository into your computer and `cd` into it. This is the code which will set up the cloud for you.
	git clone http://github.com/openstack-dev/devstack
	cd devstack/

If you do a `ls`, you will see `stack.sh`, `unstack.sh` and `rejoin-stack.sh` files in there. These are the most important files.
	r@ra:~/devstack$ ls
	accrc         exercises         HACKING.rst  rejoin-stack.sh  tests
	AUTHORS       exercise.sh       lib          run_tests.sh     tools
	clean.sh      extras.d          LICENSE      samples          unstack.sh
	driver_certs  files             localrc      stackrc
	eucarc        functions         openrc       stack-screenrc
	exerciserc    functions-common  README.md    stack.sh

File `stack.sh` is the most important of them all. Running this script will:
1. Pull OpenStack code from all of it's important projects' repositories and put them in `/opt/stack` directory. TODO: say that this directory is configurable.
2. Installs all the dependencies these OpenStack projects have -- both in the form of Ubuntu packages, and also the Python "PIP" repositories.
3. Starts all the OpenStack services with a default configuration.

Bringing down the DevStack-created cloud is easy too -- just invoke the `unstack.sh` script, and all the services are down again, freeing up the memory that these services consume. I'll talk about `rejoin-stack.sh` in some time. Let's get started before I start writing at lengths again :)


Execute the `stack.sh` script
	r@ra:~/devstack$ ./stack.sh 
	
	################################################################################
	ENTER A PASSWORD TO USE FOR THE DATABASE.
	################################################################################
	This value will be written to your localrc file so you don't have to enter it 
	again.  Use only alphanumeric characters.
	If you leave this blank, a random default value will be used.
	Enter a password now:

You need to add the MySQL database password here. Don't worry if you have not installed MySQL on this system. Just provide a password here and this script will install MySQL and use this password there.

As you can see, MySQL is where all the important data is stored by different OpenStack components. You can peep into the database later if you want to see what data is stored, etc.

Also, note the first line after the heading. If the `stack.sh` script finishes successfully, all the inputs you specify (this, and four more after this) will be written to a file named as `localrc`. All the local configuration setting pertaining to the DevStack environment will go in this file. I'll provide you with details of all of them very soon. Have patience :)

For the other four prompts, enter 'nova'. Just use 'nova' for this MySQL prompt too if it is not installed yet.

You will see that the script now starts spewing a lot of output on our screen. It is downloading all the required code, packages, dependencies, etc, and setting everything up for us -- databases, services, network, configurations, message queues. Pretty much everything. For the first time, the script might take about 30-minutes, but it again depends upon the speed of your Internet connection, and the processing speed of your virtual machine. From the next time, it can provide you with a cloud in less than 10 minutes!

If the script ends with something like this:
	+ merge_config_group /home/r/devstack/local.conf post-extra
	+ local localfile=/home/r/devstack/local.conf
	+ shift
	+ local matchgroups=post-extra
	+ [[ -r /home/r/devstack/local.conf ]]
	+ return 0
	+ [[ -x /home/r/devstack/local.sh ]]
	+ service_check
	+ local service
	+ local failures
	+ SCREEN_NAME=stack
	+ SERVICE_DIR=/opt/stack/status
	+ [[ ! -d /opt/stack/status/stack ]]
	++ ls '/opt/stack/status/stack/*.failure'
	++ /bin/true
	+ failures=
	+ '[' -n '' ']'
	+ set +o xtrace
	
	
	
	Horizon is now available at http://10.0.2.15/
	Keystone is serving at http://10.0.2.15:5000/v2.0/
	Examples on using novaclient command line is in exercise.sh
	The default users are: admin and demo
	The password: nova
	This is your host ip: 10.0.2.15
	stack.sh completed in 269 seconds.

That means your machine is now home to a Cloud! :)

Here, `10.0.2.15` is the IP of my first network interface. Don't worry about that for now.

So now you can head over to my blog [Cinder on DevStack - Quick Start](http://www.rushiagr.com/blog/2013/05/27/cinder-on-devstack-quick-start/) to get started with creating volumes (persistent storage in cloud) with Cinder -- OpenStack's block-storage project. In that guide, you will also be creating a virtual machine, so it will be a good start to OpenStack. But let's get back in our current scope.

You can type the host IP provided by the script into your browser, to access the dashboard 'Horizon'. Log into it using username 'admin', or 'demo' and password 'nova'. (For simplicity's sake, lets just assume there are two users who are allowed to access this cloud -- one has all the administrative privilages, and the other one is just a normal user).

You can view all the process logs inside screen, by typing:
	screen -x

Head over to [Linux Screens in DevStack](http://www.rushiagr.com/blog/2013/06/05/linux-screens-in-devstack/) for more information on how to work with `screen`.

### Housekeeping and customizations
In your life as an OpenStack developer, you will be setting up and destroying DevStack instance quite a number of times. So it is good to know how to do that in the most efficient manner.

Just like `stack.sh` script is used to set up DevStack, `unstack.sh` is used to destroy the DevStack setup. Running it will kill all the services, BUT it will not delete any of the code. If you want to bring down all the services manually, just do a:
	sudo killall screen

Note that this will just kill all the process which were running, for which you were able to see the logs inside screen. `unstack.sh` does some cleanups as well along with killing processes.


If you had previously run `./stack.sh`, but have brought down the environment, you can bring it up back by executing the `rejoin_stack.sh` script.

NOTE: DevStack environment doesn't persist across reboots!

So you need to bring back up the DevStack environment manually everytime you reboot. Here is where using a virtual machine comes handy. You can take a snapshot of the virtual machine, and then go back to it when you want a clean DevStack environment.

Nonetheless, the best way to reboot is: first execute `unstack.sh` to bring down the current running DevStack instance. Then reboot, and when your machine comes up again, run `rejoin_stack.sh`. If you don't run `unstack.sh`, you will need to execute `stack.sh` again to have the environment up.

### localrc configurations
`localrc` is the file where all the local configurations (local = your local machine) are kept.

After first successful `stack.sh` run, will see that a localrc file gets created with the configuration values you specified while running that script.
	$ cat localrc 
	DATABASE_PASSWORD=nova
	RABBIT_PASSWORD=nova
	SERVICE_TOKEN=nova
	SERVICE_PASSWORD=nova
	ADMIN_PASSWORD=nova


Sometimes you will forget to unstack, and will reboot the machine. And then you will find that running `stack.sh` will again do an `apt-get update`, and check for all packages, etc. 

If you specify an option `OFFLINE=True` in a file named `localrc`, inside the devstack directory, and if after specifying this you run `stack.sh`, it will not check anything over the Internet, and will set up DevStack using all the packages and code residing in your machine. Setting up a DevStack using this config option will give you a running cloud in the shortest amount of time (after `rejoin_stack.sh`, but you have already forgotten to do `unstack.sh`, right :) ).


Note that `stack.sh` will see if the git repositories of the OpenStack projects are present in `/opt/stack/` directory. If they are, it will not fetch any latest code into them from Github. But if any of the directory (say, `nova`), is absent, it will pull latest code into the newly created `nova` directory inside `/opt/stack`.

What if you want to get the latest code into all the OpenStack repositories inside `/opt/stack`? Just specify a `RECLONE=yes` parameter in localrc, and rerun `./stack.sh`. This comes particularly handy when you are developing new code. 

NOTE: Keep in mind that while developing code, you need to **commit your local changes** in, say, `/opt/stack/nova` repository, before you restack (re-run `stack.sh`) with `RECLONE=yes` option, as otherwise, the changes will be wiped off. Save yourself from a rude shock. You have been warned.

Configuration options `RECLONE=yes` and `OFFLINE=True` are complementary, and hence, use only one of them at a time in `localrc`.

If you have more than one interfaces, you can specify which one to use for external IP using this configuration:
	HOST_IP=192.168.xxx.xxx


### Developing code
If you want to immediately test out your code by running it inside DevStack, you need to make the changes in the code, and restart the affected services.

For example, let us say you are making code changes in `nova`. Just after you are done making the changes, go to the screen, and restart all the services which start with "n-". If you are very sure that only one of the Nova service is affected, just restart that. Or if you don't know which one to restart, it is safe to restart all of them.

In order to restart, go to the respective screen and press `CTRL`+`C`. Then, press the up arrow once to get the last command which started this screen session, and then press `ENTER`.


### Final words
Note that this guide just gets you started with OpenStack using DevStack. OpenStack, and cloud in general, is not about virtual machines or volumes or networks only. It is a philosophy. It is a complete paradigm shift, and as such, it is impossible to cover all of it by me. Your quest to know more about it has just started. Keep reading more and more about it and I guarantee you you will be fascinated by it's limitless possibilities.

This post is written keeping in mind that it will be consumed by a newbie to OpenStack development. If you are one of the one benefitting from this guide, I would love it if you can provide me with suggestions to improve this post, and any feedback you have about it.

Now you can go to the [DevStack](http://devstack.org) website :)

Cheers!
Rushi
