@echo off
REM Unregister the native messaging host

echo Unregistering BrowserToCalc native messaging host...

REM Unregister from Chrome
reg delete "HKEY_CURRENT_USER\Software\Google\Chrome\NativeMessagingHosts\com.example.browsertocalc" /f 2>nul

REM Unregister from Edge
reg delete "HKEY_CURRENT_USER\Software\Microsoft\Edge\NativeMessagingHosts\com.example.browsertocalc" /f 2>nul

echo.
echo Unregistration complete!
echo.
pause
