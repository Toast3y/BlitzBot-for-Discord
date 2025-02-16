# BlitzBot for Nuffle.xyz

BlitzBot is a Discord Bot to help administrators officiate leagues in Blood Bowl 3.

## How does it work?

BlitzBot connects (with permission) to Nuffle.xyz and returns formatted and neat data,
such as league pairings and the top results of who's winning in the league, while also
providing hyperlinks to relevant information and pages for a discerning coach to read.

## How to run BlitzBot

- BlitzBot requires Python 3.11 or higher

1. Install all dependencies:

	- Install discord.py - See here for more info: https://discordpy.readthedocs.io/en/stable/intro.html
	
	- Install audioop - pip install audioop-lts (due to an ongoing Discord.py requirement)
	
	- Install PyMySql - pip install PyMySQL
	
	- Install MariaDB (for database calls and features) - Latest installers can be found at: https://mariadb.org
	
2. Add env variables to establish data connections in env file.

3. Run BlitzBot by running "python blitzbot.py" from the command line.


