Pidtrk
======

Pidtrk creates a file to track all processes during a users session and a 
database to track all processes ever.

Setup as a startup application on your OS (through cron).  

Pidtrk will run as a daemon polling for spawned processes.

Pidtrk will check for a pidtrk.txt on startup. If Pidtrk finds a pidtrk.txt 
that file will be deleted and then creates a fresh file.  If no pidtrk.txt 
is found a new pidtrk.txt file is created. This pidtrk.txt will hold all 
processes for the user's session.  

Pidtrk will also check for a pidtrk.db file and create one if one doesn't 
already exist. This database will not be erase however and will contain a table 
of all the processes for every session.

You can edit the paths for these files, by default are written to the /home/user 
directory.

Root access is needed aswell to run Pidtrk. 
