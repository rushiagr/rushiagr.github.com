---
layout: post
title: "Playing around with Cinder multi-backend"
date: 2014-01-16 22:42
comments: true
categories: 
---


With Grizzly release, Cinder got equipped with another major feature -- multi-backends
with filter scheduler. So now you can have more than one storage boxes for block storage
and manage them with one Cinder deployment. Here, I'm going to test it out using our 
favourite method -- trying it out on DevStack!

<!--more-->

DevStack can provide you with two LVM backends to play around with them. But you'll need to restack it.

Go to the devstack directory and pull the latest code. Destroy previous DevStack deployment if it exists.
    rushi@jio:~/devstack$ git pull origin master
    rushi@jio:~/devstack$ ./unstack.sh

Add the config option to `localrc` which give you pre-cooked multi-backend setup with two LVM backends, both of 10G. Stack 
    rushi@jio:~$ echo "CINDER_MULTI_LVM_BACKEND=True" >> localrc
    rushi@jio:~$ ./devstack/stack.sh

You can see that the cinder.conf file now has two values for enabled backends:
    rushi@jio:~$ less /etc/cinder/cinder.conf | grep enabled_backends
    enabled_backends = lvmdriver-1,lvmdriver-2
    #enabled_backends=<None>

Also, you can see that there are two configuration groups created at the end of that config file, one each for configurations
corresponding to that particular backend
    rushi@jio:~$ tail /etc/cinder/cinder.conf 
    
    [lvmdriver-1]
    volume_backend_name = LVM_iSCSI
    volume_driver = cinder.volume.drivers.lvm.LVMISCSIDriver
    volume_group = stack-volumes
    
    [lvmdriver-2]
    volume_backend_name = LVM_iSCSI_2
    volume_driver = cinder.volume.drivers.lvm.LVMISCSIDriver
    volume_group = stack-volumes2


So you have two volume groups created for respective backends. Lets check it directly without using Cinder.
    rushi@jio:~$ sudo vgs
      VG             #PV #LV #SN Attr   VSize   VFree 
      stack-volumes    1   0   0 wz--n-  10.01g 10.01g
      stack-volumes2   1   0   0 wz--n-  10.01g 10.01g
      ubuntu-vg        1   2   0 wz--n- 931.27g 44.00m

Hmmm. Two volume groups, each of size 10G.

### Case 1: Spreading volumes across backends


Now, lets create a volume and see where it ends up.
    rushi@jio:~$ cinder create 1
    ERROR: You must provide a username via either --os-username or env[OS_USERNAME]

Oops! Let me try again..
    rushi@jio:~$ . devstack/openrc 
    rushi@jio:~$ cinder create 1
    +-------------------+--------------------------------------+
    |      Property     |                Value                 |
    +-------------------+--------------------------------------+
    |    attachments    |                  []                  |
    | availability_zone |                 nova                 |
    |      bootable     |                false                 |
    |     created_at    |      2014-01-16T17:29:49.241493      |
    |    description    |                 None                 |
    |         id        | ecfbfebb-73d5-4faf-b625-e69f18020378 |
    |      metadata     |                  {}                  |
    |        name       |                 None                 |
    |        size       |                  1                   |
    |    snapshot_id    |                 None                 |
    |    source_volid   |                 None                 |
    |       status      |               creating               |
    |      user_id      |   e441f49105f343da87316ab7157e2ab7   |
    |    volume_type    |                 None                 |
    +-------------------+--------------------------------------+

    rushi@jio:~$ cinder list
    +--------------------------------------+-----------+------+------+-------------+----------+-------------+
    |                  ID                  |   Status  | Name | Size | Volume Type | Bootable | Attached to |
    +--------------------------------------+-----------+------+------+-------------+----------+-------------+
    | ecfbfebb-73d5-4faf-b625-e69f18020378 | available | None |  1   |     None    |  false   |             |
    +--------------------------------------+-----------+------+------+-------------+----------+-------------+

    rushi@jio:~$ sudo vgs
      VG             #PV #LV #SN Attr   VSize   VFree 
      stack-volumes    1   0   0 wz--n-  10.01g 10.01g
      stack-volumes2   1   2   0 wz--n-  10.01g  9.01g
      ubuntu-vg        1   2   0 wz--n- 931.27g 44.00m

So it went to backend number 2. If you are admin (`source devstack/openrc admin admin`), you can do a `cinder show` too, to get information 
as to which host did this volume go to. Only the admin is allowed to view the host information.

The scheduler now gets reported of the capabilities which the backends have (check out the `c-shr` screen to see it). The scheduler then weighs the backend based on these capabilities and decides which of them has higher 'weight' to serve the next 'create' request. By default, the 'weigher' for scheduler is `CapacityWeigher`. That is, whichever backend has higher capacity, that backend will be chosen for the next 'create' request.

So in our case, when we'll do another 'create volume' it will now land on to the first backend.
    rushi@jio:~$ cinder create 1
    +-------------------+--------------------------------------+
    |      Property     |                Value                 |
    +-------------------+--------------------------------------+
    |    attachments    |                  []                  |
    | availability_zone |                 nova                 |
    |      bootable     |                false                 |
    |     created_at    |      2014-01-16T17:39:23.958468      |
    |    description    |                 None                 |
    |         id        | aa79c608-47cc-44e3-a614-f4bddaab68e5 |
    |      metadata     |                  {}                  |
    |        name       |                 None                 |
    |        size       |                  1                   |
    |    snapshot_id    |                 None                 |
    |    source_volid   |                 None                 |
    |       status      |               creating               |
    |      user_id      |   e441f49105f343da87316ab7157e2ab7   |
    |    volume_type    |                 None                 |
    +-------------------+--------------------------------------+

    rushi@jio:~$ sudo vgs
      VG             #PV #LV #SN Attr   VSize   VFree 
      stack-volumes    1   0   0 wz--n-  10.01g  9.01g
      stack-volumes2   1   2   0 wz--n-  10.01g  9.01g
      ubuntu-vg        1   2   0 wz--n- 931.27g 44.00m

Neat!

### Case 2 : Stacking all volumes at one backend

What if we want to keep all the volumes at only one backend? Cinder allows you to do that too!
There is a configuration option in cinder.conf, `capacity_weight_multiplier`, which allows you to multiply the 'capacity weight' by a number.
So if the multiplier is 1, a backend with higher capacity will have higher weight, and will be the choice for the next volume creation request.
This is the default case. BUT what if we set it to -1? The backend with higher available capacity will have more negative weight, which will make that backend less preferable for next 'create' request, and hence the request will go to the backend which has lesser capacity!

Let us see this too in action.

Check out the config option from cinder.conf file. 
    rushi@jio:~$ cat /etc/cinder/cinder.conf | grep -B 3 ^capacity_weight_multiplier
    
    # Multiplier used for weighing volume capacity. Negative
    # numbers mean to stack vs spread. (floating point value)
    # capacity_weight_multiplier=1.0

The config option is commented out and is there just so that you can easily change it. Now uncomment it and change it's value to -1.

Delete previously created volumes. Kill all the three Cinder screen processes (`c-api`, `c-sch` and `c-vol`), and restart them.

Lets create two volumes and see where they end up..
    rushi@jio:~$ cinder list
    +----+--------+------+------+-------------+----------+-------------+
    | ID | Status | Name | Size | Volume Type | Bootable | Attached to |
    +----+--------+------+------+-------------+----------+-------------+
    +----+--------+------+------+-------------+----------+-------------+
    rushi@jio:~$ cinder create 1
    +-------------------+--------------------------------------+
    |      Property     |                Value                 |
    +-------------------+--------------------------------------+
    |    attachments    |                  []                  |
    | availability_zone |                 nova                 |
    |      bootable     |                false                 |
    |     created_at    |      2014-01-16T17:56:59.845733      |
    |    description    |                 None                 |
    |         id        | b927b328-5ae0-411a-9de2-22ed732b4946 |
    |      metadata     |                  {}                  |
    |        name       |                 None                 |
    |        size       |                  1                   |
    |    snapshot_id    |                 None                 |
    |    source_volid   |                 None                 |
    |       status      |               creating               |
    |      user_id      |   e441f49105f343da87316ab7157e2ab7   |
    |    volume_type    |                 None                 |
    +-------------------+--------------------------------------+
    rushi@jio:~$ cinder create 1
    +-------------------+--------------------------------------+
    |      Property     |                Value                 |
    +-------------------+--------------------------------------+
    |    attachments    |                  []                  |
    | availability_zone |                 nova                 |
    |      bootable     |                false                 |
    |     created_at    |      2014-01-16T17:57:01.132756      |
    |    description    |                 None                 |
    |         id        | 9f643f2d-7221-4a5c-bf48-1977c9b89fd3 |
    |      metadata     |                  {}                  |
    |        name       |                 None                 |
    |        size       |                  1                   |
    |    snapshot_id    |                 None                 |
    |    source_volid   |                 None                 |
    |       status      |               creating               |
    |      user_id      |   e441f49105f343da87316ab7157e2ab7   |
    |    volume_type    |                 None                 |
    +-------------------+--------------------------------------+

    rushi@jio:~$ sudo vgs
      VG             #PV #LV #SN Attr   VSize   VFree 
      stack-volumes    1   0   0 wz--n-  10.01g 10.01g
      stack-volumes2   1   2   0 wz--n-  10.01g  8.01g
      ubuntu-vg        1   2   0 wz--n- 931.27g 44.00m

:)

### Case 3 : Custom choice

What if I have two different backends (maybe one is slower, or costlier, than the other), and my users want to exactly specify how many volumes they want of each 'type' of backends? Here, Cinder's 'volume types' have us covered. 

We can associate a volume type with a backend, and then the users can create a volume of whatever 'type' they want.
Let's throw some discrimination at these backends. I'll create two volume types: 'gold' and 'bronze', and associate 'stack-volumes' with 'gold' and similarly for 'stack-volumes2'. Note that this job can only be done by the administrator.

Let us be admins
    rushi@jio:~$ . devstack/openrc admin admin

Create both the volume types and list them.
    rushi@jio:~$ cinder type-create gold
    +--------------------------------------+------+
    |                  ID                  | Name |
    +--------------------------------------+------+
    | dd883ee0-24be-42e1-ab2e-b9a01454f2f9 | gold |
    +--------------------------------------+------+
    rushi@jio:~$ cinder type-create bronze
    +--------------------------------------+--------+
    |                  ID                  |  Name  |
    +--------------------------------------+--------+
    | f63dd2cb-f4e7-4d6d-a84f-5bf2cc6c5671 | bronze |
    +--------------------------------------+--------+
 
    rushi@jio:~$ cinder type-list
    +--------------------------------------+--------+
    |                  ID                  |  Name  |
    +--------------------------------------+--------+
    | dd883ee0-24be-42e1-ab2e-b9a01454f2f9 |  gold  |
    | f63dd2cb-f4e7-4d6d-a84f-5bf2cc6c5671 | bronze |
    +--------------------------------------+--------+

Get the backend names (`volume_backend_name` config option) from cinder.conf file.
    rushi@jio:~$ tail /etc/cinder/cinder.conf 
    
    [lvmdriver-1]
    volume_backend_name = LVM_iSCSI
    volume_driver = cinder.volume.drivers.lvm.LVMISCSIDriver
    volume_group = stack-volumes
    
    [lvmdriver-2]
    volume_backend_name = LVM_iSCSI_2
    volume_driver = cinder.volume.drivers.lvm.LVMISCSIDriver
    volume_group = stack-volumes2


Now let's associate backend `LVM_iSCSI` with volume type 'gold', and similarly for the other one.
    rushi@jio:~$ cinder type-key gold set volume_backend_name=LVM_iSCSI
    rushi@jio:~$ cinder type-key bronze set volume_backend_name=LVM_iSCSI_2

These association are stored as key-value pairs in the volume type's 'extra specs'. Let's see them
    rushi@jio:~$ cinder extra-specs-list 
    +--------------------------------------+--------+------------------------------------------+
    |                  ID                  |  Name  |               extra_specs                |
    +--------------------------------------+--------+------------------------------------------+
    | dd883ee0-24be-42e1-ab2e-b9a01454f2f9 |  gold  |  {u'volume_backend_name': u'LVM_iSCSI'}  |
    | f63dd2cb-f4e7-4d6d-a84f-5bf2cc6c5671 | bronze | {u'volume_backend_name': u'LVM_iSCSI_2'} |
    +--------------------------------------+--------+------------------------------------------+


You can add more key-value pairs for these volume types with different key names. `volume_backend_name` is a reserved key name, though.

Let's create two volumes of type 'gold' and see where they end up being created:
    rushi@jio:~$ cinder create --volume-type gold --name costly_vol_1 1
    +-------------------+--------------------------------------+
    |      Property     |                Value                 |
    +-------------------+--------------------------------------+
    |    attachments    |                  []                  |
    | availability_zone |                 nova                 |
    |      bootable     |                false                 |
    |     created_at    |      2014-01-16T18:24:07.670635      |
    |    description    |                 None                 |
    |         id        | 767d4c56-6d3d-46f7-b0a3-4a00f696bcad |
    |      metadata     |                  {}                  |
    |        name       |             costly_vol_1             |
    |        size       |                  1                   |
    |    snapshot_id    |                 None                 |
    |    source_volid   |                 None                 |
    |       status      |               creating               |
    |      user_id      |   c271eb32e71b411bb98ad7b93792d6d5   |
    |    volume_type    |                 gold                 |
    +-------------------+--------------------------------------+
    rushi@jio:~$ cinder create --volume-type gold --name costly_vol_2 1
    +-------------------+--------------------------------------+
    |      Property     |                Value                 |
    +-------------------+--------------------------------------+
    |    attachments    |                  []                  |
    | availability_zone |                 nova                 |
    |      bootable     |                false                 |
    |     created_at    |      2014-01-16T18:24:58.382180      |
    |    description    |                 None                 |
    |         id        | a938e556-65cf-4547-87ff-513d60f626d3 |
    |      metadata     |                  {}                  |
    |        name       |             costly_vol_2             |
    |        size       |                  1                   |
    |    snapshot_id    |                 None                 |
    |    source_volid   |                 None                 |
    |       status      |               creating               |
    |      user_id      |   c271eb32e71b411bb98ad7b93792d6d5   |
    |    volume_type    |                 gold                 |
    +-------------------+--------------------------------------+
    rushi@jio:~$ cinder list
    +--------------------------------------+-----------+--------------+------+-------------+----------+-------------+
    |                  ID                  |   Status  |     Name     | Size | Volume Type | Bootable | Attached to |
    +--------------------------------------+-----------+--------------+------+-------------+----------+-------------+
    | 767d4c56-6d3d-46f7-b0a3-4a00f696bcad | available | costly_vol_1 |  1   |     gold    |  false   |             |
    | a938e556-65cf-4547-87ff-513d60f626d3 | available | costly_vol_2 |  1   |     gold    |  false   |             |
    +--------------------------------------+-----------+--------------+------+-------------+----------+-------------+

    rushi@jio:~$ sudo vgs
      VG             #PV #LV #SN Attr   VSize   VFree 
      stack-volumes    1   2   0 wz--n-  10.01g  8.01g
      stack-volumes2   1   0   0 wz--n-  10.01g 10.01g
      ubuntu-vg        1   2   0 wz--n- 931.27g 44.00m

Now create another one, but with type 'bronze' and ensure it is created on the other backend.
    rushi@jio:~$ cinder create --volume-type bronze --name cheap_vol_1 1
    +-------------------+--------------------------------------+
    |      Property     |                Value                 |
    +-------------------+--------------------------------------+
    |    attachments    |                  []                  |
    | availability_zone |                 nova                 |
    |      bootable     |                false                 |
    |     created_at    |      2014-01-16T18:27:05.852092      |
    |    description    |                 None                 |
    |         id        | 97f62c7a-b974-41e8-a659-1e6d3eb876d5 |
    |      metadata     |                  {}                  |
    |        name       |             cheap_vol_1              |
    |        size       |                  1                   |
    |    snapshot_id    |                 None                 |
    |    source_volid   |                 None                 |
    |       status      |               creating               |
    |      user_id      |   c271eb32e71b411bb98ad7b93792d6d5   |
    |    volume_type    |                bronze                |
    +-------------------+--------------------------------------+

    rushi@jio:~$ sudo pvs
      PV         VG             Fmt  Attr PSize   PFree 
      /dev/loop0 stack-volumes  lvm2 a--   10.01g  8.01g
      /dev/loop1 stack-volumes2 lvm2 a--   10.01g  9.01g
      /dev/sda5  ubuntu-vg      lvm2 a--  931.27g 44.00m


Done :)

Cheers!
