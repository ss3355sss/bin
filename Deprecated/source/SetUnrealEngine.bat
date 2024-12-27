@echo off
setlocal enabledelayedexpansion

:: Find PROJECT_FILE
set PROJECT_FILE=""
for %%I in (*.uproject) do set PROJECT_FILE=%%I
if %PROJECT_FILE% == "" goto Error_NoProjectFile

:: Find Engine Association from uproject file
set KEY="\"EngineAssociation\""
set ENGINE_ASSOCIATION=""
for /f "tokens=*" %%a in ('findstr %KEY% %~dp0%PROJECT_FILE%') do (
    set LINE=%%a

    :: remove empty space
    set "VALUE=!LINE:*: =!"

    :: remove double quotation marks
    set "VALUE=!VALUE:~1,-2!"
    set ENGINE_ASSOCIATION=!VALUE!
)
if %ENGINE_ASSOCIATION% == "" goto Error_NoEngineAssociation


:: Find ENGINE_DIR
set ENGINE_DIR=""
for /f "delims=" %%a in ('reg query "HKEY_CURRENT_USER\Software\Epic Games\Unreal Engine\Builds" /f "%ENGINE_ASSOCIATION%" /s 2^>nul ^| find /I "%ENGINE_ASSOCIATION%"') do set "ENGINE_DIR=%%a"
for /f "tokens=3*" %%a in ("%ENGINE_DIR%") do if "%%b"=="" (
    ::When the directory does not contain a space
    set "ENGINE_DIR=%%a"
) else (
    ::When the directory contains a space
    set "ENGINE_DIR=%%a %%b"
)
if %ENGINE_DIR% == "" goto Error_NoEngineDir


:Error_NoProjectFile
echo ERROR: Failed to get vaild PROJECT_FILE
EXIT /B 999

:Error_NoEngineAssociation
echo ERROR: Failed to get vaild ENGINE_ASSOCIATION
EXIT /B 999

:Error_NoEngineDir
echo ERROR: Failed to get vaild ENGINE_DIR
EXIT /B 999

