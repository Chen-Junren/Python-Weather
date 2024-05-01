@echo off
SETLOCAL EnableDelayedExpansion
for /F "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do rem"') do (
  set "DEL=%%a"
)
rem echo say the name of the colors, don't read
:start
rem cls

call :ColorText 0e "同步开始"
echo.
net stop w32time
net start w32time
w32tm /config /manualpeerlist:"time.nist.gov" /syncfromflags:manual /reliable:yes /update
w32tm /resync
w32tm /resync
w32tm /config /manualpeerlist:"time.windows.com" /syncfromflags:manual /reliable:yes /update
w32tm /resync
w32tm /resync
call :ColorText 0e "同步结束"
echo.
pause

goto :eof

:ColorText
echo off
<nul set /p ".=%DEL%" > "%~2"
findstr /v /a:%1 /R "^$" "%~2" nul
del "%~2" > nul 2>&1
goto :eof
