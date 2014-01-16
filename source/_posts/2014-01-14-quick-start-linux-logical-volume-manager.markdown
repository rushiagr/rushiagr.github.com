---
layout: post
title: "Quick Start: Linux Logical Volume Manager"
date: 2014-01-14 20:09
comments: true
categories: 
---

While installing the latest Ubuntu OS on your computer, you will see that 
you can install the OS using LVM (Logical Volume Manager) utility. Ever wonder what is it?
LVM (Logical Volume Manager) is that fantastic utility for storage administration.
It provide the users with abilities which were not possible with raw disks.
The storage is now 'virtualized'. You can now easily create, move and extend volumes (for now, think of it as disk partitions)
without bothering about data corruption. You can carve partitions out of multiple disks,
and can add and remove disks from a 'volume group' containing such volumes without the user noticing anything!
List of all the features of LVM can be found at it's <a href="http://en.wikipedia.org/wiki/Logical_Volume_Manager_(Linux)"
target="_blank">wiki page</a>.

This blog scratches the surface of LVM, and gives some basic insights into some storage concepts.


<!-- more -->

I'll give you a simple example to better explain what a 'physical volume', a 'volume group' and a 
'logical volume' is. Say I have two 1 TB hard disks - disk A and disk B. I have two equal-sized partitions on
disk B, one of which I want to keep it to myself for my personal data. The 'partition' term used here is 
same as what you see in a file explorer. For the unpartitioned disk, the complete disk is one single partition.

The partitions I described above are 'physical volumes'. That is, on the disk, these are physically separate bytes (think of that
partitioned disk as a spiral on disk divided in its length at the midpoint).
Out of the first disk and one partition of the second disk, we create a 'volume group' -- a logical pool of storage, out of which we can 
create lots of 'logical volumes'. Even after you've created logical volumes over this volume group, you can add and remove physical volumes (partitions) from the volume group. You can do many more operations such as resize, move and extend.

I hope the basic idea written above is sufficiently clear. Else, head over to this Ubuntu <a href="https://wiki.ubuntu.com/Lvm" target="_blank">wiki</a> for a slightly more detailed, but still an overview, of LVM. Anyway, I'm concentrating more on the demo, so lets move on.

#### Hands-on
I'm demo'ing everything on an Ubuntu machine, but it should work on any Linux distro (after you install the LVM2 package)

Install LVM2 package
    sudo apt-get install lvm2


One nice thing is you don't need to create actual partitions on disks. We'll use files as <a href="http://en.wikipedia.org/wiki/Loop_device" target="_blank">loopback devices</a>, which will appear to the operating system as partitions. Neat.

Create a file of size 1G to be later used as a physical volume.
    rushi@jio:~$ truncate --size 1G backing_file_1

Create a loopback device over this file. Find the first free loopback device available and show its name.
    rushi@jio:~$ sudo losetup --find --show backing_file_1 
    /dev/loop0

List all the loopback devices.
    rushi@jio:~$ sudo losetup --all
    /dev/loop0: [fc00]:22811987 (/home/rushi/backing_file_1)

Create a physical volume over this loopback device. Note that 
    rushi@jio:~$ sudo pvcreate /dev/loop0 
      Physical volume "/dev/loop0" successfully created

List physical volumes. Apart from `pvs` (Physical Volume Scan), there are two more 
commands which do the same thing, but with different level of verbosity and formatting: `pvscan` and `pvdisplay`. (Try them out too!)
    rushi@jio:~$ sudo pvs
      PV         VG        Fmt  Attr PSize   PFree 
      /dev/loop0           lvm2 a--    1.00g  1.00g
      /dev/sda5  ubuntu-vg lvm2 a--  931.27g 44.00m


Let us repeat the steps to create another physical volume:
    rushi@jio:~$ truncate --size 1G backing_file_2
    rushi@jio:~$ sudo losetup --find --show backing_file_2 
    /dev/loop1
    rushi@jio:~$ sudo losetup --all
    /dev/loop0: [fc00]:22811987 (/home/rushi/backing_file_1)
    /dev/loop1: [fc00]:22812001 (/home/rushi/backing_file_2)
    rushi@jio:~$ sudo pvcreate /dev/loop1
      Physical volume "/dev/loop1" successfully created
    rushi@jio:~$ sudo pvs
      PV         VG        Fmt  Attr PSize   PFree 
      /dev/loop0           lvm2 a--    1.00g  1.00g
      /dev/loop1           lvm2 a--    1.00g  1.00g
      /dev/sda5  ubuntu-vg lvm2 a--  931.27g 44.00m

Create a volume group `test-volgroup` over these two physical volumes. (Actually, even if you don't create physical volumes over loopback devices, while creating volume groups it will automatically create physical volumes over them).
    rushi@jio:~$ sudo vgcreate test-volgroup /dev/loop0 /dev/loop1
      Volume group "test-volgroup" successfully created

List the volume groups. (`vgs`, `vgscan` or `vgdisplay` can be used)
    rushi@jio:~$ sudo vgs
      VG            #PV #LV #SN Attr   VSize   VFree 
      test-volgroup   2   0   0 wz--n-   1.99g  1.99g
      ubuntu-vg       1   2   0 wz--n- 931.27g 44.00m

Create a logical volume `test-logicalvol` over the `test-volgroup` volume group.
    rushi@jio:~$ sudo lvcreate --size 400M --name test-logicalvol test-volgroup
      Logical volume "test-logicalvol" created

List logical volumes. (`lvs`, `lvscan`, `lvdisplay` can be used)
    rushi@jio:~$ sudo lvs
      LV              VG            Attr      LSize   Pool Origin Data%  Move Log Copy%  Convert
      test-logicalvol test-volgroup -wi-a---- 400.00m                                           
      root            ubuntu-vg     -wi-ao--- 923.35g                                           
      swap_1          ubuntu-vg     -wi-ao---   7.88g                                           


Easy, isn't it? Let's tear down everything. Though a simpler way would be to just remove the loopback device, which will automatically 
remove all the physical, logical volumes/volume groups created over them, let's do it step-by-step. Note that you need to specify volume group while deleting logical volumes.
    rushi@jio:~$ sudo lvremove test-volgroup
    Do you really want to remove active logical volume test-logicalvol? [y/n]: y
      Logical volume "test-logicalvol" successfully removed
    rushi@jio:~$ sudo vgremove test-volgroup
      Volume group "test-volgroup" successfully removed
    rushi@jio:~$ sudo pvremove /dev/loop0 /dev/loop1
      Labels on physical volume "/dev/loop0" successfully wiped
      Labels on physical volume "/dev/loop1" successfully wiped
    rushi@jio:~$ sudo losetup --detach /dev/loop0 /dev/loop1
    rushi@jio:~$ rm backing_file_1 backing_file_2

Cheers!

