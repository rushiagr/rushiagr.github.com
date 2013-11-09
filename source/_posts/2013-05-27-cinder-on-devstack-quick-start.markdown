---
layout: post
title: "Cinder on DevStack - Quick Start"
date: 2013-05-27 22:33
comments: true
categories: OpenStack, DevStack, tech, Cinder
---

This blog post covers all the important commands for OpenStack Cinder - The block storage project.
Although this guide is written based on DevStack, it will work with actual deployment of OpenStack
cloud also (except the DevStack/Linux specific bits).

<!--more-->

All the Cinder operations can be performed via either of these three means:

1. CLI (Cinder's `python-cinderclient` command line module)
2. GUI (Using OpenStack's GUI project `horizon`)
3. Directly calling the Cinder APIs

Internally, the CLI and GUI both use Cinder APIs to interact with the Cinder API server, but for
a relatively new guy to OpenStack, I think an introduction through CLI would make the most sense.

Assumptions made:

1. You understand how to setup a DevStack environment and already have one ready at hand (remember `./stack.sh`?)
2. You know how to pass default credentials to local shell environment (`. /home/path_to_your_devstack_repo/eucarc` will do)

Let's start.

### Creation and deletion of volumes

Create a 1-GB cinder volume with no name by running command `cinder create 1`.
```
stack@stlrx300s7-27:/$ cinder create 1
+---------------------+--------------------------------------+
|       Property      |                Value                 |
+---------------------+--------------------------------------+
|     attachments     |                  []                  |
|  availability_zone  |                 nova                 |
|       bootable      |                false                 |
|      created_at     |      2013-05-28T10:32:47.243613      |
| display_description |                 None                 |
|     display_name    |                 None                 |
|          id         | 6754d216-4792-4a38-964a-d002686c8f92 |
|       metadata      |                  {}                  |
|         size        |                  1                   |
|     snapshot_id     |                 None                 |
|     source_volid    |                 None                 |
|        status       |               creating               |
|     volume_type     |                 None                 |
+---------------------+--------------------------------------+
```

Here I am describing only the minimal functionality of a command. If you wish to see more info about what all you
can do with that command, just type `cinder help <command>`, so to see all the optional parameters you can pass
while creating a Cinder volume, execute `cinder help create`.

```
stack@stlrx300s7-27:/$ cinder help create
usage: cinder create [--snapshot-id <snapshot-id>]
                     [--source-volid <source-volid>] [--image-id <image-id>]
                     [--display-name <display-name>]
                     [--display-description <display-description>]
                     [--volume-type <volume-type>]
                     [--availability-zone <availability-zone>]
                     [--metadata [<key=value> [<key=value> ...]]]
                     <size>

Add a new volume.

Positional arguments:
  <size>                Size of volume in GB

Optional arguments:
  --snapshot-id <snapshot-id>
                        Create volume from snapshot id (Optional,
                        Default=None)
  --source-volid <source-volid>
                        Create volume from volume id (Optional, Default=None)
  --image-id <image-id>
                        Create volume from image id (Optional, Default=None)
  --display-name <display-name>
                        Volume name (Optional, Default=None)
  --display-description <display-description>
                        Volume description (Optional, Default=None)
  --volume-type <volume-type>
                        Volume type (Optional, Default=None)
  --availability-zone <availability-zone>
                        Availability zone for volume (Optional, Default=None)
  --metadata [<key=value> [<key=value> ...]]
                        Metadata key=value pairs (Optional, Default=None)
```

Don't worry about the parameters, we'll use most of them in a short time.

Let's create a Cinder volume of size 1GB with a name, using `cinder create --display-name my_second_vol 1`:
```
stack@stlrx300s7-27:/$ cinder create --display-name my_second_vol 1
+---------------------+--------------------------------------+
|       Property      |                Value                 |
+---------------------+--------------------------------------+
|     attachments     |                  []                  |
|  availability_zone  |                 nova                 |
|       bootable      |                false                 |
|      created_at     |      2013-05-28T10:40:32.801981      |
| display_description |                 None                 |
|     display_name    |            my_second_vol             |
|          id         | 25fa2028-46dc-4870-84c5-d062ae99dd7a |
|       metadata      |                  {}                  |
|         size        |                  1                   |
|     snapshot_id     |                 None                 |
|     source_volid    |                 None                 |
|        status       |               creating               |
|     volume_type     |                 None                 |
+---------------------+--------------------------------------+
```

Now lets list out all the Cinder volumes, using `cinder list`:
```
stack@stlrx300s7-27:/$ cinder list
+--------------------------------------+-----------+---------------+------+-------------+----------+-------------+
|                  ID                  |   Status  |  Display Name | Size | Volume Type | Bootable | Attached to |
+--------------------------------------+-----------+---------------+------+-------------+----------+-------------+
| 25fa2028-46dc-4870-84c5-d062ae99dd7a | available | my_second_vol |  1   |     None    |  false   |             |
| 6754d216-4792-4a38-964a-d002686c8f92 | available |      None     |  1   |     None    |  false   |             |
+--------------------------------------+-----------+---------------+------+-------------+----------+-------------+
```

Now lets delete the first volume (the one without a name), using `cinder delete <volume_id>` command. If you
execute `cinder list` real quick, you will see the status of the volume going to 'deleting', and after some time
the volume will be deleted:
```
stack@stlrx300s7-27:/$ cinder delete 6754d216-4792-4a38-964a-d002686c8f92
stack@stlrx300s7-27:/$ cinder list 
+--------------------------------------+-----------+---------------+------+-------------+----------+-------------+
|                  ID                  |   Status  |  Display Name | Size | Volume Type | Bootable | Attached to |
+--------------------------------------+-----------+---------------+------+-------------+----------+-------------+
| 25fa2028-46dc-4870-84c5-d062ae99dd7a | available | my_second_vol |  1   |     None    |  false   |             |
| 6754d216-4792-4a38-964a-d002686c8f92 |  deleting |      None     |  1   |     None    |  false   |             |
+--------------------------------------+-----------+---------------+------+-------------+----------+-------------+
stack@stlrx300s7-27:/$ 
stack@stlrx300s7-27:/$ 
stack@stlrx300s7-27:/$ cinder list
+--------------------------------------+-----------+---------------+------+-------------+----------+-------------+
|                  ID                  |   Status  |  Display Name | Size | Volume Type | Bootable | Attached to |
+--------------------------------------+-----------+---------------+------+-------------+----------+-------------+
| 25fa2028-46dc-4870-84c5-d062ae99dd7a | available | my_second_vol |  1   |     None    |  false   |             |
+--------------------------------------+-----------+---------------+------+-------------+----------+-------------+
```

On a default DevStack installation, for a volume in Cinder, a 'logical volume' is created on the Linux machine,
inside the 'physical volume' named `stack-volumes`. To see the logical volumes, and physical volumes on the
ubuntu machine, just run `lvs` (logical volume scan) and `pvs` (physical volume scan) respectively (this is just
for information and you can entirely skip this part):
```
stack@stlrx300s7-27:/$ sudo lvs
  LV                                          VG            Attr   LSize Origin Snap%  Move Log Copy%  Convert
  volume-25fa2028-46dc-4870-84c5-d062ae99dd7a stack-volumes -wi-ao 1.00g
stack@stlrx300s7-27:/$
stack@stlrx300s7-27:/$ sudo pvs
  PV         VG            Fmt  Attr PSize PFree
  /dev/loop0 stack-volumes lvm2 a-   5.01g 4.01g
```

### Volume snapshots

Create the snapshot of volume:
```
stack@stlrx300s7-27:/$ cinder snapshot-create 25fa2028-46dc-4870-84c5-d062ae99dd7a
+---------------------+--------------------------------------+
|       Property      |                Value                 |
+---------------------+--------------------------------------+
|      created_at     |      2013-05-28T10:55:03.966690      |
| display_description |                 None                 |
|     display_name    |                 None                 |
|          id         | baf8764f-4c9b-496a-b2ff-bd49825c5d09 |
|       metadata      |                  {}                  |
|         size        |                  1                   |
|        status       |               creating               |
|      volume_id      | 25fa2028-46dc-4870-84c5-d062ae99dd7a |
+---------------------+--------------------------------------+
```

List all the snapshots:
```
stack@stlrx300s7-27:/$ cinder snapshot-list
+--------------------------------------+--------------------------------------+-----------+--------------+------+
|                  ID                  |              Volume ID               |   Status  | Display Name | Size |
+--------------------------------------+--------------------------------------+-----------+--------------+------+
| baf8764f-4c9b-496a-b2ff-bd49825c5d09 | 25fa2028-46dc-4870-84c5-d062ae99dd7a | available |     None     |  1   |
+--------------------------------------+--------------------------------------+-----------+--------------+------+
```

Now lets create a new volume of 1GB from the snapshot:
```
stack@stlrx300s7-27:/$ cinder create --snapshot-id baf8764f-4c9b-496a-b2ff-bd49825c5d09 1
+---------------------+--------------------------------------+
|       Property      |                Value                 |
+---------------------+--------------------------------------+
|     attachments     |                  []                  |
|  availability_zone  |                 nova                 |
|       bootable      |                false                 |
|      created_at     |      2013-05-28T10:56:20.478141      |
| display_description |                 None                 |
|     display_name    |                 None                 |
|          id         | 99ebe1d0-678b-4a9a-8ec4-438f9804d327 |
|       metadata      |                  {}                  |
|         size        |                  1                   |
|     snapshot_id     | baf8764f-4c9b-496a-b2ff-bd49825c5d09 |
|     source_volid    |                 None                 |
|        status       |               creating               |
|     volume_type     |                 None                 |
+---------------------+--------------------------------------+
```
Now you will see two volumes when you'll do a `cinder list`.


### Accessing volumes from inside a virtual instance
You can attach a volume to a VM instance, to provide additional persistent storage to that VM. It
works just like you attach an external HDD to your computer/laptop. But first, we'll need to create a
virtual machine for that.

List out all the virtual machine images present in our DevStack setup, from which we can boot a
brand new VM instance, using `glance image-list` or 'nova image-list`:
```
stack@stlrx300s7-27:/$ nova image-list
+--------------------------------------+---------------------------------+--------+--------+
| ID                                   | Name                            | Status | Server |
+--------------------------------------+---------------------------------+--------+--------+
| 291fe347-3a6f-4a21-9e85-e8809cb05d6e | cirros-0.3.1-x86_64-uec         | ACTIVE |        |
| 69d14d74-4185-4ba3-9666-1e7f569f38c6 | cirros-0.3.1-x86_64-uec-kernel  | ACTIVE |        |
| 8793532d-0c09-4b1c-aab8-d10832f13c09 | cirros-0.3.1-x86_64-uec-ramdisk | ACTIVE |        |
+--------------------------------------+---------------------------------+--------+--------+
```

We'll use the image with the shortest name, and boot an instance, giving it a name `myinstance`.
You can list all the virtual machine instances registered with Nova using command `nova list`.
If just after running the command to boot the virtual machine, you run `nova list` a few times,
you will see the machine state going from 'BUILD' to 'ACTIVE' in a few seconds.
```
stack@stlrx300s7-27:/$ nova boot --flavor m1.tiny --image 291fe347-3a6f-4a21-9e85-e8809cb05d6e myinstance
+-----------------------------+--------------------------------------+
| Property                    | Value                                |
+-----------------------------+--------------------------------------+
| status                      | BUILD                                |
| updated                     | 2013-05-28T11:03:47Z                 |
| OS-EXT-STS:task_state       | scheduling                           |
| key_name                    | None                                 |
| image                       | cirros-0.3.1-x86_64-uec              |
| hostId                      |                                      |
| OS-EXT-STS:vm_state         | building                             |
| flavor                      | m1.tiny                              |
| id                          | 3b6dd9f1-3ca3-4eed-a508-1cd62d55629f |
| security_groups             | [{u'name': u'default'}]              |
| user_id                     | 35708cb6795845fcab6362e908e6b0cf     |
| name                        | myinstance                           |
| adminPass                   | cQh34G96dCHX                         |
| tenant_id                   | 11f8fde7d627422d84036cabd6cbb7f8     |
| created                     | 2013-05-28T11:03:47Z                 |
| OS-DCF:diskConfig           | MANUAL                               |
| metadata                    | {}                                   |
| accessIPv4                  |                                      |
| accessIPv6                  |                                      |
| progress                    | 0                                    |
| OS-EXT-STS:power_state      | 0                                    |
| OS-EXT-AZ:availability_zone | nova                                 |
| config_drive                |                                      |
+-----------------------------+--------------------------------------+
stack@stlrx300s7-27:/$ nova list
+--------------------------------------+------------+--------+------------+-------------+----------+
| ID                                   | Name       | Status | Task State | Power State | Networks |
+--------------------------------------+------------+--------+------------+-------------+----------+
| 3b6dd9f1-3ca3-4eed-a508-1cd62d55629f | myinstance | BUILD  | networking | NOSTATE     |          |
+--------------------------------------+------------+--------+------------+-------------+----------+
stack@stlrx300s7-27:/$ nova list
+--------------------------------------+------------+--------+------------+-------------+----------+
| ID                                   | Name       | Status | Task State | Power State | Networks |
+--------------------------------------+------------+--------+------------+-------------+----------+
| 3b6dd9f1-3ca3-4eed-a508-1cd62d55629f | myinstance | BUILD  | spawning   | NOSTATE     |          |
+--------------------------------------+------------+--------+------------+-------------+----------+
stack@stlrx300s7-27:/$ nova list
+--------------------------------------+------------+--------+------------+-------------+------------------+
| ID                                   | Name       | Status | Task State | Power State | Networks         |
+--------------------------------------+------------+--------+------------+-------------+------------------+
| 3b6dd9f1-3ca3-4eed-a508-1cd62d55629f | myinstance | ACTIVE | None       | Running     | private=10.0.0.2 |
+--------------------------------------+------------+--------+------------+-------------+------------------+
```

Now lets attach one of our volume to this instance, and then try to peek into this volume after logging into the instance.

Attach volume using command `nova volume-attach <instance_id> <volume_id> <attach_location>`. We'll attach at the first
free device location: `/dev/vdb`:
```
stack@stlrx300s7-27:/$ nova volume-attach 3b6dd9f1-3ca3-4eed-a508-1cd62d55629f 25fa2028-46dc-4870-84c5-d062ae99dd7a /dev/vdb
+----------+--------------------------------------+
| Property | Value                                |
+----------+--------------------------------------+
| device   | /dev/vdb                             |
| serverId | 3b6dd9f1-3ca3-4eed-a508-1cd62d55629f |
| id       | 25fa2028-46dc-4870-84c5-d062ae99dd7a |
| volumeId | 25fa2028-46dc-4870-84c5-d062ae99dd7a |
+----------+--------------------------------------+
```

Now listing the volume will tell you that the volume is attached to an instance (in use):
```
stack@stlrx300s7-27:/$ cinder list
+--------------------------------------+-----------+---------------+------+-------------+----------+--------------------------------------+
|                  ID                  |   Status  |  Display Name | Size | Volume Type | Bootable |             Attached to              |
+--------------------------------------+-----------+---------------+------+-------------+----------+--------------------------------------+
| 25fa2028-46dc-4870-84c5-d062ae99dd7a |   in-use  | my_second_vol |  1   |     None    |  false   | 3b6dd9f1-3ca3-4eed-a508-1cd62d55629f |
| 99ebe1d0-678b-4a9a-8ec4-438f9804d327 | available |      None     |  1   |     None    |  false   |                                      |
+--------------------------------------+-----------+---------------+------+-------------+----------+--------------------------------------+
```

Now let's login into this virtual machine using the private IP of the instance (`10.0.0.2` in our case). Note how an
error message pops up if you have already created an instance last time when you installed DevStack. If such an error
appears on your screen too, follow the instructions just like the way I did. The default password for the cirros image
we used is `cubswin:)`. Enter into the instance, and then become root:
```
stack@stlrx300s7-27:/$ ssh cirros@10.0.0.2
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the RSA key sent by the remote host is
f5:ac:45:4c:63:8e:e4:19:cc:5a:76:7e:a1:08:e7:c8.
Please contact your system administrator.
Add correct host key in /opt/stack/.ssh/known_hosts to get rid of this message.
Offending RSA key in /opt/stack/.ssh/known_hosts:4
  remove with: ssh-keygen -f "/opt/stack/.ssh/known_hosts" -R 10.0.0.2
RSA host key for 10.0.0.2 has changed and you have requested strict checking.
Host key verification failed.

stack@stlrx300s7-27:/$ ssh-keygen -f "/opt/stack/.ssh/known_hosts" -R 10.0.0.2
/opt/stack/.ssh/known_hosts updated.
Original contents retained as /opt/stack/.ssh/known_hosts.old
```
```
stack@stlrx300s7-27:/$ ssh cirros@10.0.0.2
The authenticity of host '10.0.0.2 (10.0.0.2)' can't be established.
RSA key fingerprint is f5:ac:45:4c:63:8e:e4:19:cc:5a:76:7e:a1:08:e7:c8.
Are you sure you want to continue connecting (yes/no)? yes
Warning: Permanently added '10.0.0.2' (RSA) to the list of known hosts.
cirros@10.0.0.2's password: 
$sudo -i
#
```

Run `fdisk -l` to see the disks present for the instance. You will see that your newly attached disk
`/dev/vdb` of size 1GB is now present:
```
# fdisk -l

Disk /dev/vda: 1073 MB, 1073741824 bytes
16 heads, 63 sectors/track, 2080 cylinders, total 2097152 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x00000000

Disk /dev/vda doesn't contain a valid partition table

Disk /dev/vdb: 1073 MB, 1073741824 bytes
16 heads, 63 sectors/track, 2080 cylinders, total 2097152 sectors
Units = sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disk identifier: 0x00000000

Disk /dev/vdb doesn't contain a valid partition table
```

Command `blkid /dev/vd*` lists out the IDs of block devices for this machine and some related info. Running
this command you will see that info of only the virtual disk `/dev/vda` is present, meaning our disk `/dev/vdb`
needs formatting.
```
# blkid /dev/vd*
/dev/vda: LABEL="cirros-rootfs" UUID="74251bb8-3a28-4a46-9a78-064497b26b9d" SEC_TYPE="ext2" TYPE="ext3" 
```

Lets format it to make an EXT3 partition with block-size 1024 bytes using command `mkfs.ext3 -b 1024 /dev/vdb`:
```
# mkfs.ext3 -b 1024 /dev/vdb
mke2fs 1.42.2 (27-Mar-2012)
Filesystem label=
OS type: Linux
Block size=1024 (log=0)
Fragment size=1024 (log=0)
Stride=0 blocks, Stripe width=0 blocks
65536 inodes, 1048576 blocks
52428 blocks (5.00%) reserved for the super user
First data block=1
Maximum filesystem blocks=68157440
128 block groups
8192 blocks per group, 8192 fragments per group
512 inodes per group
Superblock backups stored on blocks: 
        8193, 24577, 40961, 57345, 73729, 204801, 221185, 401409, 663553, 
        1024001

Allocating group tables: done                            
Writing inode tables: done                            
Creating journal (32768 blocks): done
Writing superblocks and filesystem accounting information: done
```

Run `blkid` again to see the newly partitioned disk listed:
```
# blkid /dev/vd*
/dev/vda: LABEL="cirros-rootfs" UUID="74251bb8-3a28-4a46-9a78-064497b26b9d" SEC_TYPE="ext2" TYPE="ext3" 
/dev/vdb: UUID="22838e81-eb97-457d-b1e0-4ff3d8e45b05" SEC_TYPE="ext2" TYPE="ext3" 
```

In order to use this disk, you need to mount it at some location. I'll create a directory `/tempmount`
and mount our virtual block device there:
```
# mkdir /tempmount
# mount /dev/vdb /tempmount/
```

Now you can see the disk listed in the machine disks, using `df -h` command:
```
# df -h
Filesystem                Size      Used Available Use% Mounted on
/dev                    242.3M         0    242.3M   0% /dev
/dev/vda                 31.0M      9.7M     19.7M  33% /
tmpfs                   245.9M         0    245.9M   0% /dev/shm
tmpfs                   200.0K     76.0K    124.0K  38% /run
/dev/vdb               1007.7M     34.9M    921.6M   4% /tempmount
```

Now you can `cd` into `/tempmount` directory, and do whatever you want to do with the new disk -- put some files there,
or download one!

Lets wrap up this part. Unmount this volume by `umount /tempmount`, and log out from the machine by pressing `CTRL+D` twice, and execute `nova volume-detach <volume_id>
<server_id>` to detach this volume. You can now see the 'Attached to' column becomes empty again after detaching.
```
stack@stlrx300s7-27:/$ cinder list
+--------------------------------------+-----------+---------------+------+-------------+----------+--------------------------------------+
|                  ID                  |   Status  |  Display Name | Size | Volume Type | Bootable |             Attached to              |
+--------------------------------------+-----------+---------------+------+-------------+----------+--------------------------------------+
| 25fa2028-46dc-4870-84c5-d062ae99dd7a |   in-use  | my_second_vol |  1   |     None    |  false   | 3b6dd9f1-3ca3-4eed-a508-1cd62d55629f |
| 99ebe1d0-678b-4a9a-8ec4-438f9804d327 | available |      None     |  1   |     None    |  false   |                                      |
+--------------------------------------+-----------+---------------+------+-------------+----------+--------------------------------------+
stack@stlrx300s7-27:/$ nova volume-detach 3b6dd9f1-3ca3-4eed-a508-1cd62d55629f 25fa2028-46dc-4870-84c5-d062ae99dd7a
stack@stlrx300s7-27:/$ cinder list
+--------------------------------------+-----------+---------------+------+-------------+----------+-------------+
|                  ID                  |   Status  |  Display Name | Size | Volume Type | Bootable | Attached to |
+--------------------------------------+-----------+---------------+------+-------------+----------+-------------+
| 25fa2028-46dc-4870-84c5-d062ae99dd7a | available | my_second_vol |  1   |     None    |  false   |             |
| 99ebe1d0-678b-4a9a-8ec4-438f9804d327 | available |      None     |  1   |     None    |  false   |             |
+--------------------------------------+-----------+---------------+------+-------------+----------+-------------+
```

### More features
(Will update shortly)

Cheers!