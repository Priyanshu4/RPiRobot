@ECHO off
set ip=192.168.1.19
set /p ip=Enter Pi IP (hit ENTER for default [%ip%]):
set user=pi
set projectPath=home/%user%/Robot/
echo Deploying files to %projectPath% in user %user% at %ip%
scp -r .\*.py hardware server autonomy %user%@%ip%:/%projectPath%

