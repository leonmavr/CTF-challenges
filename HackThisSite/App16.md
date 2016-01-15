###Tools  
* IDA Pro  

###Solution  
Open it up with IDA. Reading the disassembly isn't that helpful. So let’s view the Functions (```View > Open subviews > Functions```). The following are found there:  
```
CreateFileA
DeleteFileA
ReadFile
WriteFile_0
```
That means that a file is probably created while the program is running and deleted when terminated.  
Now search the variable names (```View > Open subviews > Names```) for anything suspicious. A variable called ```aQuickBatchFile``` at address ```00419744``` is defined.  
Here’s a relevant code snippet:  
```
CODE:0041922B                 mov     edx, offset aQuickBatchFile "Quick Batch File Compiler"
CODE:00419230                 call    sub_404290
```
Is a batch file created during execution?
Just double click app16.exe and enter a password. Before exiting, search the C:\ disk for batch files that were created today. A file named btxxxx.bat, where xxxx is some sort of ID is found in the %temp% directory. Edit it. The password for the app is hidden there.
