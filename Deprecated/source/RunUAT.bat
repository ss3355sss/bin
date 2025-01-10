@echo off

rem echo %cd%       = pwd
rem echo %~dp0      = batch script execution location
rem echo %~dpnx0    = batch script name


call %~dp0Source/SetUnrealEngine.bat
if %ERRORLEVEL% NEQ 0 goto Error_SetUnrealEngine.bat

echo %ENGINE_DIR%



:Error_SetUnrealEngine.bat
EXIT /B 999