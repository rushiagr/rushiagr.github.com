---
layout: post
title: "OpenStack Tempest quick start with DevStack"
date: 2013-03-20 04:54
comments: true
categories: tech
---

This quick start guide explains setting up Tempest with a DevStack environment
for Grizzly release. Most of the information here is taken from
[here](http://www.joinfu.com/2012/03/testing-essex-rc1-with-devstack-and-tempest/), the only difference being this blog post is more recent, and is based on Grizzly.

<!--more-->

Assumptions made are that you understand:
1. What is a `localrc` file in DevStack.
2. What does `./stack.sh` do in DevStack.
3. How to clone using git.

##Setting up DevStack

Clone DevStack
    git clone https://github.com/openstack-dev/devstack.git
    cd devstack

Tempest requires that the rate-limiting for DevStack is turned off. By default, it is turned on, so turn it off by adding this line to the localrc file.
    API_RATE_LIMIT=False

If you have already created a DevStack environment, you will have to go through the labour of setting it all again by unstacking and restacking it with this parameter in localrc.
Quick tip: If you already had a working DevStack in your computer, adding `OFFLINE=True` line in localrc will create the DevStack environment in your computer WITHOUT
downloading all the OpenStack code all over again from the Github repos, but will build the environment from the existing code (thus saving you some Internet bandwidth and time).

Build the DevStack environment
    ./stack.sh
Supply all the five passwords. (If you are just playing around, just like me, then
you can easily supply `nova` to all the passwords.)


Note the IP of the system where DevStack is running (The 'host IP' mentioned at the last of the output after running `stack.sh`).

##Setting up Tempest

Clone latest Tempest code
    git clone https://github.com/openstack/tempest.git
    cd tempest

Create tempest.conf file from the sample configuration file. This file will contain the configuration information of the OpenStack environment (here, the DevStack
environment)
    cp etc/tempest.conf.sample etc/tempest.conf

Now open the file tempest.conf in an editor, and replace all instance of word `secret` with the appropriate password (`nova` if you followed me, and just typed `nova` whenever the
`stack.sh` script asked for passwords)

If, for example, your host IP is 10.0.24.30, change this line in tempest.conf 
    uri = http://127.0.0.1:5000/v2.0/
to make it
    uri = http://10.0.24.30:5000/v2.0/

The last thing to update in the tempest.conf file is the ID of the Cirros image. The image ID can be obtained by two ways
####Image ID using glance
This command will return the image ID. Note that I have used the password `nova` in this line. You might also need to change the host IP address
    glance -I admin -K nova -T admin -N http://10.0.24.30:5000/v2.0 -S keystone index | grep ami | cut -f1 | awk '{print $1}'
####Image ID using OpenStack CLI
Become stack user
    su - stack
Source the sample credentials file
    . /opt/stack/devstack/eucarc
OR
    . /opt/stack/devstack/openrc
Show all the images, with their IDs
    $ nova image-list
    +--------------------------------------+---------------------------------+--------+--------+
    | ID                                   | Name                            | Status | Server |
    +--------------------------------------+---------------------------------+--------+--------+
    | 13abf9c8-5603-48cb-802e-e27162e10b58 | cirros-0.3.0-x86_64-uec         | ACTIVE |        |
    | 39b023ae-9201-427d-8350-4f30e5bbc01a | cirros-0.3.0-x86_64-uec-kernel  | ACTIVE |        |
    | 431a9c04-47b1-47e4-9521-7f12295c78e0 | cirros-0.3.0-x86_64-uec-ramdisk | ACTIVE |        |
    +--------------------------------------+---------------------------------+--------+--------+
The ID of the smallest image name is what we're interested in.

Now replace `{$IMAGE_ID}` and `{$IMAGE_ID_ALT}` with this value, to make those two lines appear in tempest.conf as
    image_ref = 13abf9c8-5603-48cb-802e-e27162e10b58
    image_ref_alt = 13abf9c8-5603-48cb-802e-e27162e10b58

##Installing required dependencies
Install all the required packages needed to run Tempest integration test suite. (The list of required packages is maintained in file `tools/pip-requires`)
    $ sudo pip install -r tools/pip-requires 

##Show time!
We'll run all the tests in verbose mode. To run all the tests:
    nosetests -v tempest
To run tests only from a specific file, say `tempest/tests/volume/test_volumes_list.py`:
    nosetests -sv tempest.tests.volume.test_volumes_list
OR
    nosetests -sv tempest.tests.volume.test_volumes_list.py
To run a specific test `test_volume_list_with_details` from test class `VolumeListTest`, which resides in the above file:
        nosetests -sv tempest.tests.volume.test_volumes_list:VolumeListTest.test_volume_list_with_details
        

And that ladies and gentlemen, is the end! :)
