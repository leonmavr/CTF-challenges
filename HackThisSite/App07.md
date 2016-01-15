###Tools  

* IDA Pro  
* Python interpreter  

###Solution  

Load the .exe in IDA with default options. Jump to graphical view and view the first loop:  
```
.text:0040103F loc_40103F:                             ; CODE XREF: _main+62j
.text:0040103F                 call    j___fgetchar
.text:00401044                 mov     [ebp+var_4], al
.text:00401047                 movsx   ecx, [ebp+var_4]
.text:0040104B                 mov     edx, [ebp+var_1C]
.text:0040104E                 add     edx, ecx
.text:00401050                 mov     [ebp+var_1C], edx
.text:00401053                 movsx   eax, [ebp+var_4]
.text:00401057                 cmp     eax, 0Ah
.text:0040105A                 jz      short loc_401064
.text:0040105C                 movsx   ecx, [ebp+var_4]
.text:00401060                 test    ecx, ecx
.text:00401062                 jnz     short loc_40103F
```
The ```j___fgetchar``` function kind of gives away the above instructions do. ```[ebp+var_4]``` stores the value returned by the latter function (character read). It is evident from ```.text:0040104B-50``` that ```var_1C``` stores the sum of all characters entered so far, including the return (```0Ah```). Next, if the current character (```var_4```) is return (```0Ah```), jump to address ```401064```. If it is not ```EOF``` or ```NULL```, return to ```00401062```. Therefore ```var_4``` is renamed to ```char_input``` and ```var_1C``` is renamed to ```input_sum```.    

Next a file ```encrypted.enc``` is read. The following lines check some conditions based on ```var_24```:  
```
.text:00401093
.text:00401093 loc_401093:                             ; CODE XREF: _main+7Dj
.text:00401093                                         ; _main+17Bj
.text:00401093                 mov     edx, [ebp+var_24]
.text:00401096                 and     edx, 4
.text:00401099                 test    edx, edx
.text:0040109B                 jz      short loc_4010AB
.text:0040109D                 mov     eax, [ebp+var_24]
.text:004010A0                 and     eax, 1
.text:004010A3                 test    eax, eax
.text:004010A5                 jnz     loc_401180
```
```[ebp+var_24]``` is ANDed with 4 (```1000```) and the result is stored in ```edx```. If ```ZF``` is set, the program continues to address  
```4010AB``` to resume the formation of a sum (explained later). Otherwise, the same local variable is ANDed with 1 (```0001```) and jumps  
to ```4010AB```  if the result is non-zero. What do these logical operations mean?  
The sum processing (mentioned) above will take place as long as ```[ebp+var_24] & 4) == 0) || (([ebp+var_24] & 1) == 0```, i.e. for 5 (0th to 4th) runs.  
```var_24``` acts as a counter. Before we analyse the section  below ```4010AB```, have a look at the following lines:    
```
.text:0040118C                 cmp     [ebp+var_18], 0DCAh
.text:00401193                 jnz     short loc_4011A8
```
If the comparison returns ```0```, the program eventually reaches address ```401199```, where the "Congratulations" message is dumped.  
Now focus on ```4010D8```, where operations on ```[ebp+var_18]``` take place. They can be summarised by the following pseudocode:  
```
for i from 0 to 4:
	var_18 += input_sum ^ enc[i]
end
```
, where ```^``` denotes ```XOR``` operation. For convenience, ```var_18``` will be renamed to ```xor_sum```.
The rest of the main loop loads some values in an array based on an index which runs from 0 to input_sum. It does not affect ```xor_sum``` though,  
which is all we need for the password.  
  
If the latter pseudocode is reversed, the first five encoded characters – the ones that contribute to the checksum can be obtained.  
So just solve for each one of them:  
```
for i from 1 to 5:
  enc[i-1] = (xor_sum[i] - xor_sum[i-1]) ^ char_sum
end
```
Setting some breakpoints at ```4010E8``` and ```40118C``` will let us measure ```xor_sum``` at each run. Since ```char_sum``` is previously known, ```enc[i-1]``` can be found. Also, add ```xor_sum``` and ```char_sum``` to the watch list (Select it and on the menu Debugger > Watches > Watch List).  
Debug the program (F9). For testing, ```aaaaa``` was entered as password at the command prompt. ```char_sum``` is ```1EF``` and the ```xor_sum``` values are ```0 280, 57C, 804, A88, D0A```. A quick and dirty [python script](https://github.com/0xLeo/HackThisSite/blob/master/App07.py) based on the last loop has been written to compute the encoded characters (```enc```).  
Run this to obtain the 5 encoded chars (```enc``` list). The answer is represented with stars so that the solution is not spoiled. ```enc = [*, *, *, *, *]``` - these characters are staticly encoded in the ```encrypted.enc``` file. All we need now is a sum of characters that  makes ```xor_sum``` equal to ```0DCA```.  
The python script emulates the program (actually the parts relevant to the pass code). It is split in three parts:    
**1.** encode(flag) – solves for the encoded chars ```enc```, has been discussed  
**2.** decode() – given a certain input (```input_str```), it computes ```xor_sum``` at each run. Its purpose is to check if the values it finds are consistent with IDA’s.  
**3.** test_sum_chars(low,high,flag) – finds xor_sum for a range of sum_chars (sum of input characters) and compares it to the  checksum (```0DCA```). If the correct ```sum_chars``` is found, it stops and prints it. The range is a intuitive, therefore  given some intuition on how the program works, the script works as a brute forcer.  
  
The required ```sum_chars``` has been found when testing within the range ```[500,900]```. All that remains is to find an ASCII string with sum of characters equal to that sum_chars, however long. That is really easy by consulting the ACSII chart.    
Enter it in the command prompt and the "Congratulations" message with the password is dumped ;)
