###Tools  
* IDA Pro 
* Any tool able to perform FFT analysis   

###Solution

By running the .exe, the following screen pops up.  
<p align="center">
  <img src=https://github.com/0xLeo/CTF-challenges/blob/master/HackThisSite/App09img/image001.jpg title="img_01" width=40%>
</p>  
The play button plays a continuous beep of three characteristic tones. Each match button plays another, beep of a slightly different tone. So let’s find out the frequencies of these beeps.  
Record all beeps in a wav file – I suggest one for the play button and one for buttons 1,2,3. When done recording them their exact frequencies need to be found.  
This can be achieved e.g. by FFT analysis using an audio editor such as WavePad Sound Editor on Windows or manually. For example in Matlab/ Octave, the sampled waveform of the play button in time domain looks as follows:  
<p align="center">
  <img src=https://github.com/0xLeo/CTF-challenges/blob/master/HackThisSite/App09img/image002.jpg title="img_02" width=60%>
</p>   
Zoom in and notice each “rectangle” consists of repetitions of a single sinusoid.  
<p align="center">
  <img src=https://github.com/0xLeo/CTF-challenges/blob/master/HackThisSite/App09img/image003.jpg title="img_03" width=60%>
</p>  
Given the width of half its cycle (in sample indices, from two successive zero crossings), its frequency is found. Details in App09.m. The result is that the frequencies of buttons 1,2,3 are offset by +100 from play button’s.  
Disassemble the program with IDA Pro and the following snippet is found in the text segment:  
```
.text:00405519                 push    offset a200     ; "200"
.text:0040551E                 call    edi ; __vbaI4Str
.text:00405520                 push    offset a600     ; "600"
.text:00405525                 mov     [esi+34h], eax
.text:00405528                 call    edi ; __vbaI4Str
.text:0040552A                 push    offset a1100    ; "1100"
```
Let’s follow the offset ```a200``` to find out where it points (double click it):  
```
text:0040522C a200:                                   ; DATA XREF: .text:00405519o
.text:0040522C                 unicode 0, <200>,0
.text:00405234                 dd 6
.text:00405238 a600:                                   ; DATA XREF: .text:00405520o
.text:00405238                 unicode 0, <600>,0
.text:00405240                 dw 8
.text:00405240                 unicode 0, <>,0
.text:00405244 a1100:                                  ; DATA XREF: .text:0040552Ao
.text:00405244                 unicode 0, <1100>,0
.text:0040524E                 align 10h
.text:00405250 a4:
.text:00405250                 unicode 0, <4>,0
.text:00405254 aAbcdefghijklmn:                        ; DATA XREF: .text:004057D5o
.text:00405254                 unicode 0, <abcdefghijklmnopqrstuvwxyz>,0
.text:0040528A                 align 4
.text:0040528C                 dd 6
.text:00405290 a100:                                   ; DATA XREF: .text:00405918o
.text:00405290                 unicode 0, <100>,0
.text:00405298 dword_405298    dd 33AD4EF1h, 11CF6699h, 0AA000CB7h, 93D36000h, 6
.text:00405298                                         ; DATA XREF: .text:0040596Bo
.text:00405298                                         ; .text:004059D9o ...
.text:004052AC a500:                                   ; DATA XREF: .text:0040598Co
.text:004052AC                 unicode 0, <500>,0
.text:004052B4                 dw 8
.text:004052B4                 unicode 0, <>,0
.text:004052B8 a1000:                                  ; DATA XREF: .text:004059F2o
.text:004052B8                 unicode 0, <1000>,0
```
So the values we need to change are obviously 100, 500, 1000:  
```
0x0040522C; a200
0x00405238; a600
0x00405244; a1100
```
Each needs to be incremented by 100. From IDA, view the hexdump and jump to the addresses of interest:  
```
.text:00405220  63 00 2E 00 00 00 00 00  06 00 00 00 32 00 30 00  c..........2.0.
.text:00405230  30 00 00 00 06 00 00 00  36 00 30 00 30 00 00 00  0......6.0.0...
.text:00405240  08 00 00 00 31 00 31 00  30 00 30 00 00 00 00 00  ...1.1.0.0.....
```
And change the values they contain (an ASCII chart might come in handy):  
<p align="center">
  <img src=https://github.com/0xLeo/CTF-challenges/blob/master/HackThisSite/App09img/image004.jpg title="img_04" width=72%>
</p>    
When done changing the values, save the changes to a new .dif file. 
```
File > Produce File > Create DIF file
```
Open the .dif file a text editor. It simply contains the changed bytes.  
```
0000522C: 32 31
00005238: 36 35
00005246: 31 30
```
Now all we need to do is apply the patch to the executable. The .c program found [here](http://pastebin.com/pe6DPJ73) ( (C) copyright Chris Eagle cseagle at gmail.com) does this job. Open up the command line and pass the patch and the executable as arguments:  
<p align="center">
  <img src=https://github.com/0xLeo/CTF-challenges/blob/master/HackThisSite/App09img/image005.png title="img_05" width=75%>
</p>    
Open the new executable and it’s cracked :)  
<p align="center">
  <img src=https://github.com/0xLeo/CTF-challenges/blob/master/HackThisSite/App09img/image006.jpg title="img_06" width=40%>
</p>  
