@echo off
setlocal

:: Define paths
set "data_dir=C:\xampp\mysql\data"
set "backup_dir=C:\xampp\mysql\error_backup"

echo [1/5] Creating error_backup directory...
if exist "%backup_dir%" rd /s /q "%backup_dir%"
md "%backup_dir%"

echo [2/5] Copying folders except phpmyadmin, performance_schema, mysql...
for /d %%D in ("%data_dir%\*") do (
    set "folder=%%~nxD"
    setlocal enabledelayedexpansion
    if /i not "!folder!"=="phpmyadmin" ^
    if /i not "!folder!"=="performance_schema" ^
    if /i not "!folder!"=="mysql" ^
    robocopy "%%D" "%backup_dir%\!folder!" /e >nul
    endlocal
)

echo [3/5] Copying ibdata1...
if exist "%data_dir%\ibdata1" copy "%data_dir%\ibdata1" "%backup_dir%\" >nul

echo [4/5] Deleting contents of data directory...
for /d %%D in ("%data_dir%\*") do rd /s /q "%%D"
del /q "%data_dir%\*" >nul 2>&1

echo [5/5] Moving backup contents back to data directory...
move "%backup_dir%\*" "%data_dir%\" >nul

rd /q "%backup_dir%"

echo Done!
endlocal