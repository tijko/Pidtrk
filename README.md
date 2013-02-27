Pidtrk
======

Creates a file to track all processes during a users session and a database to track all processes ever.


Setup as a startup application on your OS.  

Pidtrk will run as a daemon polling for spawned processes.

Pidtrk will check for a log.txt on startup and delete and create a fresh file or will created a new file.
This log.txt will hold all processes for the user's session.  

Pidtrk will also check for a pidtrk.db file and create one if one doesn't already exist.  
This database will not be erase however and will contain table of all the processes for every session.

You can edit the paths for these files and are by default written to the /home/user directory.

Root access is needed aswell to run Pidtrk. 
