##Level00
  
###[Instructions](https://exploit-exercises.com/nebula/)  
A file (executable) with Set User ID (SUID) permissions needs to be found.  
SUID is set by an extra bit type in the user octet in the file permissions  
indicated by `S` (intead of r/w/x). When it is set, it allows the user to  
temporarily run the program as its owner, which may lead to exploits.  
*A hint from the instrutions: consult the find command manual.*  
  
###Solution
The objective is clear. Search the filesystem for a file with SUID permissions.  
Therefore:  
find in the filesystem \  
a file \  
with SUID permissions \  
throw error in /dev/null \  
and store results in temp.txt
```
$ find /  
> -type f  
> -perm -u+s  
> 2>/dev/null  
> > temp.txt
$ head temp.txt
/bin/.../flag00
<sniped>
```
Execute the file:
```
$ /bin/.../flag00
Congrats, now run getflag to get your flag!
$ getflag
You have successfully executed getflag on a target account
```  
The option `-type f -executable` could narrow down the results but the flag  
is captured.  

###References  
* Schneiter, S., Stanger, J., Pessanha, B. and Haeder, A. (2010). LPI  
Linux certification in a nutshell. 2nd ed. Beijing: O'Reilly, p.440.
