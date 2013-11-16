Pidtrk
======

Pidtrk creates a file to track all processes during a users session and a 
database to track all processes ever.

Setup as a startup application on your OS (through cron).  

Pidtrk will run as a daemon polling for spawned processes.

Pidtrk will create a fresh `.pidtrk.log` in the directory it is being run from 
This `.pidtrk.log` will hold all processes for the user's session.  

Pidtrk will also check for a pidtrk.db file and create one if one doesn't 
already exist. This database will not be erase however and will contain a table 
of all the processes for every session.

You can edit the paths for these files, by default are written to the /home/user 
directory.

Root access is needed aswell to run Pidtrk. 
