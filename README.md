

# ![Quacksly](/ideas/Quacksly.png) Quacksly the CS50 Discord Duck
#### Video Demo:  <https://youtu.be/DNKT2PsY6tc>
#### Description:


Quacksly is a helpful Discord bot that will help students of CS50 have an easier time connecting to work on a project together.


## Problem Statement
The idea started with the below message chain on the Final Project section of the CS50 Discord.

![Project Seed](/ideas/Seed.png)

A user looking for others to work with laments that their message will be lost in the whirlwind of other chats going on.


## Approach
+ The solution must be accessible on Discord alone - No external websites
+ Mobile users and desktop users should both be able to intergrate
+ The data must be retriveable at a later date(offline?) and not a simple post
+ The information has to be reactive - Don't spam/clutter needlessly
+ Commands/Actions should be simple
+ A duck must be involved

With the above approach laid out I decided that a bot on Discord would be the best solution. This bot should work similarly to a noticeboard where users can post and remove projects they are seeking help with and seekers can check the board and elect to sign up for projects (and remove their application). I realised that this bot would need to have a database to store this information.


## Requirements
+ [Python 3 installed](https://www.python.org/downloads/)
+ [discord.py installed](https://discordpy.readthedocs.io/en/stable/)
+ [SQLite installed](https://www.sqlite.org/index.html)
+ [dotenv installed](https://github.com/motdotla/dotenv)
+ projects.db file with the correct schema in the bot directory
+ .env file with the bot token (DISCORD_TOKEN) and a trigger word (TRIGGER)

![env Example](/ideas/envExample.png)

## The Commands
<sub>Note all commands are case insensitive - Everything is treated as upper case for comparisons and storage</sub>


```
!quack
```
This is the root command that will initiate all other commands. Quacksly checks any new messages to see if they begin with this, if they do Quacksly will then take action. Quacksly will quack back at users who don't give commands

```
!quack help
!quack help projects
!quack help offers
!quack help create
!quack help join
!quack help deleteProject
!quack help deleteOffer
```
These all result in Quacksly returning useful context on how to use each command

```
!quack projects
```
This will return a list of all open projects seeking help and the owner of said project (discord username including #0000 number to allow communication)

```
!quack offers
```
This will return the names of all usernames of who have offered to help with your project. It will also include the project name each time in the event you have multiple projects open

```
!quack create [project_name]
```
Creates a project with the user as an owner. Project name must be 1 word and must be unique. If it's not unique then the bot will append a unique ID number to the end (based on the users discord ID)

```
!quack join [project_name]
```
Adds an offer to the project for the user. Project_name must be an exact match otherwise it will return a fail state

```
!quack deleteProject [project_name]
```
Deletes the named project from the DB only if it exists and the requestor was the original creator. Also removes any offers

```
!quack deleteOffer [project_name]
```
Deletes the users offer to help on the named project (if it exists)

## bot.py

Central file for instantiating and carrying out actions for the bot. This impliments discords on API and includes the library `discord.py`. Full details of the [API can be found here](https://discordpy.readthedocs.io/en/stable/index.html)

__Standard API functions included__
`on_ready()` is called when the bot loads in after creation
`on_message(message)` is called when a new message is entered in a channel Quacksly can see. This contains a message object as detailed in the API. If Quacksly detects the trigger word then follow up checks are made via `parseRequest()` otherwise it's ignored.

__Custom functions__
`parseRequest(message, uid)` is responsible to deciding what action the user wants to take TODO: Stop this being a massive IF ELSE section.
`discord_username(uid)` uses Discord API to get the username based on a unique discord user id - This is an API call rather than using the cached members list. Open selected as it's not going to be a consistently used call.
`projects() | offers(uid) | create(uid, pName) | join(uid, pName)` execute the command identified by the `parseRequest()` function. These also clean up the response from the database to be user friendly


## dbAccess.py

File responsible for accessing a locally stored DB via SQL. I've implimented SQLite to do this as it's small and fast. My db is only going to be storing a few tables and using a handful of simple SQL statements to access them so my solution didn't need to be complex. Full docs for [SQLite can be found here](https://www.sqlite.org/docs.html)

__Custom functions__
`commit()` As the db won't be setup in auto commit mode this function is called when a commitable action has been taken by the rest of the code. This has been handy for testing as it's allowed me to test junk data into my db without causing issues later (such as invalid user ids being stored)

`getUniqueName(seed, ProjectName)` A recursive function to check a project name is unique and if not it will generate a new name for the project. The seed intially is the unique discord username of the user which has all of its digits summed to create a number to append to the project name, this is checked and if not unique then it's re-ran but the seed is incremented by 1 until a  unique name is found. 

`ActiveProjects() | FindSignUps(uID)` Are simple look ups for the database using SELECT statements. No user inputs are needed for either. The second uses the unique discord username.

`CreateProject(uID, ProjectName) | CreateSignUp(uID, ProjectName)` Do the insertions into the database. These use SQLites functionality to clean the data before it's inserted to attempt to avoid SQL injection attacks as the ProjectName is user generated.


## projects.db

__.schema__
```
CREATE TABLE `activeProjects` (
	`ID` INTEGER  PRIMARY KEY,
	`owner` INTEGER unsigned NOT NULL,
	`project_name` TEXT NOT NULL,
	'timedate'  DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE `activeParticipants` (
	`ID` INTEGER  PRIMARY KEY,
	`project_id` INTEGER unsigned NOT NULL,
	`helper` TEXT NOT NULL,
	'timedate'  DATETIME DEFAULT CURRENT_TIMESTAMP
);
```
__rational__

`activeProjects` stores the owner/creators unique discord ID and the name of the project - Note this isn't denoted as unique but is enforced by the code prior to being entered. ID will be auto generated to keep track of individual projects and the timedate will be auto saved - Potential future expansion to allow cleaning projects over 90 days old.

`activeParticipants` stores a project ID from the previous table as well as the person offering helps unique discord id. Again timedate is captured but goes unused currently but could be expended later to help with cleaning the db up

## Possible changes

+ Auto clean up the DB after a period of time
+ Create a 3rd table to store a project description to allow further information to be shared
+ GDPR compliance - Storage of personally identifiable information could be a GDPR issue though data is only stored via consent of using the commands and 1 user can't sign another up there may still be further things to look at to ensure compliance

## Example Usage

![Example usage](/ideas/QuackslyExamples.png)