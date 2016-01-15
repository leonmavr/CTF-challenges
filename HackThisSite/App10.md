###Tools  
* VB decompiler  
* Ollydbg  

###Solution  
Execute the program. If we try entering a password, a ```404 object(pwd); not found!``` message is returned.  
<p align="center">
  <img src=https://raw.githubusercontent.com/0xLeo/HackThisSite/master/img/App10_01.jpg title="img_01" width=60%>
</p> 
This time the executable cannot be decompiled by IDA. It is written in Visual Basic therefore open it with  
VB decompiler. Open the .exe using VB decompiler. There are two important sections of code  

1. ```Code -> Form1 -> Command1_Click_405500```  
2. ```Code -> Form1 -> Label1_Click_4049E0```  

<p align="center">
  <img src=https://raw.githubusercontent.com/0xLeo/HackThisSite/master/img/App10_03.jpg title="img_02" width=80%>
</p>  
\#1 seems to be invoked when the "Proceed" button is clicked. It calls a  MsgBox at address ```004055AD```.  
It also stores the string ```"Error: 404 object(pwd); not found!"``` at ```var_5C```, as shown at address ```0040558F```.  
  
Let's take a look into section ```Label1_Click_4049E0```. It starts at ```004049E0```. It, too, contains a single call to  
MsgBox. That should display the password. These are the only MsgBoxes the application invokes. Shouldn't  
the second one display the password? Let’s force the application to jump to that code section. Note the  
addresses of the code sections since they will be needed from now on.  
  
Open Ollydbg and navigate to ```00405500``` (the starting address of ```Command1_Click_405500```). By double clicking  
on the line or hitting spacebar, replace the (function initialisation):  
```
push ebp
mov ebp, esp
```
with a jump to the password(?) section:  
```
JMP 004049E0
```
Untick "Keep size fixed" and tick "Fill rest with nop".  
<p align="center">
  <img src=https://raw.githubusercontent.com/0xLeo/HackThisSite/master/img/App10_03.jpg title="img_03" width=80%>
</p>   
  
Write the changes to a new executable. Right click -> Edit -> Select all, Copy to executable and save it as exe.  
Run it, click "Proceed" and the password is obtained.  
<p align="center">
  <img src=https://raw.githubusercontent.com/0xLeo/HackThisSite/master/img/App10_04.jpg title="img_04" width=30%>
</p> 
