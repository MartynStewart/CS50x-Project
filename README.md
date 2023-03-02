# Quacksly the CS50 Discord Duck
#### Video Demo:  <URL HERE>
#### Description:

Quacksly is a helpful Discord bot that will help students of CS50 have an easier time connecting to work on a project together.


### Problem Statement
The idea started with the below message chain on the Final Project section of the CS50 Discord.

![Project Seed](/ideas/Seed.png)

A user looking for others to work with laments that their message will be lost in the whirlwind of other chats going on.


### Approach
+ The solution must be accessible on Discord alone - No external websites
+ Mobile users and desktop users should both be able to intergrate
+ The data must be retriveable at a later date(offline?) and not a simple post
+ The information has to be reactive - Don't spam/clutter needlessly
+ Commands/Actions should be simple
+ A duck must be involved

With the above approach laid out I decided that a bot on Discord would be the best solution. This bot should work similarly to a noticeboard where users can post and remove projects they are seeking help with and seekers can check the board and elect to sign up for projects (and remove their application). I realised that this bot would need to have a database to store this information.

### The Commands
<sub>Note all commands are case insensitive - Everything is treated as upper case for comparisons and storage</sub>


```
!quack
```
This is the root command that will initiate all other commands. Quacksly checks any new messages to see if they begin with this, if they do Quacksly will then take action

```
!quack help
!quack help projects
!quack help offers
!quack help create
!quack help join
```
These all result in Quacksly returning useful context on how to use each command

```
!quck projects
```
This will return a list of all open projects seeking help and the owner of said project (discord username including #0000 number to allow communication)

```
!quck offers
```
This will return the names of all usernames of who have offered to help with your project. It will also include the project name each time in the event you have multiple projects open

```
!quck create [project_name]
```
Creates a project with the user as an owner. Project name must be 1 word and must be unique. If it's not unique then the bot will append a unique ID number to the end (based on the users discord ID)

```
!quck join [project_name]
```
Adds an offer to the project for the user. Project_name must be an exact match otherwise it will return a fail state