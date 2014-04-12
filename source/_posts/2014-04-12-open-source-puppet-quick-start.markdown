---
layout: post
title: "Open Source Puppet - Quick Start"
date: 2014-04-12 20:18
comments: true
categories: [tech, cheatsheet, automation, cloud]
---

This post aims to be your quickest guide to get started with Puppet. We'll be using the open source version of Puppet. An hour of spare time and two Ubuntu machines (physical or virtual doesn't matter) is all that is needed.

## Quick Introduction
Lets say you want to install and run apache server on one of the machines in your lab. On another, you want to create a new user. On a third machine, you want to install MySQL, and allow access to this machine only from the first server. Seems like a lot of manual work isn't it? The power of Puppet is, you can specify all these tasks in a file, called 'Puppet manifest', and then execute it. Everything will be set up for you just as you wanted! Now what makes this 'I care about the end result, not the process' approach really powerful is you can 'apply' this manifest over and over again to get the same end result. You can easily modify this manifest file, extend it, and manage it under version control, just like you would with a piece of software. Welcome to the world of IT automation :)

Although the syntax of a Puppet manifest is Ruby-ish, no knowledge of Ruby is required at all (I don't know Ruby).

There is a whole lot of things you can do with Puppet. Here, we'll just get us started with it. Once you are through this post, you can head over to Puppet Labs' documents and tutorials, for more on "how"s and "why"s of Puppet.


## Setup
You just require two Ubuntu machines connected to each other. One will be the Puppet 'master' node (the machine which will take care of managing the configuration and state of all the machines in our deployment), the other one 'slave' (which unfortunately is the only actual machine in demo deployment :) ). 

Here I am using two  virtual machines, but you can create one virtual machine and use your host machine as the other one. The hostnames of the master and slave in my setup are `puppet-master` and `puppet-agent`.

Make sure both the machines are ping-able from each other -- by their IP as well as hostnames (e.g. `ping 123.123.123.123` and `ping puppet-master`). Make sure your /etc/hosts file looks something like this to achieve that: 

(`192.168.56.130` and `192.168.56.131` are the IP addresses of externally-visible interfaces of hosts `puppet-master` and `puppet-agent` respectively)

Master: 

	r@puppet-master:~$ cat /etc/hosts
	127.0.0.1	localhost
	127.0.1.1	puppet-master
	
	192.168.56.131	puppet-agent


Slave: 
	r@puppet-agent:~$ cat /etc/hosts
	127.0.0.1	localhost
	127.0.1.1	puppet-agent
	
	192.168.56.130	puppet-master



## Getting the hands dirty -- Puppet CLI
Install `puppetmaster` package on the master node
	sudo apt-get install puppetmaster


List all the users on the current system:
	puppet resource user --list

So basically a 'user' is a 'resource' in Puppet terminology. Now only list a specific resource. `r` is the current user in my case.
	r@puppet-master:~$ puppet resource user r
	user { 'r':
	  ensure  => 'present',
	  comment => 'r,,,',
	  gid     => '1000',
	  groups  => ['adm', 'cdrom', 'sudo', 'dip', 'plugdev', 'lpadmin', 'sambashare'],
	  home    => '/home/r',
	  shell   => '/bin/bash',
	  uid     => '1000',
	}

Notice the syntax. Resource 'r' is of type 'user', with 'ensure', 'comment', etc as keys/attributes, and 'present', 'r,,,' as values for those attributes.

You can change the value using the Puppet CLI
	r@puppet-master:~$ sudo puppet resource user r comment='some text missing'
	notice: /User[r]/comment: comment changed 'r,,,' to 'some text missing'
	user { 'r':
	  ensure  => 'present',
	  comment => 'some text missing',
	}

Create a new user with specified key-value pairs

	r@puppet-master:~$ sudo puppet resource user katie ensure=present shell=/bin/bash
	notice: /User[katie]/ensure: created
	user { 'katie':
	  ensure => 'present',
	  shell  => '/bin/bash',
	}
	r@puppet-master:~$ sudo puppet resource user katie 
	user { 'katie':
	  ensure           => 'present',
	  gid              => '1001',
	  home             => '/home/katie',
	  password         => '!',
	  password_max_age => '99999',
	  password_min_age => '0',
	  shell            => '/bin/bash',
	  uid              => '1001',
	}


Remove the newly created user, but this time, let's put this information into a file `katie_remove.pp` and ask Puppet to 'apply' this file and thus removing the user 'katie'.
	r@puppet-master:~$ cat katie_remove.pp 
	user {'katie':
	    ensure => absent,
	}

Apply this Puppet manifest
	r@puppet-master:~$ sudo puppet apply katie_absent.pp 
	warning: Could not retrieve fact fqdn
	notice: /Stage[main]//User[katie]/ensure: removed
	notice: Finished catalog run in 0.47 seconds

Puppet's description of user 'katie':
	r@puppet-master:~$ sudo puppet resource user katie
	  user { 'katie':
	  ensure => 'absent',
	}

is now same as that of a non-existent user. 
	r@puppet-master:~$ sudo puppet resource user absent-user
	  user { 'absent-user':
	  ensure => 'absent',
	}

That is, the user 'katie' is now deleted. You can see that the 'ensure' attribute can be used to make sure a user (or in general, any 'resource', is present, or absent).

**Note**: Ignore the warning which is printed while applying a manifest from a file. Or if you are bothered by it popping up all the time, in the `/etc/hosts` file, change
	127.0.1.1	puppet-master
to
	127.0.1.1	puppet-master.rushiagr.com puppet-master
where you can choose a domain name of your own choice in place of `.rushiagr.com`.

## Puppet modules
**Note:** `puppet module` doesn't work on Precise (Ubuntu 12.04). You need to install ruby, and gems, etc. Too much of a hassle. So I'll just post commands here which work for a higher version of Ubuntu.

Install standard library:
	sudo puppet module install puppetlabs/stdlib

View all the installed modules
	r@puppet-master:~$ sudo puppet module list
	/etc/puppet/modules
	├── puppetlabs-mysql (v2.2.1)
	├── puppetlabs-ntp (v3.0.2)
	└── puppetlabs-stdlib (v4.1.0)
	/usr/share/puppet/modules (no modules installed)

All the modules, and all other information in the system goes in `/etc/puppet` directory.

**Note**: Modules installed via `sudo` will be visible when you perform `puppet module list` with `sudo` only. Same for non-`sudo` use.


## Puppet in master-client configuration
Everything we did so far concerned with a single machine. Let's now introduce another machine -- Puppet agent.

Note that you need to set FQDNs for both the machines. See the step above, where we suppressed a warning.

First, we'll need to install `puppet` package (the agent) on the agent node.
	sudo apt-get install puppet

By default, the Puppet agent service will not be running.
	r@puppet-agent:~$ sudo service puppet status
	 * agent is not running

Before starting it, change `START=no` to `START=yes` in `/etc/default/puppet` file, to start the agent service by default when the system starts/reboots.

	sudo sed -i s/START=no/START=yes/g /etc/default/puppet 

And add these two lines at the end of `/etc/puppet/puppet.conf` to allow the agent to discover the master by its FQDN.

	[agent]
	server = puppet-master

Now start the Puppet agent service

	r@puppet-agent:~$ sudo service puppet start
	 * Starting puppet agent                                                       [ OK ] 

I also make sure that clocks of both the machines are synchronized by running `ntpdate` on both master and slave. I am not sure if this is required, but doesn't do any harm.
	sudo ntpdate pool.ntp.org

Now the master needs to sign the certs by agent.

Execute this command on agent node.
	sudo puppet agent --test --waitforcert 60

Now hop over to the master node, and retrieve the list of certs waiting to be signed
	r@puppet-master:~$ sudo puppet cert --list
	  "puppet-agent.rushiagr.com" (EB:0F:E4:14:6F:B2:7E:85:7E:21:26:C4:78:80:58:E1)

Sign the cert
	r@puppet-master:~$ sudo puppet cert sign puppet-agent.rushiagr.com
	notice: Signed certificate request for puppet-agent.rushiagr.com
	notice: Removing file Puppet::SSL::CertificateRequest puppet-agent.rushiagr.com at '/var/lib/puppet/ssl/ca/requests/puppet-agent.rushiagr.com.pem'

Now we are ready to go. Let's create a file ('Puppet manifest') on master where we write that: 1. We want apache package to be installed. 2. Once we ensure that the package is installed, we want to start the apache service. We'll name the file `site.pp`, which is the 'main' configuration file for Puppet. We'll put it into `/etc/puppet/manifests` directory. Note how we can specify a dependency between resources.


	package { 'apache2':
	    ensure => installed
	}
	
	service { 'apache2':
	    ensure => true,
	    enable => true,
	    require => Package['apache2']
	}       

Puppet works on 'push' model, meaning configurations are pulled by agents at periodic intervals. I think the default periodic interval is 30 minutes. Alternatively, you can pull from agent at your own will, any time. Let's do that now. Execute this command on the agent:
	r@puppet-agent:~$ sudo puppet agent --test
	info: Caching catalog for puppet-agent.rushiagr.com
	info: Applying configuration version '1397343482'
	notice: /Stage[main]//Package[apache2]/ensure: ensure changed 'purged' to 'present'
	notice: Finished catalog run in 6.30 seconds

And you can see the apache server running!
	r@puppet-agent:~$ sudo service apache2 status
	Apache2 is running (pid 5874).

Ta! Da!

Please comment if you have any ideas to make this post easier for the newbies to understand.

Cheers!

**Notes:**

This is just a quick start guide. There are excellent resources and docs at [puppetlabs.com](http://puppetlabs.com). I have their beginner's [PDF](https://dl.dropboxusercontent.com/u/42084476/OpenStack/learningpuppet.pdf) saved in my DropBox. 
Around 80 pages long, it covers almost every aspect of basic Puppet. The only problem with this guide is it is (I think deliberately) made to work only with the Enterprise Puppet version, but you can always refer back to this post to know how to set the open source version :)

If you mess up the cert signing process, here is a quick and dirty way to get it resolved. On master:

    sudo puppet cert clean puppet-agent.rushiagr.com
On both master and slave:
    sudo rm -r /var/lib/puppet/ssl 
    sudo service puppet restart



