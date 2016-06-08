
###Tools###
* IDA Pro  

###Solution###

If we run the application, a password prompt appears and as soon as a wrong password is entered it exits.
Open it up with IDA by the default settings.  
The following section reads input from the user.  
<p align="center">
  <img src=https://github.com/0xLeo/CTF-challenges/blob/master/HackThisSite/App05img/image001.png title="img_01" width=50%>
</p>  
```var_4``` reads the current character and ```var_1C``` reads the length of the input string (number of chars + 1). ```var_4``` is renamed to ```inputChar``` and ```var_1C``` is renamed to ```inputLen```:  

Inspecting the big loop, the most important instructions along their addresses are:  
**1.** 
```
004010AE cmp     [ebp+var_20], 0Dh
```
 Obviously the truth of this condition implies we got the password. If false, the input is checked in another iteration. How ```var_20``` is evaluated is explained in part 4.  
**2.**  
```
004010C3 cmp     eax, [ebp+edx*4+var_18]
```
This compares ```eax``` to a local variable that resides ```-18h + edx*4``` bytes relative to the stack base pointer. If false, the program prints we got the wrong password and exits.  
(Note that according to IDA’s naming convention ```[ebp + 18h]``` is found ```18h``` bytes below the stack base, given the stack grows downwards.)  
**3.**   
```
004010BD mov     edx, [ebp+var_24]
004010A8 sub     edx, 1
```
This is important because it tells eax in part 2 which value to compare to. For example ```edx``` was initialised to 3 therefore eax would compare to ebp offset by ```3*4-18h =  -Ch```. And so forth.  
**4.** 
```
.text:0040109C mov     ecx, [ebp+var_20]
.text:0040109F add     ecx, 4
.text:004010A2 mov     [ebp+var_20], ecx
```
Note that ```var_20``` was initialised to 0. Recall part 1 where it’s compared to ```0Dh``` and it’s clear that the input check runs for *four* rounds.
    
What we need to do when debugging is avoid falling in the wrong password handler.   
Set breakpoints at:
```
004010B2 jnb     short loc_4010DC
004010C3 cmp     eax, [ebp+edx*4+var_18]
```
Start debugging (F9). Type a random password. When the second breakpoint is reached for the first time, edx equals 3. Therefore ```ebp+edx*4+var_18 = ebp – Ch```,. By hovering the mouse over the expression (at ```004010C3```), IDA tells us that this points to ```var_C```, whose value is ```65776F70h```.  
   <p align="center">
  <img src=https://github.com/0xLeo/CTF-challenges/blob/master/HackThisSite/App05img/image002.png  title="img_02" width=60%>
</p>    
Of course ```eax``` needs to be modified to the latter value. If the registers are not visible, go to ```Debugger > General registers```,  right click on ```eax```, and modify it with the right value.    
 <p align="center">
  <img src=https://github.com/0xLeo/CTF-challenges/blob/master/HackThisSite/App05img/image003.png  title="img_03" width=40%>
</p>    
  
Repeat the process 3 more times, stopping only at the second breakpoint to adjust ```eax```. Each time, write down the value at ```ebp + edx*4 + var_18h```.  
   <p align="center">
  <img src=hhttps://github.com/0xLeo/CTF-challenges/blob/master/HackThisSite/App05img/image004.png  title="img_04" width=60%>
</p>    
After the fourth iteration, the program exits. Recall the little endianess of Intel processors and observe each byte contained from ```var_C``` to ```var_18```. Do they form a pattern?  
  <p align="center">
  <img src=hhttps://github.com/0xLeo/CTF-challenges/blob/master/HackThisSite/App05img/image005.png  title="img_05" width=30%>
</p>    
  
  *Hint*: If a series of bytes reminds you of an Iron Maiden song title, you got it right ;)
