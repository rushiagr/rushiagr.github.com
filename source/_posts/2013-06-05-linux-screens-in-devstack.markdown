---
layout: post
title: "Linux Screens in DevStack"
date: 2013-06-05 20:50
comments: true
categories: [tech, openstack, cloud]
---

This blog article explains handling screens within OpenStack running as a DevStack setup. Some useful generic screen commands are also provided at the end.

<!--more-->

In a DevStack environment, all the processes run under something special in Linux, called as a `screen`. For now, you can think of a ‘screen’ as a terminal running inside a terminal, with the special property that when you close your current terminal, your ‘screens’ will not actually die, so that you can reconnect to them when you connect to the Linux system through another terminal again! Now that should give you a hint why people use screens :)

Each screen runs a special ‘service’ of OpenStack. So the logs of each service will go to the respective screen. If you created the DevStack environment as a root user, the process of going to a screen is slightly complicated: You first need to become the `stack` user if you are currently `root`, and even before that, you need to run this command in most of the cases:

```
chown stack:stack `readlink /proc/self/fd/0`
```
Else it will produce this error `Cannot open your terminal '/dev/pts/2' - please check.` , and then you can proceed to run this command to get to the screens:

```
screen -x
```
And if you ran the DevStack `stack.sh` script as a non-root user, you just need to run that last little thingy to see the screens. One more reason why you should run DevStack as a non-root.

The way to detach from a screen is `CTRL+A` `D`, that is, first press `CTRL+A`, and then press `D`.

## Navigating across screens

You will see names of all the screens at the bottom of the terminal. The screen on which you currently are bears an asterisk (`*`) near its name. To move to the right screen, do a `CTRL+A` `N`. Keep in mind that you are going to use `CTRL+A` a lot of times during your adventures with screen. Similar to the command `CTRL+A` `N` to move to the right (“next”) screen, to move to the left screen the command is `CTRL+A` `P`.

There is one more way to jump directly to a screen. Lets say you want to directly jump to the fourth screen. You just need to do a `CTRL+A` `4`, to go to fourth screen! Wasn’t that easy? But hey! How do I get to the seventeenth screen? Frankly, I don’t know a ‘direct’ way. I do a `CTRL+A` `9` once, and `CTRL+A` `N` eight more times. :( If you have a better way, please do tell me.

Navigating inside a screen

The first and biggest difficulty I faced while tracking an error in the screen logs is the periodic updates in Cinder dumps some lines to the Cinder screens every now and then. So if you have a stack trace of an error on the screen, it will go up and up and up till you can no more see it! Nope, scrolling your mouse up, or pulling the scrollbar up won’t help either (why not try it once :) ).

Within a few days, I thought “Hey, I’ll just reduce the font of the terminal and I’ll be able to see more lines of screen logs on my screen!”. I knew the command to reduce the font size of the terminal font: `CTRL`+`-` (just for the sake of completeness, the command to increase font is `CTRL`+`SHIFT`+`+`). That worked pretty okay upto a point. It actually helps to have logs in small font, as the logs will fit in one line on the screen and will look prettier. But what if I come after say a ten-minute break, and see all my logs are too far up to be able to see even by reducing font size?

Then I got to know the command which saved a ton of time in my life: The command to actually scroll up and down the screen.

To scroll up, first press `CTRL`+`[`. After that, you can use arrow keys to scroll up and down. You can also use `page-up` and `page-down` buttons to scroll one complete page up or down. This isn’t all of it. If you are vim user, you will find that the `H` `J` `K` `L` will work for for `left`, `down`, `up`, and `right` respectively. And the last and most convenient thing: once you press `CTRL` `[`, that is, once you are in ‘copy mode’, you can then use your mouse scroll wheel too to scroll up and down!! Now that is a perfect delight :)

To come out of this copy mode (so that you can switch to another screen, and do other such stuff), press `]` and you are back to normal once again.

## Some more ‘generic’ screen commands

So that you can start playing around with screens outside OpenStack too

Create a new screen

```
screen
```
To detach from current screen

```
ctrl+A,D
```
To reattach to an existing screen

```
screen -rd
```
To view all the screens, their states and IDs

```
screen -list
```
To kill a screen with id SCREENID

```
screen -X -S SCREENID kill
```


Cheers!

-Rushi Agrawal
