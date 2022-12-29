# LOGUP - A log management utility with encryption. 

This use num6 encryption algorithm to encrypt data logs.


## Example LOG:
----------------------------
{1 : {"27/04/2022" : "This is a first log."},
{2 :  ......  }

## Encryption mode:
------------------------------
01020021020101030300103201000101110020202020101

## CRUD operation:
-----------------------------
To create new log file
logup --create/ -c "logfile_name" --pin/ -p PIN 

To add a log 
logup --file/ -f "logfile_name" --add/ -a "Bugfix 4021" --pin/ -p 524

To get fill log list 
logup --file/ -f "logfile_name" --list/ -l 

To get help
logup --help/ -h 

To change pin
logup --file/ -f "logfile_name" --changepin/ -cp 524 620 

To clear all logs 
logup --file/ -f "logfile_name" --cleanup/ -cu 

To get a log by number
logup --file/ -f "logfile_name" --item/ -i 5 

To add user global
logup --globalname/ -gn "Md. Almas Ali"
logup --globalemail/ -ge "almaspr3@gmail.com"


## File example:
------------------------
system-monitor.logup 
task.logup

## Test:
-----------
python logup.py 
