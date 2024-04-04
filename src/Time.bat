@echo off
%1 mshta vbscript:CreateObject("Shell.Application").ShellExecute("cmd.exe","/c %~s0 ::","","runas",1)(window.close)&&exit
cd /d "%~dp0"
echo 开始同步时间
net stop w32time
net start w32time
w32tm /config /manualpeerlist:"time.nist.gov" /syncfromflags:manual /reliable:yes /update
w32tm /resync
w32tm /resync
w32tm /config /manualpeerlist:"time.windows.com" /syncfromflags:manual /reliable:yes /update
w32tm /resync
w32tm /resync
echo 同步结束
pause