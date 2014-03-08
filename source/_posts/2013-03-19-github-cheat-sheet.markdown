---
layout: post
title: "Git(hub) Cheat Sheet"
date: 2013-03-19 04:22
comments: true
categories: git, github, cheat-sheet, web, tech
---


I am posting my github cheat sheet here. I started writing it as soon as I started
learning Github and Git. So, some of the content here can appear quite naive. 
I will try to keep this blog post as updated as I can, and if you find any 
suggestion, please comment!

This post is just for a reference of commands. This post will be a bad way to learn
how git works. A basic understanding of git is assumed.

<!--more-->

##Initial configuration
Configure user details only for the first time
    git config --global user.name "Rushi Agrawal"
    git config --global user.email "rushi.agr@gmail.com"
To check your git configuration
	git config --list
	
##Branches
List all branches in the local repo
	git branch
List all branches including remote-tracking branches
	git branch -r
List all branches (including the ones at remote)
	git branch -a
	
Creating your own branch `my_branch`, with content same as your current branch
	git branch my_branch
Switch to the newly created branch
	git checkout my_branch
Execute the above two commands in one line:
	git checkout -b my_branch
to pull a branch `only_remote` which exists at github (at remote `rushiagr` but not in local repo. (More about `git remote update` later)
	git remote update
    git checkout -b only_remote rushiagr/only_remote

## Remotes
Create a new remote `rushiagr` which will track `cinder` repository by user `rushiagr`
    git remote add rushiagr https://github.com/rushiagr/cinder.git
If this is your personal repo, you can append the username in the remote as shown. After that, every time you push to the origin, 
github will not ask for your username but only password.
    git remote add rushiagr https://rushiagr@github.com/rushiagr/cinder.git
Delete the remote `rushiagr`
    git remote rm rushiagr
List all the remotes
    git remote
The above command only shows the names of remotes. To also check the links to the remotes:
    git remote -v
Now this is very important command.
    git remote update
This will contact the git server, and will update the local repository with ALL the content at ALL those remotes. The interesting part is, nothing will actually change. That is, no more new branches (which got created at the server after you last pulled from the server) were created, and the existing branches are also not updated. BUT, all the content goes into the magic `.git` directory. After you've run this command, when you create a branch only existing at remote, the local git repo will not contact the server but will fetch all the contents from within the repository.

To take a new branch from remote, and create a new branch having contents of that remote branch. (You might need to run 'git remote update')
	git checkout -b stable/folsom origin/stable/folsom

## Push
Pushing this newly created branch to remote `rushiagr`
	git push rushiagr my_branch
If you want to push the local branch `my_branch` with a different name to 
remote, say `my_remote_branch`:
    git push rushiagr my_branch:my_remote_branch
To create an association with the remote (only first time):
	git push -u origin my_branch
or
	git push --set-upstream origin my_branch

## Pull
Git pull is nothing more than a macro that does git fetch and git merge, in 
that order. The common syntax to pull from branch `remote_branch` located at remote `remote_name` to the current active branch in the local repo:
	git pull remote_name remote_branch

## Oops! I didn't intend to do that!
####To undo last commit. 
This will just undo the commit, but will keep changes, so that you can modify the files and commit again
	git reset --soft HEAD^
####To not keep the uncommitted changes. 
This command will wipe off all the changes which are not committed. Very useful when you made some changes but dont want to commit it. All the more useful when you `pull`ed something but everything became a mess (possibly due to a merge conflict, or pulling to/from a different branch!)
	git reset --hard
####To delete a branch `timepass_testing` from github server
	git push rushiagr --delete timepass_testing
(NOT `git push rushiagr --delete rushiagr/timepass_testing`)
####Change author of the last commit
	git commit --amend --author="Rushi Agrawal <rushi.agr@gmail.com>"
You committed some changes, but then you realised you wanted to add this one line to the commit. In such a case
just add that one line, and run this command to have this last change incorporated into that previous commit. This command also gives you an option to 
change the commit message.
    git commit -a --amend

## Show me the money
To see the patch of the last commit without undoing the last commit
	git show
To see the changes introduced by any earlier commit with commit id `c5bb6d821e10ca8f114fa0b3b0149bc8b7257a92`
    git show c5bb6d821e10ca8f114fa0b3b0149bc8b7257a92
To see the latest changes you made -- the changes which have not been staged to be committed
    git diff
You can redirect the output from the above three commands to a file, to create corresponding patch file.

## Patching in git	
Check the status of patch. How many lines changed, etc
	git apply --stat patchfile
Check if the patch can be applied.
If no output or no error, patch can be applied safely
	git apply --check patchfile
Apply patch with signing-off (better way)
	git am --signoff < patchfile
Normal way of applying patch
	git apply patchfile


##Miscellaneous
	
To pull only specific files from another branch: (here, assuming that we have two branches, 'test', and 'master', and currently we are on 'master' branch. If you want to pull ##only 'testfile.py' file from 'test' branch to 'master' branch, do this:)
	git checkout test testfile.py1
	
	
	
If your master changed while you were working on your topic_branch, and if you want to merge the master's changes, and also get an option to squash the changes you made on topic_branch:
	git checkout master
	git pull origin master
	git checkout topic_branch
	git rebase -i master

[Undo last commit at the remote repo](http://christoph.ruegg.name/blog/2010/5/5/git-howto-revert-a-commit-already-pushed-to-a-remote-reposit.html}
(you can use git revert, but don’t know how exactly it works)

Clone a specific branch git repository from github
	git clone -b stable/essex https://github.com/openstack-dev/devstack.git

[Squash several commits into one single commit](https://makandracards.com/makandra/527-squash-several-git-commits-into-a-single-commit)
	
Checkout a previous commit with SHA commit id cff2580ad7bc16934b72dd9be7463eb090b31d55 from the current branch to a new branch 'neew'
	git checkout -b neew cff2580ad7bc16934b72dd9be7463eb090b31d55
	

