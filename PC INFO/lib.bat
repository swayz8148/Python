@echo off

REM Install required libraries
pip install psutil==5.8.0
pip install gputil==1.4.0
pip install wmi==1.5.1
pip install humanize==3.11.0

REM Verify installation
echo Installed libraries:
pip list | findstr /R "psutil gputil wmi humanize"
