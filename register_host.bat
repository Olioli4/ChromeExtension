@echo off
REM Register the native messaging host for Chrome and Edge

echo Registering BrowserToCalc native messaging host...

REM Register for Chrome
reg add "HKEY_CURRENT_USER\Software\Google\Chrome\NativeMessagingHosts\com.example.browsertocalc" /ve /t REG_SZ /d "D:\Browsertocalc\browsertocalc_host.json" /f

REM Register for Edge
reg add "HKEY_CURRENT_USER\Software\Microsoft\Edge\NativeMessagingHosts\com.example.browsertocalc" /ve /t REG_SZ /d "D:\Browsertocalc\browsertocalc_host.json" /f

echo.
echo Registration complete!
echo.
echo Next steps:
echo 1. Load your extension in Chrome/Edge developer mode
echo 2. Note the extension ID from chrome://extensions
echo 3. Update browsertocalc_host.json with the correct extension ID
echo 4. Test the extension
echo.
pause
