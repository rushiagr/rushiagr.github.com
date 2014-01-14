---
layout: post
title: "Installing OpenID plugin for MediaWiki"
date: 2014-01-12 13:09
comments: true
categories: 
---

This post is about setting up your wiki such that their users access the wiki
only via an OpenID provider login (e.g. Google or Facebook login). This post assumes 
MediaWiki is already installed.

<!--more-->


### Assumptions, prerequisites and requirements
All of what this blogpost says has been tried on an Ubuntu machine, but it 
should work well on other Linux distros too (except for the `apt-get` package 
installs, for which you'll need to find alternatives on your favourite distro).

`$IP` is assumed to be the root of your wiki directory (which in my case is
`/var/www/wikis/<my_wiki>/`.

Install all the required packages for the plugin to work
```
sudo apt-get install php5-mcrypt php5-gmp
```


Installing the plugin
---------------------

Get the source code for the extension into ``$IP/extensions`` directory
```
	cd extensions
	git clone http://gerrit.wikimedia.org/r/p/mediawiki/extensions/OpenID.git 
```

Check your mediawiki version by going to ``<your_wiki_URL>/index.php?title=Special:Version``. Say your version is 1.19.x. 
  Check out branch for the same version of OpenID code
```
	git branch -a 
	git checkout -b stable_REL1_19 origin/REL1_19 
```

Add this line at the end of LocalSettings.php file
```
require_once "$IP/extensions/OpenID/OpenID.php"; 
```
Now install Auth subdirectory as following:
```
	cd $IP/extensions/OpenID 
	git clone http://github.com/openid/php-openid.git 
	mv php-openid/Auth Auth 
	rm -r php-openid 
	cd $IP 
	php maintenance/update.php --conf LocalSettings.php 
```
Restart apache server
```
	/etc/init.d/apache2 restart 
```

### Editing 'Login required' page.  

By default, the main page of the wiki is not editable. Generally we would like
to give some information to a user, e.g. what this wiki is all about, how
to log into it, which OpenIDs are permitted, etc.

Now we'll give any registered user the ability to edit the protected pages and the 
'interface' pages, of which our special login page is a part of. Add these lines
 to `$IP/LocalSettings.php`:
```
	$wgGroupPermissions['user']['editprotected'] = true; 
	$wgGroupPermissions['user']['editinterface'] = true; 
```
Now you can edit the ``<your_wiki_URL>/jiocloud/index.phpmediawiki:loginreqpagetext``
 page which is presented when the user is not logged in.


### Other settings
Below you can see a snip of LocalSettings.php file, which contains many other 
fields which I used to customize my wiki. I allowed only the registered user 
an edit permission (which most of you would also want I guess). Also, I have disabled
regular login, and made it mandatory users to login via only OpenID, and that too, 
only using their launchpad.net accounts (an issue tracking software from Canonical).

If you want to get more information regarding these (and more) 
configuration options, see <a href="http://www.mediawiki.org/wiki/Extension:OpenID" target="_blank">this</a> link.

```
# Disable reading by anonymous users
$wgGroupPermissions['*']['read'] = false;

# Disable anonymous editing too
$wgGroupPermissions['*']['edit'] = false;
 
# But allow them to access the OpenID login page or else there will be no way to log in!
$wgWhitelistRead = array ("Special:OpenIDLogin", "Special:OpenIDFinish", 
"MediaWiki:Common.css", "MediaWiki:Common.js", "MediaWiki:Monobook.css", 
"MediaWiki:Monobook.js", "-");
 
# For registered users, allow editing protected pages
$wgGroupPermissions['user']['editprotected'] = true;
$wgGroupPermissions['user']['editinterface'] = true;

# Only allow OpenIDs for login
$wgOpenIDLoginOnly = true;
$wgOpenIDOnly = true;       # a value used with older versions. Optional

# Your wiki web URL
$wgOpenIDTrustRoot = "http://your.wiki.url.com/";

# By default, deny all OpenID
$wgOpenIDConsumerDenyByDefault = true;

# Then allow only launchpad.net OpenID (with and without HTTPS both)
$wgOpenIDConsumerAllow = array("@^(https://)?launchpad.net/@");
```

Troubleshooting
---------------
If there are troubles uploading a file via the MediaWiki web interface, go to the wiki directory on the server and chown the ``images`` folder.

	sudo chown -R www-data:www-data images/

Don't forget to comment if you find the information presented here is outdated, or is not working for you.


Cheers,
Rushi
