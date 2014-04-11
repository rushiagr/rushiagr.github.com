---
layout: post
title: "MySQL Cheat Sheet"
date: 2014-03-31 18:49
comments: true
categories: [tech, cheatsheet]
---

Databases are so important, yet almost all the time I need to work with it, I find that I have already forgotten all the syntax! So here I am writing down a quick cheat sheet to get me up and running when I'm waking up from slumber. I hope this will help atleast one other guy on this planet.

<!-- more -->

I use mostly Ubuntu, so some of the commands might be Ubuntu specific.


Install mysql
	sudo apt-get install mysql-server

A prompt will ask for the root password.

To change the root password:
	UPDATE mysql.user SET password=PASSWORD('nova') WHERE user='root';
NOTE: MySQL keywords are case insensitive. They're represented in capital here just so that they appear different than the rest. When you're just testing out some things logging into the DB console, people generally prefer writing in small caps. 

Note that `PASSWORD` is a function, and unlike other MySQL keywords cannot be used in small caps.

Log into MySQL console with user `root` and password `mysecretpassword`:
	mysql -uroot -pmysecretpassword
or
	mysql -u'root' -p'mysecretpassword'
or entering the password in 'secret' mode:
	$ mysql -uroot -p
	Enter password: 



### MySQL console

List all databases:
	mysql> SHOW DATABASES;
	+--------------------+
	| Database           |
	+--------------------+
	| information_schema |
	| mysql              |
	| performance_schema |
	| test               |
	+--------------------+
	4 rows in set (0.01 sec)

Create a new database `rushi`:
	mysql> CREATE DATABASE rushi;
	Query OK, 1 row affected (0.00 sec)
	
	mysql> show databases;
	+--------------------+
	| Database           |
	+--------------------+
	| information_schema |
	| mysql              |
	| performance_schema |
	| rushi              |
	| test               |
	+--------------------+
	5 rows in set (0.00 sec)

Select database `rushi`, so that all the further operations are executed inside this database:
	mysql> USE rushi;
	Database changed

Create a table `friends` inside `rushi` database:
	mysql> CREATE TABLE friends (name VARCHAR(20), age INT);
	Query OK, 0 rows affected (0.03 sec)

If you didn't select the database in the last to last command, you need to specify table in this format:`<database>.<tablename>`. So the last command would look like:
	mysql> CREATE TABLE rushi.friends (name VARCHAR(20), age INT);

List all the tables:
	mysql> show tables;
	+-----------------+
	| Tables_in_rushi |
	+-----------------+
	| friends         |
	+-----------------+
	1 rows in set (0.00 sec)

Insert data into `friends`:
	mysql> INSERT INTO friends VALUES ('arvind', 24);
	Query OK, 1 row affected (0.01 sec)

Display all the data from the table:
	mysql> SELECT * FROM friends;
	+--------+------+
	| name   | age  |
	+--------+------+
	| arvind |   24 |
	+--------+------+
	1 row in set (0.00 sec)

Insert another friend:
	mysql> INSERT INTO friends VALUES ('honshu', 23);
	Query OK, 1 row affected (0.00 sec)
	
	mysql> SELECT * FROM friends;
	+--------+------+
	| name   | age  |
	+--------+------+
	| arvind |   24 |
	| honshu |   23 |
	+--------+------+
	2 rows in set (0.00 sec)


Update a row in the table:
	mysql> UPDATE friends SET age=22 WHERE name='honshu';
	Query OK, 1 row affected (0.02 sec)
	Rows matched: 1  Changed: 1  Warnings: 0

	mysql> SELECT * FROM friends;
	+--------+------+
	| name   | age  |
	+--------+------+
	| arvind |   24 |
	| honshu |   22 |
	+--------+------+
	2 rows in set (0.00 sec)

Delete a row from table:
	mysql> DELETE FROM friends WHERE age=24;
	Query OK, 1 row affected (0.00 sec)
	
	mysql> select * from friends;
	+--------+------+
	| name   | age  |
	+--------+------+
	| honshu |   22 |
	+--------+------+
	1 row in set (0.00 sec)

Delete all rows from the table in one go, and reset the autoincrement if any:
	mysql> TRUNCATE friends;
	Query OK, 0 rows affected (0.04 sec)

Delete the table and all of its contents:
	mysql> DROP TABLE friends;


Other commonly used commands are listed below. Try to try all of them out atleast once.
Count the number of rows in a table:
	SELECT COUNT(*) FROM friends;

Select distinct values for a row, and order them too:
	SELECT DISTINCT age FROM friends ORDER BY age;

Modify table to add one more column to it:
	ALTER TABLE friend ADD height varchar(10);

Use regular expressions:
	SELECT * FROM friend WHERE name REGEXP 'arv*';
CAUTION: Regular expressions comes with some binary/encoding trickery. Use it with a lot of caution.

Create a new user for the database, and give it all the root privileges
	CREATE USER 'rushiagr'@'localhost' IDENTIFIED BY 'mysecretpass'
	GRANT ALL PRIVILEGES ON * . * TO 'rushiagr'@'localhost'

Take a dump of database `rushi` and store it in a file `db.dump`. Execute this command in bash shell, and not in the MySQL shell.:
	mysqldump --user root rushi > db.dump

The End!

Comments/suggestions/feedback? Please feel free to comment and I'll make sure I acknowledge them to the fullest.

Cheers!


